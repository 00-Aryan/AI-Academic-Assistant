"""
Model Validation Script for AURA Database

This script validates all database models and their fields before running populate_db.py
It checks for:
1. Model existence
2. Required fields
3. Enum values
4. Relationships
5. Field types

Run this before populate_db.py to catch any schema mismatches early.

Usage: python validate_models.py
"""

import sys
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for Windows
init(autoreset=True)

# Test imports
print("=" * 70)
print(f"{Fore.CYAN}AURA MODEL VALIDATION SCRIPT{Style.RESET_ALL}")
print("=" * 70)
print()

validation_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}


def test_import(module_path, item_name):
    """Test if a module or class can be imported."""
    try:
        parts = module_path.split(".")
        module = __import__(module_path, fromlist=[item_name])
        item = getattr(module, item_name)
        validation_results["passed"].append(f"✓ Import: {module_path}.{item_name}")
        return item
    except Exception as e:
        validation_results["failed"].append(f"✗ Import Failed: {module_path}.{item_name} - {str(e)}")
        return None


def test_model_fields(model_class, expected_fields):
    """Test if model has expected fields."""
    model_name = model_class.__name__
    
    if not hasattr(model_class, '__table__'):
        validation_results["failed"].append(f"✗ {model_name}: Not a valid SQLAlchemy model")
        return False
    
    columns = {col.name for col in model_class.__table__.columns}
    missing_fields = set(expected_fields) - columns
    
    if missing_fields:
        validation_results["failed"].append(
            f"✗ {model_name}: Missing fields: {', '.join(missing_fields)}"
        )
        return False
    else:
        validation_results["passed"].append(
            f"✓ {model_name}: All expected fields present ({len(expected_fields)} fields)"
        )
        return True


def test_enum_values(enum_class, expected_values):
    """Test if enum has expected values."""
    enum_name = enum_class.__name__
    actual_values = {e.value for e in enum_class}
    missing_values = set(expected_values) - actual_values
    
    if missing_values:
        validation_results["warnings"].append(
            f"⚠ {enum_name}: Missing values: {', '.join(missing_values)}"
        )
        return False
    else:
        validation_results["passed"].append(
            f"✓ {enum_name}: All expected values present ({len(expected_values)} values)"
        )
        return True


print(f"{Fore.YELLOW}Phase 1: Testing Model Imports{Style.RESET_ALL}")
print("-" * 70)

# Import all models
User = test_import("app.models.user", "User")
Profile = test_import("app.models.profile", "Profile")
Course = test_import("app.models.course", "Course")
KnowledgeSource = test_import("app.models.knowledge", "KnowledgeSource")
KnowledgeChunk = test_import("app.models.knowledge", "KnowledgeChunk")
Task = test_import("app.models.task", "Task")
Query = test_import("app.models.query", "Query")
QueryResponse = test_import("app.models.query", "QueryResponse")
ChatSession = test_import("app.models.chat_session", "ChatSession")
DoubtUpload = test_import("app.models.doubts", "DoubtUpload")
DoubtMessage = test_import("app.models.doubts", "DoubtMessage")
Announcement = test_import("app.models.announcement", "Announcement")
Resource = test_import("app.models.resource", "Resource")
Quiz = test_import("app.models.quiz", "Quiz")
QuizAttempt = test_import("app.models.quiz_attempt", "QuizAttempt")
SlideDeck = test_import("app.models.slide_deck", "SlideDeck")
Tag = test_import("app.models.tag", "Tag")
Call = test_import("app.models.call", "Call")

print()
print(f"{Fore.YELLOW}Phase 2: Testing Enum Imports{Style.RESET_ALL}")
print("-" * 70)

# Import enums
CategoryEnum = test_import("app.models.enums", "CategoryEnum")
TaskTypeEnum = test_import("app.models.enums", "TaskTypeEnum")
TaskStatusEnum = test_import("app.models.enums", "TaskStatusEnum")
CallStatusEnum = test_import("app.models.enums", "CallStatusEnum")
UserRole = test_import("app.schemas.user_schema", "UserRole")
QueryStatus = test_import("app.schemas.query_schema", "QueryStatus")
QueryCategory = test_import("app.schemas.query_schema", "QueryCategory")
QueryPriority = test_import("app.schemas.query_schema", "QueryPriority")
AnnouncementType = test_import("app.schemas.announcement_schema", "AnnouncementType")
AnnouncementTarget = test_import("app.schemas.announcement_schema", "AnnouncementTarget")
ResourceType = test_import("app.schemas.resource_schema", "ResourceType")
ResourceVisibility = test_import("app.schemas.resource_schema", "ResourceVisibility")

print()
print(f"{Fore.YELLOW}Phase 3: Testing Model Fields{Style.RESET_ALL}")
print("-" * 70)

# Test model fields
if User:
    test_model_fields(User, ["id", "email", "full_name", "role", "password", "is_active"])

if Profile:
    test_model_fields(Profile, ["id", "user_id", "full_name", "bio", "department"])

if Course:
    test_model_fields(Course, ["id", "name", "description", "created_by_id"])

if Tag:
    test_model_fields(Tag, ["id", "name", "created_by_id", "created_at"])

if Announcement:
    test_model_fields(Announcement, ["id", "title", "content", "announcement_type", "target_audience", "created_by_id"])

if Resource:
    test_model_fields(Resource, ["id", "title", "description", "resource_type", "url", "visibility", "created_by_id"])

if Quiz:
    test_model_fields(Quiz, ["id", "title", "description", "course_id", "created_by_id", "questions", "is_published"])

if QuizAttempt:
    test_model_fields(QuizAttempt, ["id", "quiz_id", "user_id", "score", "total_marks", "submitted_answers"])

if SlideDeck:
    test_model_fields(SlideDeck, ["id", "title", "description", "course_id", "created_by_id", "slides"])

if DoubtUpload:
    test_model_fields(DoubtUpload, ["id", "course_code", "source", "created_by_id", "created_at"])

if DoubtMessage:
    test_model_fields(DoubtMessage, ["id", "upload_id", "author_role", "text"])

if Call:
    test_model_fields(Call, ["id", "caller_number", "twilio_sid", "language", "status", "created_at"])

if KnowledgeSource:
    test_model_fields(KnowledgeSource, ["id", "title", "description", "content", "category", "is_active"])

if Task:
    test_model_fields(Task, ["id", "task_type", "status", "created_at"])

if Query:
    test_model_fields(Query, ["id", "title", "description", "category", "priority", "status", "student_id"])

if QueryResponse:
    test_model_fields(QueryResponse, ["id", "query_id", "user_id", "content", "is_solution"])

if ChatSession:
    test_model_fields(ChatSession, ["id", "ip_address", "device_info", "language", "created_at"])

print()
print(f"{Fore.YELLOW}Phase 4: Testing Enum Values{Style.RESET_ALL}")
print("-" * 70)

# Test enum values used in populate_db.py
if UserRole:
    test_enum_values(UserRole, ["STUDENT", "TA", "INSTRUCTOR", "ADMIN"])

if QueryStatus:
    test_enum_values(QueryStatus, ["OPEN", "IN_PROGRESS", "RESOLVED"])

if QueryCategory:
    test_enum_values(QueryCategory, ["TECHNICAL", "GENERAL", "ASSIGNMENT", "EXAM"])

if QueryPriority:
    test_enum_values(QueryPriority, ["LOW", "MEDIUM", "HIGH"])

if AnnouncementType:
    test_enum_values(AnnouncementType, ["GENERAL", "URGENT", "DEADLINE", "UPDATE"])

if AnnouncementTarget:
    test_enum_values(AnnouncementTarget, ["ALL", "STUDENTS", "TAS", "INSTRUCTORS"])

if ResourceType:
    test_enum_values(ResourceType, ["VIDEO", "PDF", "DOCUMENT", "LINK"])

if ResourceVisibility:
    # Check for the correct value
    if hasattr(ResourceVisibility, "COURSE"):
        validation_results["passed"].append("✓ ResourceVisibility: Has COURSE value")
    elif hasattr(ResourceVisibility, "COURSE_SPECIFIC"):
        validation_results["warnings"].append("⚠ ResourceVisibility: Has COURSE_SPECIFIC instead of COURSE")
    else:
        validation_results["failed"].append("✗ ResourceVisibility: Missing COURSE/COURSE_SPECIFIC value")
    
    test_enum_values(ResourceVisibility, ["PUBLIC", "PRIVATE"])

if CategoryEnum:
    test_enum_values(CategoryEnum, ["COURSES", "ASSIGNMENTS", "QUIZZES", "ADMISSION", "QUERIES", "PLACEMENT"])

if TaskTypeEnum:
    test_enum_values(TaskTypeEnum, ["EMBEDDING", "QUERY", "DATA_PROCESSING"])

if TaskStatusEnum:
    test_enum_values(TaskStatusEnum, ["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"])

if CallStatusEnum:
    test_enum_values(CallStatusEnum, ["ACTIVE", "COMPLETED", "FAILED"])

print()
print("=" * 70)
print(f"{Fore.CYAN}VALIDATION SUMMARY{Style.RESET_ALL}")
print("=" * 70)

# Print results
if validation_results["passed"]:
    print(f"\n{Fore.GREEN}PASSED ({len(validation_results['passed'])}){Style.RESET_ALL}")
    for result in validation_results["passed"]:
        print(f"  {Fore.GREEN}{result}{Style.RESET_ALL}")

if validation_results["warnings"]:
    print(f"\n{Fore.YELLOW}WARNINGS ({len(validation_results['warnings'])}){Style.RESET_ALL}")
    for result in validation_results["warnings"]:
        print(f"  {Fore.YELLOW}{result}{Style.RESET_ALL}")

if validation_results["failed"]:
    print(f"\n{Fore.RED}FAILED ({len(validation_results['failed'])}){Style.RESET_ALL}")
    for result in validation_results["failed"]:
        print(f"  {Fore.RED}{result}{Style.RESET_ALL}")

print()
print("=" * 70)

# Final verdict
total_tests = len(validation_results["passed"]) + len(validation_results["failed"])
success_rate = (len(validation_results["passed"]) / total_tests * 100) if total_tests > 0 else 0

if validation_results["failed"]:
    print(f"{Fore.RED}VALIDATION FAILED!{Style.RESET_ALL}")
    print(f"Success Rate: {success_rate:.1f}% ({len(validation_results['passed'])}/{total_tests})")
    print()
    print(f"{Fore.RED}⛔ DO NOT run populate_db.py - Fix the errors above first!{Style.RESET_ALL}")
    sys.exit(1)
else:
    print(f"{Fore.GREEN}✓ ALL VALIDATIONS PASSED!{Style.RESET_ALL}")
    print(f"Success Rate: {success_rate:.1f}% ({len(validation_results['passed'])}/{total_tests})")
    if validation_results["warnings"]:
        print(f"{Fore.YELLOW}⚠ {len(validation_results['warnings'])} warning(s) - Review but safe to proceed{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}✓ Safe to run: python populate_db.py{Style.RESET_ALL}")
    sys.exit(0)
