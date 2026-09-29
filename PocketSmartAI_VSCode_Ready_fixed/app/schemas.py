from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: List[str] = Field(min_length=1, max_length=10)
    style: str = Field(default="Modern", min_length=2, max_length=80)
    city: str = Field(default="Coimbatore", min_length=2, max_length=80)
    notes: str = Field(default="", max_length=1500)


class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10_000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="", max_length=120)
    city: str = Field(default="Coimbatore", min_length=2, max_length=80)
    notes: str = Field(default="", max_length=1500)


class RecommendationItem(BaseModel):
    category: str = Field(min_length=1, max_length=120)
    name: str = Field(min_length=1, max_length=200)
    estimated_price: float = Field(ge=0)
    platform: str = Field(min_length=1, max_length=80)
    reason: str = Field(min_length=1, max_length=1000)
    search_url: str = Field(min_length=1, max_length=2000)


class RecommendationResponse(BaseModel):
    planner: str
    title: str
    budget: float
    allocation: Dict[str, float]
    summary: str
    recommendations: List[RecommendationItem]
    tips: List[str]
    disclaimer: str
    ai_generated: bool
    history_id: Optional[int] = None
