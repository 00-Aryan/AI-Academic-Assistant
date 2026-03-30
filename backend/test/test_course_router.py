"""
API tests for the Course CRUD endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course_schema import CourseCreate

# Mark all tests in this file as 'api' and 'course' tests
pytestmark = [pytest.mark.api, pytest.mark.course]


def test_create_course_as_admin(
    client: TestClient, admin_auth_headers: dict, db_session: Session
):
    """
    Tests that an admin can successfully create a new course.
    """
    response = client.post(
        "/api/courses/",
        headers=admin_auth_headers,
        json={"name": "New Admin Course", "description": "A course by an admin."},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Admin Course"
    assert data["creator"]["email"] is not None

    # Verify it's in the database
    course = db_session.query(Course).filter(Course.id == data["id"]).first()
    assert course is not None
    assert course.name == "New Admin Course"


def test_create_course_as_student(
    client: TestClient, auth_headers: dict
):
    """
    Tests that a non-admin user (student) cannot create a course.
    """
    response = client.post(
        "/api/courses/",
        headers=auth_headers,
        json={"name": "Student Course Attempt", "description": "This should fail."},
    )
    assert response.status_code == 403  # Forbidden
    assert "Access denied" in response.json()["detail"]


def test_create_course_duplicate_name(
    client: TestClient, admin_auth_headers: dict, test_course: Course
):
    """
    Tests that creating a course with a name that already exists fails.
    """
    response = client.post(
        "/api/courses/",
        headers=admin_auth_headers,
        json={"name": test_course.name, "description": "A duplicate course."},
    )
    assert response.status_code == 409  # Conflict
    assert "course with this name already exists" in response.json()["detail"]


def test_get_all_courses(
    client: TestClient, auth_headers: dict, test_course: Course
):
    """
    Tests that any authenticated user can retrieve a list of all courses.
    """
    response = client.get("/api/courses/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check if the test_course is in the response list
    assert any(c["id"] == test_course.id for c in data)


def test_get_course_by_id(
    client: TestClient, auth_headers: dict, test_course: Course
):
    """
    Tests successful retrieval of a single course by its ID.
    """
    response = client.get(f"/api/courses/{test_course.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_course.id
    assert data["name"] == test_course.name


def test_get_course_by_id_not_found(
    client: TestClient, auth_headers: dict
):
    """
    Tests that requesting a non-existent course ID returns a 404 error.
    """
    response = client.get("/api/courses/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_course_as_admin(
    client: TestClient, admin_auth_headers: dict, test_course: Course
):
    """
    Tests that an admin can successfully update an existing course.
    """
    updated_name = "Updated Course Name"
    response = client.put(
        f"/api/courses/{test_course.id}",
        headers=admin_auth_headers,
        json={"name": updated_name},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_course.id
    assert data["name"] == updated_name
    assert data["description"] == test_course.description  # Description should be unchanged


def test_update_course_as_student(
    client: TestClient, auth_headers: dict, test_course: Course
):
    """
    Tests that a non-admin user cannot update a course.
    """
    response = client.put(
        f"/api/courses/{test_course.id}",
        headers=auth_headers,
        json={"name": "Student Update Attempt"},
    )
    assert response.status_code == 403  # Forbidden


def test_update_course_to_duplicate_name_fails(
    client: TestClient, admin_auth_headers: dict, db_session: Session, test_course: Course
):
    """
    Tests that updating a course name to an existing name of another course fails.
    The current implementation will likely raise a 500 error instead of a 409.
    """
    # Create a second course
    course2 = Course(
        name="Second Course Name", description="Another course.", created_by_id=test_course.created_by_id
    )
    db_session.add(course2)
    db_session.commit()

    # Try to update test_course to have the same name as course2
    response = client.put(
        f"/api/courses/{test_course.id}",
        headers=admin_auth_headers,
        json={"name": course2.name},
    )

    # This assertion is expected to fail. The API should return 409, but it will likely return 500.
    assert response.status_code == 409, f"API returned {response.status_code} instead of 409. Body: {response.text}"
    assert "course with this name already exists" in response.json()["detail"]


def test_delete_course_as_admin(
    client: TestClient, admin_auth_headers: dict, db_session: Session
):
    """
    Tests that an admin can successfully delete a course.
    """
    # Create a course to delete
    course_to_delete = Course(
        name="Course to be Deleted", description="temp", created_by_id=1
    )
    db_session.add(course_to_delete)
    db_session.commit()
    db_session.refresh(course_to_delete)
    course_id = course_to_delete.id

    # Delete it
    response = client.delete(f"/api/courses/{course_id}", headers=admin_auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    deleted_course = db_session.query(Course).filter(Course.id == course_id).first()
    assert deleted_course is None

    # Verify getting it by ID now fails
    get_response = client.get(f"/api/courses/{course_id}", headers=admin_auth_headers)
    assert get_response.status_code == 404


def test_delete_course_as_student(
    client: TestClient, auth_headers: dict, test_course: Course
):
    """
    Tests that a non-admin user cannot delete a course.
    """
    response = client.delete(
        f"/api/courses/{test_course.id}", headers=auth_headers
    )
    assert response.status_code == 403  # Forbidden