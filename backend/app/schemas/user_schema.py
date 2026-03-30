"""
User-related Pydantic schemas for request/response validation.

This module defines all schemas related to user authentication,
registration, and profile management.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


# ----------- Enums -----------


class UserRole(str, Enum):
    """User role enumeration for role-based access control."""
    STUDENT = "student"
    TA = "ta"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


# ----------- Request Schemas -----------


class UserCreate(BaseModel):
    """
    Schema for user registration.

    Attributes:
        email: Valid email address (RFC 5322 compliant)
        password: Password with minimum 8 characters, must contain:
                  - At least one uppercase letter
                  - At least one lowercase letter
                  - At least one digit
        role: User role (student, ta, instructor, admin)
        full_name: User's full name (optional during registration)
        course_ids: List of course IDs (required for TA/Instructor, ignored for students)

    Example:
        {
            "email": "ta@example.com",
            "password": "SecurePass123",
            "role": "ta",
            "full_name": "Jane Smith",
            "course_ids": [1, 3, 5]
        }
    """
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password with min 8 characters"
    )
    role: UserRole = Field(
        default=UserRole.STUDENT,
        description="User role: student, ta, instructor, or admin"
    )
    full_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="User's full name"
    )
    course_ids: Optional[List[int]] = Field(
        default_factory=list,
        description="List of course IDs (required for TA/Instructor)"
    )


class UserLogin(BaseModel):
    """
    Schema for user authentication.

    Attributes:
        email: Registered email address
        password: User's password

    Example:
        {
            "email": "student@example.com",
            "password": "SecurePass123"
        }
    """
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="User password")


class UserUpdate(BaseModel):
    """
    Schema for updating user information.

    All fields are optional - only provided fields will be updated.

    Attributes:
        full_name: Updated full name
        email: Updated email address
        current_password: Current password (required if changing password)
        new_password: New password

    Example:
        {
            "full_name": "Jane Doe",
            "email": "newemail@example.com"
        }
    """
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    current_password: Optional[str] = Field(
        None,
        description="Required when changing password"
    )
    new_password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=100,
        description="New password"
    )


# ----------- Response Schemas -----------


class UserSimpleResponse(BaseModel):
    """
    A simplified user schema for nested responses.

    This schema is useful for embedding creator/user information within
    other API responses without exposing sensitive details.

    Attributes:
        id: User's unique identifier
        email: User's email address
        full_name: User's full name
    """
    id: int
    email: EmailStr
    full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    """
    Schema for user data in API responses.

    This schema excludes sensitive information like passwords.

    Attributes:
        id: User's unique identifier
        email: User's email address
        role: User's role in the system
        full_name: User's full name
        is_active: Whether the user account is active
        created_at: Account creation timestamp

    Example:
        {
            "id": 1,
            "email": "student@example.com",
            "role": "student",
            "full_name": "John Doe",
            "is_active": true,
            "created_at": "2025-01-15T10:30:00Z"
        }
    """
    id: int
    email: EmailStr
    role: UserRole
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """
    Schema for JWT token response after successful authentication.

    Attributes:
        access_token: JWT access token for API authentication
        refresh_token: JWT refresh token for obtaining new access tokens
        token_type: Token type (always "bearer")
        expires_in: Token expiration time in seconds
        user: User information

    Example:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "id": 1,
                "email": "student@example.com",
                "role": "student"
            }
        }
    """
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    user: UserResponse


class TokenData(BaseModel):
    """
    Schema for data extracted from JWT tokens.

    Used internally for token validation and user identification.

    Attributes:
        user_id: User's unique identifier
        email: User's email address
        role: User's role
        exp: Token expiration timestamp
    """
    user_id: int
    email: EmailStr
    role: UserRole
    exp: Optional[datetime] = None


class RefreshTokenRequest(BaseModel):
    """
    Schema for refresh token requests.

    Attributes:
        refresh_token: The refresh token to exchange for a new access token

    Example:
        {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    refresh_token: str = Field(..., description="Refresh token")
