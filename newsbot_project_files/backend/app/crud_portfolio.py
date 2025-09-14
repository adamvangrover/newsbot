from sqlalchemy.orm import Session
from . import models, schemas

def get_portfolio(db: Session, portfolio_id: int):
    return db.query(models.Portfolio).filter(models.Portfolio.portfolio_id == portfolio_id).first()

def get_portfolios_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Portfolio).filter(models.Portfolio.user_id == user_id).offset(skip).limit(limit).all()

def create_portfolio(db: Session, portfolio: schemas.PortfolioCreate, user_id: int):
    db_portfolio = models.Portfolio(**portfolio.dict(), user_id=user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def update_portfolio(db: Session, portfolio_id: int, portfolio: schemas.PortfolioCreate):
    db_portfolio = get_portfolio(db, portfolio_id)
    if db_portfolio:
        for key, value in portfolio.dict().items():
            setattr(db_portfolio, key, value)
        db.commit()
        db.refresh(db_portfolio)
    return db_portfolio

def delete_portfolio(db: Session, portfolio_id: int):
    db_portfolio = get_portfolio(db, portfolio_id)
    if db_portfolio:
        db.delete(db_portfolio)
        db.commit()
    return db_portfolio

def add_asset_to_portfolio(db: Session, portfolio_id: int, asset: schemas.PortfolioAssetCreate):
    db_asset = models.PortfolioAsset(**asset.dict(), portfolio_id=portfolio_id)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def remove_asset_from_portfolio(db: Session, portfolio_id: int, asset_id: int):
    db_asset = db.query(models.PortfolioAsset).filter(models.PortfolioAsset.portfolio_id == portfolio_id, models.PortfolioAsset.asset_id == asset_id).first()
    if db_asset:
        db.delete(db_asset)
        db.commit()
    return
