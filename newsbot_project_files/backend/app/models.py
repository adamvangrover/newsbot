from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from newsbot_project_files.backend.app.core.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    portfolio_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    assets = relationship("PortfolioAsset", back_populates="portfolio")

class PortfolioAsset(Base):
    __tablename__ = "portfolio_assets"

    portfolio_asset_id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.portfolio_id"), nullable=False)
    asset_id = Column(Integer, nullable=False) # In a real app, this would be a foreign key to an assets table
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    portfolio = relationship("Portfolio", back_populates="assets")
