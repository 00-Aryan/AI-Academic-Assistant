"""
Pytest integration tests for the SlidesService.

These tests verify the functionality of generating slides by making
live calls to the Google Gemini API.
"""

import pytest
import os
import sys

# Add the project's root directory (`backend`) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services import SlidesService, SlideTheme

# --- Test Configuration ---

# Mark all tests in this file for pytest.
# These tests will be skipped if the GOOGLE_API_KEY is not set.
pytestmark = [
    pytest.mark.integration,
    pytest.mark.slides,
    pytest.mark.skipif(not os.getenv("GOOGLE_API_KEY"), reason="GOOGLE_API_KEY not set in environment")
]


# --- Fixtures ---

@pytest.fixture(scope="function")
def slides_service() -> SlidesService:
    """Provides a new SlidesService instance for each test function."""
    service = SlidesService()
    if not service.llm:
        pytest.xfail("SlidesService LLM failed to initialize. Check GOOGLE_API_KEY and dependencies.")
    return service


# --- Test Class for SlidesService ---

@pytest.mark.asyncio
class TestSlidesService:
    """Groups tests for the SlidesService."""

    @pytest.mark.parametrize("theme", [SlideTheme.MINIMAL, SlideTheme.CORPORATE])
    async def test_generate_slides_success(self, slides_service: SlidesService, theme: SlideTheme):
        """
        Tests successful slide generation for different themes.
        Verifies the structure of the generated Markdown.
        """
        instructions = "Create a 3-slide presentation on the basics of FastAPI.\
            Include a title slide, one content slide about its key features,\
            and a summary slide."

        print(f"\n[TEST] Generating slides with theme '{theme.value}'...")
        markdown_output = await slides_service.generate_slides(
            instructions=instructions,
            theme=theme
        )

        # Assertions
        assert isinstance(markdown_output, str)
        assert "## Error" not in markdown_output, f"API returned an error: {markdown_output}"
        assert "---" in markdown_output, "Slide separator '---' must be present."
        assert markdown_output.strip().startswith("#"), "Output should start with a title slide (#)."
        assert "fastapi" in markdown_output.lower(), "The content should be about FastAPI."

        print(f"[SUCCESS] Slides for theme '{theme.value}' generated and validated.")
        print("========================================")
        print(markdown_output)
        print("========================================")