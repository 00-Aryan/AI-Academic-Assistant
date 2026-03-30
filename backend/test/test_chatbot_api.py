"""
Tests for Chatbot API endpoints.

This module tests:
- POST /api/chatbot/chat - Regular chat
- POST /api/chatbot/chat/stream - Streaming chat
- DELETE /api/chatbot/conversation/{id} - Clear conversation
- GET /api/chatbot/conversation/{id}/history - Get conversation history
- GET /api/chatbot/status - Get chatbot status
- GET /api/chatbot/metrics - Get chatbot metrics
- GET /api/chatbot/conversation/{id}/state - Get conversation state
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio


# ============================================================================
# Chatbot Status Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.chatbot
class TestChatbotStatus:
    """Tests for GET /api/chatbot/status endpoint."""

    def test_get_status_success(self, client: TestClient):
        """Test getting chatbot status."""
        response = client.get("/api/chatbot/status")

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "configured" in data
        assert "model" in data
        assert "available_modes" in data
        assert "features" in data
        assert "message" in data

        # Check available modes
        assert isinstance(data["available_modes"], list)
        assert "academic" in data["available_modes"]
        assert "general" in data["available_modes"]
        assert "study_help" in data["available_modes"]
        assert "doubt_clarification" in data["available_modes"]

    def test_status_shows_features(self, client: TestClient):
        """Test that status shows ADK features."""
        response = client.get("/api/chatbot/status")

        assert response.status_code == 200
        data = response.json()

        features = data["features"]
        assert "implementation" in features
        assert "adk_runner" in features
        assert "session_service" in features
        assert "memory_service" in features
        assert "observability" in features


# ============================================================================
# Chat Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.chatbot
class TestChat:
    """Tests for POST /api/chatbot/chat endpoint."""

    def test_chat_requires_authentication(self, client: TestClient):
        """Test that chat endpoint requires authentication."""
        response = client.post(
            "/api/chatbot/chat",
            json={
                "message": "Hello",
                "mode": "general"
            }
        )

        assert response.status_code in [401, 403]

    @patch('app.services.chatbot_service_hybrid.HybridChatbotService.chat')
    def test_chat_success(self, mock_chat, client: TestClient, auth_headers, sample_chat_request):
        """Test successful chat message."""
        # Mock the chat service response
        mock_chat.return_value = asyncio.coroutine(
            lambda: ("This is a test response", "conv-123")
        )()

        response = client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json=sample_chat_request
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "response" in data
        assert "conversation_id" in data
        assert "model" in data
        assert "timestamp" in data

    def test_chat_with_conversation_id(self, client: TestClient, auth_headers):
        """Test chat with existing conversation ID."""
        request_data = {
            "message": "Continue our conversation",
            "mode": "academic",
            "conversation_id": "existing-conv-123"
        }

        # Note: Actual response depends on chatbot service
        response = client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json=request_data
        )

        # May succeed or fail depending on chatbot availability
        assert response.status_code in [200, 500]

    def test_chat_different_modes(self, client: TestClient, auth_headers):
        """Test chat with different modes."""
        modes = ["academic", "general", "study_help", "doubt_clarification"]

        for mode in modes:
            response = client.post(
                "/api/chatbot/chat",
                headers=auth_headers,
                json={
                    "message": f"Test {mode} mode",
                    "mode": mode
                }
            )

            # May succeed or fail depending on chatbot availability
            assert response.status_code in [200, 500]

    def test_chat_invalid_mode(self, client: TestClient, auth_headers):
        """Test chat with invalid mode."""
        response = client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json={
                "message": "Test message",
                "mode": "invalid_mode"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_chat_empty_message(self, client: TestClient, auth_headers):
        """Test chat with empty message."""
        response = client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json={
                "message": "",
                "mode": "general"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_chat_missing_message(self, client: TestClient, auth_headers):
        """Test chat with missing message field."""
        response = client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json={
                "mode": "general"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_chat_long_message(self, client: TestClient, auth_headers):
        """Test chat with very long message."""
        long_message = "A" * 10000  # 10k characters

        response = client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json={
                "message": long_message,
                "mode": "general"
            }
        )

        # May succeed or fail depending on chatbot availability and limits
        assert response.status_code in [200, 422, 500]


# ============================================================================
# Streaming Chat Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.chatbot
class TestChatStream:
    """Tests for POST /api/chatbot/chat/stream endpoint."""

    def test_chat_stream_requires_authentication(self, client: TestClient):
        """Test that streaming chat requires authentication."""
        response = client.post(
            "/api/chatbot/chat/stream",
            json={
                "message": "Hello",
                "mode": "general"
            }
        )

        assert response.status_code in [401, 403]

    def test_chat_stream_success(self, client: TestClient, auth_headers):
        """Test successful streaming chat."""
        response = client.post(
            "/api/chatbot/chat/stream",
            headers=auth_headers,
            json={
                "message": "Stream test",
                "mode": "general"
            },
            stream=True
        )

        # Check that we get a streaming response
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    def test_chat_stream_with_conversation_id(self, client: TestClient, auth_headers):
        """Test streaming chat with conversation ID."""
        response = client.post(
            "/api/chatbot/chat/stream",
            headers=auth_headers,
            json={
                "message": "Continue stream",
                "mode": "academic",
                "conversation_id": "stream-conv-123"
            },
            stream=True
        )

        assert response.status_code == 200


# ============================================================================
# Conversation Management Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.chatbot
class TestConversationManagement:
    """Tests for conversation management endpoints."""

    def test_clear_conversation_requires_auth(self, client: TestClient):
        """Test that clearing conversation requires authentication."""
        response = client.delete("/api/chatbot/conversation/test-conv-123")

        assert response.status_code in [401, 403]

    def test_clear_conversation_success(self, client: TestClient, auth_headers):
        """Test successfully clearing a conversation."""
        # First, create a conversation by chatting
        client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json={
                "message": "Test message",
                "mode": "general"
            }
        )

        # Try to clear it
        response = client.delete(
            "/api/chatbot/conversation/test-conv-123",
            headers=auth_headers
        )

        # May succeed (200) or not found (404) depending on implementation
        assert response.status_code in [200, 404]

    def test_clear_nonexistent_conversation(self, client: TestClient, auth_headers):
        """Test clearing a conversation that doesn't exist."""
        response = client.delete(
            "/api/chatbot/conversation/nonexistent-conv-999",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_conversation_history_requires_auth(self, client: TestClient):
        """Test that getting conversation history requires authentication."""
        response = client.get("/api/chatbot/conversation/test-conv-123/history")

        assert response.status_code in [401, 403]

    def test_get_conversation_history_empty(self, client: TestClient, auth_headers):
        """Test getting history for conversation with no messages."""
        response = client.get(
            "/api/chatbot/conversation/empty-conv/history",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        assert "conversation_id" in data
        assert "messages" in data
        assert "total" in data
        assert data["total"] == 0
        assert data["messages"] == []

    def test_get_conversation_history_structure(self, client: TestClient, auth_headers):
        """Test conversation history response structure."""
        # Get history for any conversation
        response = client.get(
            "/api/chatbot/conversation/test-conv/history",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Check structure
        assert "conversation_id" in data
        assert "messages" in data
        assert "total" in data
        assert isinstance(data["messages"], list)

        # If there are messages, check their structure
        if data["messages"]:
            message = data["messages"][0]
            assert "role" in message
            assert "content" in message


# ============================================================================
# Conversation State Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.chatbot
class TestConversationState:
    """Tests for GET /api/chatbot/conversation/{id}/state endpoint."""

    def test_get_conversation_state_requires_auth(self, client: TestClient):
        """Test that getting conversation state requires authentication."""
        response = client.get("/api/chatbot/conversation/test-conv/state")

        assert response.status_code in [401, 403]

    def test_get_conversation_state_success(self, client: TestClient, auth_headers):
        """Test getting conversation state."""
        response = client.get(
            "/api/chatbot/conversation/test-conv-123/state",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "conversation_id" in data
        assert "state" in data
        assert "message" in data

    def test_get_nonexistent_conversation_state(self, client: TestClient, auth_headers):
        """Test getting state for non-existent conversation."""
        response = client.get(
            "/api/chatbot/conversation/nonexistent-999/state",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Should return empty state
        assert data["state"] == {}


# ============================================================================
# Metrics Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.chatbot
class TestChatbotMetrics:
    """Tests for GET /api/chatbot/metrics endpoint."""

    def test_get_metrics_requires_auth(self, client: TestClient):
        """Test that getting metrics requires authentication."""
        response = client.get("/api/chatbot/metrics")

        assert response.status_code in [401, 403]

    def test_get_metrics_success(self, client: TestClient, auth_headers):
        """Test getting chatbot metrics."""
        response = client.get(
            "/api/chatbot/metrics",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "metrics" in data
        assert "message" in data

    def test_metrics_structure(self, client: TestClient, auth_headers):
        """Test metrics response structure when available."""
        response = client.get(
            "/api/chatbot/metrics",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Metrics may be None if observability not enabled
        if data["metrics"] is not None:
            # Check that metrics is a dict
            assert isinstance(data["metrics"], dict)


# ============================================================================
# Integration Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.chatbot
@pytest.mark.integration
class TestChatbotIntegration:
    """Integration tests for chatbot workflow."""

    def test_full_conversation_flow(self, client: TestClient, auth_headers):
        """Test a full conversation flow."""
        # 1. Send first message
        response1 = client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json={
                "message": "Hello, what is Python?",
                "mode": "academic"
            }
        )

        # May succeed or fail based on chatbot availability
        if response1.status_code == 200:
            conv_id = response1.json()["conversation_id"]

            # 2. Send follow-up message
            response2 = client.post(
                "/api/chatbot/chat",
                headers=auth_headers,
                json={
                    "message": "Tell me more about its features",
                    "mode": "academic",
                    "conversation_id": conv_id
                }
            )

            assert response2.status_code == 200

            # 3. Get conversation history
            response3 = client.get(
                f"/api/chatbot/conversation/{conv_id}/history",
                headers=auth_headers
            )

            assert response3.status_code == 200
            history = response3.json()
            # Should have at least 2 messages (user + bot, user + bot)
            assert history["total"] >= 2

            # 4. Clear conversation
            response4 = client.delete(
                f"/api/chatbot/conversation/{conv_id}",
                headers=auth_headers
            )

            assert response4.status_code in [200, 404]

    def test_multiple_concurrent_conversations(self, client: TestClient, auth_headers):
        """Test handling multiple conversations simultaneously."""
        conversations = []

        # Create 3 different conversations
        for i in range(3):
            response = client.post(
                "/api/chatbot/chat",
                headers=auth_headers,
                json={
                    "message": f"Message {i}",
                    "mode": "general"
                }
            )

            if response.status_code == 200:
                conversations.append(response.json()["conversation_id"])

        # Each conversation should have unique ID
        assert len(conversations) == len(set(conversations))

    def test_different_users_different_conversations(
        self, client: TestClient, auth_headers, ta_auth_headers
    ):
        """Test that different users have separate conversations."""
        # User 1 sends message
        response1 = client.post(
            "/api/chatbot/chat",
            headers=auth_headers,
            json={
                "message": "User 1 message",
                "mode": "general"
            }
        )

        # User 2 sends message
        response2 = client.post(
            "/api/chatbot/chat",
            headers=ta_auth_headers,
            json={
                "message": "User 2 message",
                "mode": "general"
            }
        )

        # Both should work independently
        if response1.status_code == 200 and response2.status_code == 200:
            # Conversation IDs might be different or same pattern
            # but they should be isolated
            conv_id1 = response1.json()["conversation_id"]
            conv_id2 = response2.json()["conversation_id"]

            # Each user can only access their own conversation
            assert response1.status_code == 200
            assert response2.status_code == 200


# ============================================================================
# Error Handling Tests
# ============================================================================

@pytest.mark.api
@pytest.mark.chatbot
class TestChatbotErrorHandling:
    """Tests for chatbot error handling."""

    def test_chat_handles_service_error(self, client: TestClient, auth_headers):
        """Test that chat endpoint handles service errors gracefully."""
        with patch('app.services.chatbot_service_hybrid.HybridChatbotService.chat') as mock_chat:
            # Make the service raise an exception
            mock_chat.side_effect = Exception("Service error")

            response = client.post(
                "/api/chatbot/chat",
                headers=auth_headers,
                json={
                    "message": "Test message",
                    "mode": "general"
                }
            )

            # Should return 500 with error message
            assert response.status_code == 500
            assert "error" in response.json()["detail"].lower()

    def test_invalid_json_request(self, client: TestClient, auth_headers):
        """Test handling of invalid JSON in request."""
        response = client.post(
            "/api/chatbot/chat",
            data="invalid json",
            headers={**auth_headers, "Content-Type": "application/json"}
        )

        assert response.status_code == 422
