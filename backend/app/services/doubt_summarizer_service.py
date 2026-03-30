import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# --- 1. SETUP & IMPORTS ---
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.prompts import PromptTemplate
    from pydantic import BaseModel, Field
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseModel = object
    Field = lambda **kwargs: None
    ChatGoogleGenerativeAI = None
    JsonOutputParser = None
    PromptTemplate = None

# Config import
try:
    from app.core.config import settings
except ImportError:
    import os
    class MockSettings:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        GEMINI_MODEL = "gemini-2.5-flash"
    settings = MockSettings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# REAL IMPORTS (Person 1 + Person 2)
# -----------------------------------------------------------------------------
from app.models.doubts import DoubtUpload, DoubtMessage
from app.schemas.doubts import DoubtUploadCreate, WeeklySummaryResponse

# -----------------------------------------------------------------------------
# SERVICE
# -----------------------------------------------------------------------------

class DoubtSummarizerService:
    def __init__(self):
        """Initialize LLM + JSON parser"""
        self.llm = None
        self.parser = None

        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not installed. Doubt summarizer will not work.")
            logger.warning("Install with: pip install langchain langchain-google-genai")
            return

        if not settings.GOOGLE_API_KEY:
            logger.warning("⚠️ Google API Key missing — LLM disabled.")
            return

        try:
            self.parser = JsonOutputParser(pydantic_object=WeeklySummaryResponse)
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.2,
                convert_system_message_to_human=True
            )
            logger.info("DoubtSummarizerService initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")

    # -------------------------------------------------------------------------
    # Task 1 — Save Upload + Messages
    # -------------------------------------------------------------------------
    def create_doubt_upload(self, db: Session, upload_in: DoubtUploadCreate, user_id: int):
        """
        Saves the upload metadata and related messages into the database.
        """

        # Create upload
        new_upload = DoubtUpload(
            course_code=upload_in.course_code,
            source=upload_in.source,
            created_by_id=user_id
        )
        db.add(new_upload)
        db.commit()
        db.refresh(new_upload)

        # Create messages
        for msg in upload_in.messages:
            new_message = DoubtMessage(
                upload_id=new_upload.id,
                author_role=msg.get("author_role", "student"),
                text=msg.get("text")
            )
            db.add(new_message)

        db.commit()
        return new_upload

    # -------------------------------------------------------------------------
    # Task 2 — Fetch Recent Messages
    # -------------------------------------------------------------------------
    def get_recent_messages_for_course(
        self, 
        db: Session, 
        course_code: str, 
        limit: int = 100,
        period: str = None,
        source: str = None
    ) -> List[str]:
        """
        Fetch the most recent messages for a course with optional period and source filters.
        
        Args:
            period: 'daily', 'weekly', 'monthly', or None for all time
            source: 'forum', 'email', 'chat', or None for all sources
        """
        from datetime import datetime, timedelta

        query = (
            db.query(DoubtMessage.text)
            .join(DoubtUpload, DoubtMessage.upload_id == DoubtUpload.id)
            .filter(DoubtUpload.course_code == course_code)
        )

        # Apply period filter
        if period:
            now = datetime.utcnow()
            if period == 'daily':
                start_date = now - timedelta(days=1)
            elif period == 'weekly':
                start_date = now - timedelta(weeks=1)
            elif period == 'monthly':
                start_date = now - timedelta(days=30)
            else:
                start_date = None
            
            if start_date:
                query = query.filter(DoubtUpload.created_at >= start_date)

        # Apply source filter
        if source and source != 'all':
            query = query.filter(DoubtUpload.source == source)

        rows = query.order_by(DoubtUpload.created_at.desc()).limit(limit).all()

        return [r[0] for r in rows]

    # -------------------------------------------------------------------------
    # Task 3 — LLM Analysis (Summary + Topics + Insights)
    # -------------------------------------------------------------------------
    async def generate_summary_topics_insights(self, messages: List[str], course_code: str, include_stats: bool = False) -> Dict[str, Any]:
        """
        Sends messages to Gemini to generate structured summaries.
        
        Args:
            messages: List of doubt message texts
            course_code: Course identifier
            include_stats: If True, caller should add stats separately
        """

        if not self.llm:
            return {"error": "LLM not configured"}

        if not messages:
            return self._empty_state(course_code)

        prompt = PromptTemplate(
            template="""
You are an expert academic assistant analyzing doubts for "{course_code}".

Analyze the following student queries:
{doubts_text}

Return ONLY valid JSON with:
- overall_summary
- topics (clusters)
- learning_gaps
- insights

{format_instructions}
            """,
            input_variables=["course_code", "doubts_text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            }
        )

        chain = prompt | self.llm | self.parser

        try:
            formatted = "\n".join([f"- {m}" for m in messages])
            result = await chain.ainvoke({
                "course_code": course_code,
                "doubts_text": formatted
            })
            
            # Calculate recurring issues: learning gaps mentioned by multiple students
            if isinstance(result, dict) and 'learning_gaps' in result:
                recurring_count = sum(1 for gap in result.get('learning_gaps', []) 
                                     if isinstance(gap, dict) and gap.get('student_count', 0) > 1)
                result['recurring_issues_count'] = recurring_count
            
            return result
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return {"error": str(e)}

    # -------------------------------------------------------------------------
    # Task 3.5 — Compute Enhanced Statistics
    # -------------------------------------------------------------------------
    def compute_summary_stats(self, db: Session, course_code: str, period: str = None, source: str = None) -> Dict[str, Any]:
        """
        Compute comprehensive statistics including message counts, unique uploads, and recurring issues.
        """
        from datetime import datetime, timedelta
        from sqlalchemy import func, distinct

        query = (
            db.query(
                func.count(DoubtMessage.id).label('total_messages'),
                func.count(distinct(DoubtUpload.id)).label('unique_uploads')
            )
            .join(DoubtUpload, DoubtMessage.upload_id == DoubtUpload.id)
            .filter(DoubtUpload.course_code == course_code)
        )

        # Apply period filter
        if period:
            now = datetime.utcnow()
            if period == 'daily':
                start_date = now - timedelta(days=1)
            elif period == 'weekly':
                start_date = now - timedelta(weeks=1)
            elif period == 'monthly':
                start_date = now - timedelta(days=30)
            else:
                start_date = None
            
            if start_date:
                query = query.filter(DoubtUpload.created_at >= start_date)

        # Apply source filter
        if source and source != 'all':
            query = query.filter(DoubtUpload.source == source)

        result = query.first()

        return {
            'total_messages': result.total_messages if result else 0,
            'unique_uploads': result.unique_uploads if result else 0
        }

    # -------------------------------------------------------------------------
    # Task 4 — Get Source Breakdown
    # -------------------------------------------------------------------------
    def get_source_breakdown(self, db: Session, course_code: str, period: str = None) -> Dict[str, Any]:
        """
        Get breakdown of doubts by source (forum, email, chat) with counts and percentages.
        """
        from datetime import datetime, timedelta
        from sqlalchemy import func

        query = (
            db.query(
                DoubtUpload.source,
                func.count(DoubtMessage.id).label('count')
            )
            .join(DoubtMessage, DoubtUpload.id == DoubtMessage.upload_id)
            .filter(DoubtUpload.course_code == course_code)
        )

        # Apply period filter
        if period:
            now = datetime.utcnow()
            if period == 'daily':
                start_date = now - timedelta(days=1)
            elif period == 'weekly':
                start_date = now - timedelta(weeks=1)
            elif period == 'monthly':
                start_date = now - timedelta(days=30)
            else:
                start_date = None
            
            if start_date:
                query = query.filter(DoubtUpload.created_at >= start_date)

        results = query.group_by(DoubtUpload.source).all()

        # Calculate totals and percentages
        total = sum(r.count for r in results)
        breakdown = {}
        
        for result in results:
            source_name = result.source
            count = result.count
            percentage = round((count / total * 100), 1) if total > 0 else 0
            breakdown[source_name] = {
                "count": count,
                "percentage": percentage
            }

        # Ensure all sources are present (even if 0)
        for source in ['forum', 'email', 'chat']:
            if source not in breakdown:
                breakdown[source] = {"count": 0, "percentage": 0}

        return {
            "total": total,
            "breakdown": breakdown
        }

    # -------------------------------------------------------------------------
    # Empty State
    # -------------------------------------------------------------------------
    def _empty_state(self, course_code: str):
        return {
            "course_code": course_code,
            "overall_summary": "No data.",
            "topics": [],
            "learning_gaps": [],
            "insights": []
        }


# GLOBAL INSTANCE
doubt_summarizer_service = DoubtSummarizerService()
