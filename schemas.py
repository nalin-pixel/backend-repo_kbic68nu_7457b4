"""
Database Schemas for the Techno Opera: Carthage

Each Pydantic model corresponds to a MongoDB collection (lowercased class name).
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class Subscriber(BaseModel):
    email: EmailStr = Field(..., description="Subscriber email address")
    name: Optional[str] = Field(None, description="Subscriber name")
    source: Optional[str] = Field(None, description="Where the subscriber came from (site, event, etc.)")


class Message(BaseModel):
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    subject: str = Field(..., description="Message subject")
    body: str = Field(..., description="Message body")


class Event(BaseModel):
    title: str = Field(..., description="Event title")
    date: datetime = Field(..., description="ISO date for the event")
    venue: str = Field(..., description="Venue name")
    location: str = Field(..., description="City, Country")
    url: Optional[str] = Field(None, description="Ticket or info URL")
    description: Optional[str] = Field(None, description="Short description of the event")


class TimelineEntry(BaseModel):
    year: str = Field(..., description="Era or year, e.g., '264 BCE' or 'Modern Day'")
    title: str = Field(..., description="Entry title")
    description: str = Field(..., description="Entry description")
    tags: Optional[List[str]] = Field(default=None, description="Keywords for filtering")

