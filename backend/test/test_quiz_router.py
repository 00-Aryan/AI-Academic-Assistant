"""
API tests for the Quiz and Quiz Attempt endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import AsyncMock

from app.models.user import User
from app.models.course import Course
from app.models.quiz import Quiz

# Mark all tests in this file
pytestmark = [pytest.mark.api, pytest.mark.quiz]

# Sample AI-generated quiz data for mocking
MOCK_QUIZ_QUESTIONS = {
    "questions": [
        {
            "question_text": "What is Python?",
            "question_type": "mcq",
            "options": ["A snake", "A programming language", "A car", "A fruit"],
            "correct_answers": ["A programming language"],
            "explanation": "Python is a high-level, interpreted, general-purpose programming language.",
            "marks": 5,
        },
        {
            "question_text": "Which of the following are Python data types?",
            "question_type": "msq",
            "options": ["str", "int", "list", "vector"],
            "correct_answers": ["str", "int", "list"],
            "explanation": "str, int, and list are built-in Python data types. vector is not.",
            "marks": 10,
        },
    ]
}


@pytest.fixture
def test_quiz(db_session: Session, test_course: Course, authenticated_ta: User) -> Quiz:
    """Creates a sample quiz in the database for testing."""
    quiz = Quiz(
        title="Sample Test Quiz",
        description="A quiz created for testing.",
        course_id=test_course.id,
        created_by_id=authenticated_ta.id,
        questions=MOCK_QUIZ_QUESTIONS,
    )
    db_session.add(quiz)
    db_session.commit()
    db_session.refresh(quiz)
    return quiz


@pytest.mark.asyncio
async def test_generate_quiz_as_ta(
    client: TestClient, ta_auth_headers: dict, test_course: Course, monkeypatch
):
    """Tests that a TA can successfully generate and save a quiz."""
    # Mock the AI service call
    mock_generate = AsyncMock(return_value=MOCK_QUIZ_QUESTIONS) 
    monkeypatch.setattr("app.api.quiz_router.quiz_service.generate_quiz", mock_generate)

    request_data = {
        "course_id": test_course.id,
        "title": "New AI-Generated Quiz",
        "topics": ["Python basics"],
        "difficulty": "Easy",
        "marks_per_question": 5,
        "num_questions": 2,
    }

    response = client.post("/api/quizzes/generate", headers=ta_auth_headers, json=request_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New AI-Generated Quiz"
    assert data["course_id"] == test_course.id
    assert data["questions"] == MOCK_QUIZ_QUESTIONS
    mock_generate.assert_called_once()


@pytest.mark.asyncio
async def test_generate_quiz_as_student(client: TestClient, auth_headers: dict, test_course: Course):
    """Tests that a student cannot generate a quiz."""
    request_data = {
        "course_id": test_course.id,
        "title": "Student Quiz Attempt",
        "topics": ["Python basics"],
        "difficulty": "Easy",
        "marks_per_question": 5,
        "num_questions": 2,
    }
    response = client.post("/api/quizzes/generate", headers=auth_headers, json=request_data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_quiz_as_creator(
    client: TestClient, ta_auth_headers: dict, test_quiz: Quiz, monkeypatch
):
    """Tests that the creator of a quiz can update it."""
    mock_update = AsyncMock(return_value={"questions": [{"updated": True}]})
    monkeypatch.setattr("app.api.quiz_router.quiz_service.update_quiz", mock_update)

    response = client.put(
        f"/api/quizzes/{test_quiz.id}",
        headers=ta_auth_headers,
        json={"feedback": "Make it better"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["questions"] == {"questions": [{"updated": True}]}
    mock_update.assert_called_once()


@pytest.mark.asyncio
async def test_update_quiz_as_other_ta(
    client: TestClient, admin_auth_headers: dict, test_quiz: Quiz
):
    """Tests that another TA/Admin cannot update a quiz they did not create."""
    response = client.put(
        f"/api/quizzes/{test_quiz.id}",
        headers=admin_auth_headers,
        json={"feedback": "I want to change this"},
    )
    assert response.status_code == 403
    assert "You can only update quizzes you have created" in response.json()["detail"]


def test_get_all_quizzes(client: TestClient, auth_headers: dict, test_quiz: Quiz):
    """Tests that an authenticated user can list quizzes."""
    response = client.get("/api/quizzes/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(q["id"] == test_quiz.id for q in data)


def test_get_quiz_by_id(client: TestClient, auth_headers: dict, test_quiz: Quiz):
    """Tests retrieving a single quiz by its ID."""
    response = client.get(f"/api/quizzes/{test_quiz.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_quiz.id
    assert data["title"] == test_quiz.title
    # Ensure sensitive parts of questions (correct_answers, explanation) are returned
    # This is a design choice. If they should be hidden, this test would change.
    assert "correct_answers" in data["questions"]["questions"][0]


def test_submit_quiz_attempt_correct(
    client: TestClient, auth_headers: dict, test_quiz: Quiz, db_session: Session
):
    """Tests submitting a quiz attempt with all correct answers."""
    attempt_data = [
        {"question_index": 0, "selected_options": ["A programming language"]},
        {"question_index": 1, "selected_options": ["str", "int", "list"]},
    ]
    response = client.post(
        f"/api/quizzes/{test_quiz.id}/attempt", headers=auth_headers, json=attempt_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 15  # 5 + 10
    assert data["total_marks"] == 15
    assert data["user"]["email"] is not None


def test_submit_quiz_attempt_partially_correct(
    client: TestClient, auth_headers: dict, test_quiz: Quiz
):
    """Tests submitting a quiz attempt with one correct and one incorrect answer."""
    attempt_data = [
        {"question_index": 0, "selected_options": ["A programming language"]},  # Correct
        {"question_index": 1, "selected_options": ["str", "int"]},  # Incorrect (incomplete)
    ]
    response = client.post(
        f"/api/quizzes/{test_quiz.id}/attempt", headers=auth_headers, json=attempt_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 5  # Only marks for the first question, second is incorrect
    assert data["total_marks"] == 15


def test_delete_quiz_as_creator(client: TestClient, ta_auth_headers: dict, test_quiz: Quiz):
    """Tests that the creator can delete their own quiz."""
    response = client.delete(f"/api/quizzes/{test_quiz.id}", headers=ta_auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/api/quizzes/{test_quiz.id}", headers=ta_auth_headers)
    assert get_response.status_code == 404


def test_delete_quiz_as_other_user(
    client: TestClient, admin_auth_headers: dict, test_quiz: Quiz
):
    """Tests that a user who is not the creator cannot delete the quiz."""
    response = client.delete(f"/api/quizzes/{test_quiz.id}", headers=admin_auth_headers)
    assert response.status_code == 403
    assert "You can only delete quizzes you have created" in response.json()["detail"]


def test_get_quiz_attempts_for_quiz(
    client: TestClient, ta_auth_headers: dict, test_quiz: Quiz
):
    """
    Tests retrieving all attempts for a specific quiz.
    (This endpoint is not yet implemented, so this is a placeholder)
    """
    # To implement this test, you would first create an attempt,
    # then call an endpoint like GET /api/quizzes/{quiz_id}/attempts
    # and assert the attempt is in the response.
    pass