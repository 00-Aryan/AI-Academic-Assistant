"""
Database models package.

This module exports all SQLAlchemy models for easy imports and
ensures they are registered with SQLAlchemy's Base registry.
"""

from app.models.user import User
from app.models.query import Query, QueryResponse
from app.models.resource import Resource
from app.models.announcement import Announcement
from app.models.profile import Profile
from app.models.course import Course
from app.models.user_course import UserCourse
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.doubts import DoubtUpload, DoubtMessage
from app.models.slide_deck import SlideDeck
from app.models.tag import Tag
# (and any others that appear in relationship("...") strings)

# New models for knowledge base, calls, tasks
from app.models.enums import (
    CategoryEnum,
    TaskTypeEnum,
    TaskStatusEnum,
    SourceTypeEnum,
    CallStatusEnum
)
from app.models.knowledge import KnowledgeSource, KnowledgeChunk
from app.models.call import Call
from app.models.chat_session import ChatSession
from app.models.task import Task

__all__ = [
    # Original models
    "User",
    "Query",
    "QueryResponse",
    "Resource",
    "Announcement",
    "Profile",
    # Course management models
    "Course",
    "UserCourse",
    "Quiz",
    "QuizAttempt",
    "DoubtUpload",
    "DoubtMessage",
    "SlideDeck",
    "Tag",
    # Enums
    "CategoryEnum",
    "TaskTypeEnum",
    "TaskStatusEnum",
    "SourceTypeEnum",
    "CallStatusEnum",
    # Knowledge base
    "KnowledgeSource",
    "KnowledgeChunk",
    # Voice calls
    "Call",
    # Chat sessions
    "ChatSession",
    # Background tasks
    "Task",
]
