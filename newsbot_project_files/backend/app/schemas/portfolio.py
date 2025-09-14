from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Portfolio Asset Schemas ---

class PortfolioAssetBase(BaseModel):
    asset_id: int

class PortfolioAssetCreate(PortfolioAssetBase):
    pass

class PortfolioAsset(PortfolioAssetBase):
    id: int
    portfolio_id: int
    added_at: datetime

    class Config:
        orm_mode = True

# --- Portfolio Schemas ---

class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    user_id: int # In a real app, this might be a User schema
    assets: List[PortfolioAsset] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
