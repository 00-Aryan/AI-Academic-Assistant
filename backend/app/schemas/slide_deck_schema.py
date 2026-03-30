"""
Pydantic schemas for Slide Deck operations.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

from app.schemas.user_schema import UserSimpleResponse


class GraphType(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"


class AxisMetadata(BaseModel):
    """Metadata for graph axis."""
    label: str = Field(description="Name of the axis (e.g., 'Time', 'Revenue')")
    unit: Optional[str] = Field(None, description="Unit of measurement (e.g., '$', 'years', 'percentage')")
    min_value: Optional[float] = Field(None, description="Minimum value on axis")
    max_value: Optional[float] = Field(None, description="Maximum value on axis")


class GraphData(BaseModel):
    """Enhanced graph data with metadata for better visualization."""
    type: GraphType = Field(description="Type of chart")
    title: str = Field(description="Title of the graph")
    labels: List[str] = Field(description="Data labels/categories")
    datasets: List[Dict[str, Any]] = Field(description="Data values e.g., [{'label': 'Data', 'data': [1,2,3]}]")
    x_axis: Optional[AxisMetadata] = Field(None, description="X-axis metadata with label and unit")
    y_axis: Optional[AxisMetadata] = Field(None, description="Y-axis metadata with label and unit")
    data_description: Optional[str] = Field(None, description="Brief description of what the data represents")
    data_source: Optional[str] = Field(None, description="Source or generation method of the data")


class Slide(BaseModel):
    """Represents a single slide with a title and markdown content."""
    title: str = Field(..., min_length=3, max_length=150, description="The title of the slide (max 150 chars for 16:9 display).")
    content: str = Field(..., min_length=10, max_length=2000, description="The markdown content of the slide (max 2000 chars for readability).")
    graph_data: Optional[GraphData] = Field(None, description="Optional graph data for the slide.")
    graph_image: Optional[str] = Field(None, description="Optional base64 Data URI of chart image (PNG).")
    content_metrics: Optional[Dict[str, Any]] = Field(None, description="Content statistics (word count, etc.)")


class SlideDeckBase(BaseModel):
    """Base schema for slide deck attributes."""
    title: str = Field(..., min_length=3, max_length=100, description="Title of the slide deck.")
    description: Optional[str] = Field(None, max_length=500, description="A brief description of the slide deck.")


class SlideDeckGenerationRequest(SlideDeckBase):
    """Schema for requesting AI-powered slide deck generation."""
    course_id: int = Field(..., description="The ID of the course this deck belongs to.")
    topics: List[str] = Field(..., description="A list of topics to be covered in the slides.")
    num_slides: int = Field(..., gt=0, le=20, description="Number of slides to generate.")
    format: str = Field("presentation", description="Format: 'presentation' or 'document' affecting content length.")
    include_graphs: bool = Field(False, description="Whether to include graphs in slides.")
    graph_types: Optional[List[GraphType]] = Field(None, description="Types of graphs to include if include_graphs is True.")


class SlideDeckPreview(BaseModel):
    """Preview of the slide deck before generation."""
    outline: List[str] = Field(..., description="Bullet points outlining what the slides will contain.")


class SlideDeckUpdateRequest(BaseModel):
    """Schema for updating an existing slide deck."""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    slides: Optional[List[Slide]] = Field(None, description="The complete, updated list of slides.")


class SlideDeckResponse(SlideDeckBase):
    """Schema for returning a slide deck in an API response."""
    id: int
    course_id: int
    slides: List[Slide]
    created_at: datetime
    updated_at: Optional[datetime] = None
    creator: UserSimpleResponse

    class Config:
        from_attributes = True


class SlideDeckRefineRequest(BaseModel):
    """Schema for requesting AI-powered refinement of existing slides."""
    feedback: str = Field(..., description="Detailed feedback or instructions for refining the slides.")
