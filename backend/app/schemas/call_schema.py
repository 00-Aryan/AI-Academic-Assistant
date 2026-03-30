"""
Pydantic schemas for voice call API endpoints.

This module defines request and response models for Twilio voice call operations.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from app.models.enums import CallStatusEnum


class CallCreateRequest(BaseModel):
    """Request model for creating/starting a new call session."""
    caller_number: Optional[str] = Field(None, max_length=50)
    twilio_sid: str = Field(..., max_length=100)
    language: Optional[str] = Field(None, max_length=10)
    location: Optional[str] = Field(None, max_length=255)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class CallUpdateRequest(BaseModel):
    """Request model for updating call information."""
    status: Optional[CallStatusEnum] = None
    duration: Optional[str] = Field(None, max_length=50)
    recording_url: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = None


class CallResponse(BaseModel):
    """Response model for call information."""
    id: UUID
    caller_number: Optional[str]
    twilio_sid: str
    language: Optional[str]
    location: Optional[str]
    status: CallStatusEnum
    duration: Optional[str]
    recording_url: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CallSpeechProcessRequest(BaseModel):
    """Request model for processing speech input during a call."""
    call_id: str
    speech_text: str = Field(..., min_length=1, max_length=5000)
    language: Optional[str] = Field(None, max_length=10)


class CallSpeechProcessResponse(BaseModel):
    """Response model for speech processing result."""
    call_id: str
    query_id: str
    response_text: str
    tts_url: Optional[str] = None
    language: str
    confidence: int = Field(ge=0, le=100)
    processing_time_ms: int


class CallStatusUpdate(BaseModel):
    """Request model for Twilio call status updates."""
    CallSid: str
    CallStatus: str
    CallDuration: Optional[str] = None
    RecordingUrl: Optional[str] = None


class ActiveCallsResponse(BaseModel):
    """Response model for listing active calls."""
    total: int
    calls: list[CallResponse]


class CallMetrics(BaseModel):
    """Model for call analytics and metrics."""
    total_calls: int
    active_calls: int
    completed_calls: int
    failed_calls: int
    avg_duration_seconds: float
    languages_used: Dict[str, int]
    success_rate: float
