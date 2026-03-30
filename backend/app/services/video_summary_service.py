import logging
from app.core.config import settings

# LangChain imports with fallback
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    ChatGoogleGenerativeAI = None
    PromptTemplate = None

# Import the library you have
try:
    import youtube_transcript_api
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoSummaryService:
    def __init__(self):
        self.llm = None
        # We instantiate the API class because your version seems to require it
        self.yt_api = YouTubeTranscriptApi() if YouTubeTranscriptApi else None

        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not installed. Video summary will not work.")
            return

        if settings.GOOGLE_API_KEY:
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0.3
                )
            except Exception as e:
                logger.error(f"Failed to init LLM: {e}")

    def extract_video_id(self, url: str) -> str:
        """Extracts video ID from a YouTube URL."""
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return url

    def get_transcript(self, video_id: str) -> str:
        """Fetches transcript from YouTube using the .fetch() method."""
        if not self.yt_api:
            logger.error("YouTube Library not installed.")
            return None
            
        try:
            # --- ADAPTED FOR YOUR VERSION ---
            # Using .fetch() instead of .get_transcript()
            # We try to get the raw data if possible, or handle the object
            transcript_object = self.yt_api.fetch(video_id)
            
            # If .fetch() returns a list directly (standard for some variants)
            if isinstance(transcript_object, list):
                transcript_list = transcript_object
            # If it returns an object with a method to get data
            elif hasattr(transcript_object, 'to_raw_data'):
                transcript_list = transcript_object.to_raw_data()
            # Fallback: assume it's the list itself or iterable
            else:
                transcript_list = transcript_object

            # Combine text
            full_text = " ".join([t['text'] for t in transcript_list])
            return full_text
            
        except Exception as e:
            logger.error(f"Transcript Fetch Error: {e}")
            return None

    async def summarize_video(self, video_url: str) -> dict:
        if not self.llm:
            return {"error": "LLM not configured"}

        video_id = self.extract_video_id(video_url)
        if not video_id:
             return {"error": "Invalid YouTube URL"}

        transcript = self.get_transcript(video_id)

        if not transcript:
            return {"error": "Could not fetch transcript. The video might not have captions enabled."}

        # Limit transcript length to ~15k characters to fit Gemini's context window
        truncated_transcript = transcript[:15000]

        prompt = PromptTemplate.from_template("""
        You are an expert academic assistant. Summarize the following video transcript.
        
        **Transcript:**
        {text}
        
        **Instructions:**
        1. Provide a concise summary (3-5 sentences).
        2. List 3-5 key takeaways/bullet points.
        3. Mention the estimated difficulty level.
        4. **Further Learning:** Suggest 3 short, specific Google Search queries that the user should search to learn more about these topics. Format them as a bulleted list.
        
        Return the result in Markdown format.
        """)

        try:
            chain = prompt | self.llm
            result = await chain.ainvoke({"text": truncated_transcript})
            return {"summary": result.content}
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return {"error": str(e)}

video_summary_service = VideoSummaryService()