"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Gaming tournament schemas

class Tournament(BaseModel):
    """
    Tournaments collection schema
    Collection name: "tournament"
    """
    title: str
    game: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    entry_fee_inr: int = Field(..., ge=0, description="Entry fee in INR")
    prize_pool_inr: int = Field(..., ge=0, description="Prize pool in INR")
    mode: str = Field("Online", description="Online or Offline")
    slots: int = Field(0, ge=0)
    region: Optional[str] = None
    featured: bool = False
    banner_url: Optional[str] = None

class Registration(BaseModel):
    """
    Registrations collection schema
    Collection name: "registration"
    """
    name: str
    email: EmailStr
    role: str = Field(..., description="player or organizer")
    team_name: Optional[str] = None
    tournament_id: Optional[str] = Field(None, description="Associated tournament ID")
    message: Optional[str] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
