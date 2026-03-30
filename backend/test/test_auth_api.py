"""
Tests for Authentication API endpoints.

This module tests:
- User registration (signup)
- User login
- Token refresh
- Get current user profile
- Update user profile
- Password change functionality
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# ============================================================================
# User Registration Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.auth
class TestSignup:
    """Tests for POST /api/auth/signup endpoint."""

    def test_signup_success(self, client: TestClient, db_session: Session):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123!",
                "full_name": "New User",
                "role": "student"
            }
        )

        assert response.status_code == 201
        data = response.json()

        # Check response structure
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert "user" in data

        # Check user data
        user = data["user"]
        assert user["email"] == "newuser@example.com"
        assert user["full_name"] == "New User"
        assert user["role"] == "student"
        assert user["is_active"] is True
        assert "id" in user
        assert "created_at" in user

    def test_signup_duplicate_email(self, client: TestClient, authenticated_user):
        """Test registration with already registered email."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": authenticated_user.email,
                "password": "AnotherPass123!",
                "full_name": "Duplicate User",
                "role": "student"
            }
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_signup_invalid_email(self, client: TestClient):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "invalid-email",
                "password": "SecurePass123!",
                "full_name": "Invalid Email User",
                "role": "student"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_signup_weak_password(self, client: TestClient):
        """Test registration with weak password."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "weak@example.com",
                "password": "123",
                "full_name": "Weak Password User",
                "role": "student"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_signup_different_roles(self, client: TestClient):
        """Test registration with different user roles."""
        roles = ["student", "ta", "instructor"]

        for i, role in enumerate(roles):
            response = client.post(
                "/api/auth/signup",
                json={
                    "email": f"{role}{i}@example.com",
                    "password": "SecurePass123!",
                    "full_name": f"{role.title()} User",
                    "role": role
                }
            )

            assert response.status_code == 201
            assert response.json()["user"]["role"] == role

    def test_signup_missing_required_fields(self, client: TestClient):
        """Test registration with missing required fields."""
        # Missing password
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "missing@example.com",
                "full_name": "Missing Password",
                "role": "student"
            }
        )
        assert response.status_code == 422

        # Missing email
        response = client.post(
            "/api/auth/signup",
            json={
                "password": "SecurePass123!",
                "full_name": "Missing Email",
                "role": "student"
            }
        )
        assert response.status_code == 422


# ============================================================================
# User Login Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.auth
class TestLogin:
    """Tests for POST /api/auth/login endpoint."""

    def test_login_success(self, client: TestClient, create_test_user):
        """Test successful login."""
        # Create user first
        user = create_test_user(
            email="login@example.com",
            password="LoginPass123!"
        )

        response = client.post(
            "/api/auth/login",
            json={
                "email": "login@example.com",
                "password": "LoginPass123!"
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Check tokens
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

        # Check user data
        assert data["user"]["email"] == "login@example.com"
        assert data["user"]["id"] == user.id

    def test_login_invalid_email(self, client: TestClient):
        """Test login with non-existent email."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePass123!"
            }
        )

        assert response.status_code in [401, 403]
        assert "invalid" in response.json()["detail"].lower()

    def test_login_wrong_password(self, client: TestClient, create_test_user):
        """Test login with incorrect password."""
        create_test_user(
            email="wrongpass@example.com",
            password="CorrectPass123!"
        )

        response = client.post(
            "/api/auth/login",
            json={
                "email": "wrongpass@example.com",
                "password": "WrongPass123!"
            }
        )

        assert response.status_code in [401, 403]
        assert "invalid" in response.json()["detail"].lower()

    def test_login_inactive_user(self, client: TestClient, create_test_user):
        """Test login with inactive account."""
        create_test_user(
            email="inactive@example.com",
            password="InactivePass123!",
            is_active=False
        )

        response = client.post(
            "/api/auth/login",
            json={
                "email": "inactive@example.com",
                "password": "InactivePass123!"
            }
        )

        assert response.status_code == 403
        assert "inactive" in response.json()["detail"].lower()

    def test_login_missing_credentials(self, client: TestClient):
        """Test login with missing credentials."""
        # Missing password
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com"}
        )
        assert response.status_code == 422

        # Missing email
        response = client.post(
            "/api/auth/login",
            json={"password": "Pass123!"}
        )
        assert response.status_code == 422


# ============================================================================
# Token Refresh Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.auth
class TestRefreshToken:
    """Tests for POST /api/auth/refresh endpoint."""

    def test_refresh_token_success(self, client: TestClient, user_token):
        """Test successful token refresh."""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": user_token["refresh_token"]}
        )

        assert response.status_code == 200
        data = response.json()

        # Check new tokens are returned
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["access_token"] != user_token["access_token"]  # New token
        assert "user" in data

    def test_refresh_token_invalid(self, client: TestClient, invalid_token):
        """Test token refresh with invalid token."""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": invalid_token}
        )

        assert response.status_code in [401, 403]
        assert "invalid" in response.json()["detail"].lower()

    def test_refresh_token_missing(self, client: TestClient):
        """Test token refresh without providing token."""
        response = client.post(
            "/api/auth/refresh",
            json={}
        )

        assert response.status_code == 422


# ============================================================================
# Get Current User Profile Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.auth
class TestGetCurrentUser:
    """Tests for GET /api/auth/me endpoint."""

    def test_get_current_user_success(self, client: TestClient, authenticated_user, auth_headers):
        """Test retrieving current user profile."""
        response = client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert data["email"] == authenticated_user.email
        assert data["full_name"] == authenticated_user.full_name
        assert data["role"] == authenticated_user.role
        assert data["is_active"] is True

    def test_get_current_user_unauthorized(self, client: TestClient):
        """Test getting current user without authentication."""
        response = client.get("/api/auth/me")

        assert response.status_code in [401, 403]

    def test_get_current_user_invalid_token(self, client: TestClient, invalid_token):
        """Test getting current user with invalid token."""
        headers = {"Authorization": f"Bearer {invalid_token}"}
        response = client.get("/api/auth/me", headers=headers)

        assert response.status_code in [401, 403]


# ============================================================================
# Update User Profile Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.auth
class TestUpdateCurrentUser:
    """Tests for PUT /api/auth/me endpoint."""

    def test_update_full_name(self, client: TestClient, authenticated_user, auth_headers, db_session):
        """Test updating user's full name."""
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"full_name": "Updated Name"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"

        # Verify in database
        db_session.refresh(authenticated_user)
        assert authenticated_user.full_name == "Updated Name"

    def test_update_email(self, client: TestClient, authenticated_user, auth_headers, db_session):
        """Test updating user's email."""
        new_email = "newemail@example.com"

        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"email": new_email}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == new_email

        # Verify in database
        db_session.refresh(authenticated_user)
        assert authenticated_user.email == new_email

    def test_update_email_duplicate(self, client: TestClient, authenticated_user, create_test_user, auth_headers):
        """Test updating email to already existing email."""
        # Create another user
        other_user = create_test_user(email="other@example.com")

        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"email": other_user.email}
        )

        assert response.status_code == 400
        assert "already in use" in response.json()["detail"].lower()

    def test_update_password_success(self, client: TestClient, authenticated_user, auth_headers, db_session):
        """Test successful password update."""
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={
                "current_password": "TestPassword123!",
                "new_password": "NewPassword123!"
            }
        )

        assert response.status_code == 200

        # Verify new password works
        db_session.refresh(authenticated_user)
        assert authenticated_user.verify_password("NewPassword123!")
        assert not authenticated_user.verify_password("TestPassword123!")

    def test_update_password_wrong_current(self, client: TestClient, auth_headers):
        """Test password update with wrong current password."""
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={
                "current_password": "WrongPassword123!",
                "new_password": "NewPassword123!"
            }
        )

        assert response.status_code in [401, 403]
        assert "incorrect" in response.json()["detail"].lower()

    def test_update_password_missing_current(self, client: TestClient, auth_headers):
        """Test password update without providing current password."""
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={"new_password": "NewPassword123!"}
        )

        assert response.status_code == 400
        assert "current password" in response.json()["detail"].lower()

    def test_update_multiple_fields(self, client: TestClient, authenticated_user, auth_headers, db_session):
        """Test updating multiple fields at once."""
        response = client.put(
            "/api/auth/me",
            headers=auth_headers,
            json={
                "full_name": "Multiple Update",
                "email": "multiupdate@example.com"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Multiple Update"
        assert data["email"] == "multiupdate@example.com"

    def test_update_unauthorized(self, client: TestClient):
        """Test profile update without authentication."""
        response = client.put(
            "/api/auth/me",
            json={"full_name": "Unauthorized Update"}
        )

        assert response.status_code in [401, 403]


# ============================================================================
# Role-Based Access Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.auth
class TestRoleBasedAccess:
    """Tests for role-based access control."""

    def test_student_can_access_profile(self, client: TestClient, authenticated_user, auth_headers):
        """Test that student role can access their profile."""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["role"] == "student"

    def test_ta_can_access_profile(self, client: TestClient, authenticated_ta, ta_auth_headers):
        """Test that TA role can access their profile."""
        response = client.get("/api/auth/me", headers=ta_auth_headers)
        assert response.status_code == 200
        assert response.json()["role"] == "ta"

    def test_instructor_can_access_profile(self, client: TestClient, authenticated_instructor, instructor_auth_headers):
        """Test that instructor role can access their profile."""
        response = client.get("/api/auth/me", headers=instructor_auth_headers)
        assert response.status_code == 200
        assert response.json()["role"] == "instructor"

    def test_admin_can_access_profile(self, client: TestClient, authenticated_admin, admin_auth_headers):
        """Test that admin role can access their profile."""
        response = client.get("/api/auth/me", headers=admin_auth_headers)
        assert response.status_code == 200
        assert response.json()["role"] == "admin"
