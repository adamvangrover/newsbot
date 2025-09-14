from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from newsbot_project_files.backend.app import schemas, crud_portfolio, models
from newsbot_project_files.backend.app.core.database import get_db

router = APIRouter()

# Placeholder for getting the current user ID.
# In a real app, this would come from an authentication system.
def get_current_user_id() -> int:
    return 1 # Hardcoded for now

@router.post("/", response_model=schemas.Portfolio)
def create_portfolio(
    portfolio: schemas.PortfolioCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return crud_portfolio.create_portfolio(db=db, portfolio=portfolio, user_id=user_id)

@router.get("/", response_model=List[schemas.Portfolio])
def read_portfolios(
    user_id: int = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    portfolios = crud_portfolio.get_portfolios_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return portfolios

@router.get("/{portfolio_id}", response_model=schemas.Portfolio)
def read_portfolio(
    portfolio_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    db_portfolio = crud_portfolio.get_portfolio(db, portfolio_id=portfolio_id)
    if db_portfolio is None or db_portfolio.user_id != user_id:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_portfolio

@router.put("/{portfolio_id}", response_model=schemas.Portfolio)
def update_portfolio(
    portfolio_id: int,
    portfolio: schemas.PortfolioCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    db_portfolio = crud_portfolio.get_portfolio(db, portfolio_id=portfolio_id)
    if db_portfolio is None or db_portfolio.user_id != user_id:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return crud_portfolio.update_portfolio(db=db, portfolio_id=portfolio_id, portfolio=portfolio)

@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(
    portfolio_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    db_portfolio = crud_portfolio.get_portfolio(db, portfolio_id=portfolio_id)
    if db_portfolio is None or db_portfolio.user_id != user_id:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    crud_portfolio.delete_portfolio(db=db, portfolio_id=portfolio_id)
    return

@router.post("/{portfolio_id}/assets", response_model=schemas.Portfolio)
def add_asset_to_portfolio(
    portfolio_id: int,
    asset: schemas.PortfolioAssetCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    db_portfolio = crud_portfolio.get_portfolio(db, portfolio_id=portfolio_id)
    if db_portfolio is None or db_portfolio.user_id != user_id:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    crud_portfolio.add_asset_to_portfolio(db=db, portfolio_id=portfolio_id, asset=asset)
    return crud_portfolio.get_portfolio(db, portfolio_id=portfolio_id)

@router.delete("/{portfolio_id}/assets/{asset_id}", status_code=204)
def remove_asset_from_portfolio(
    portfolio_id: int,
    asset_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    db_portfolio = crud_portfolio.get_portfolio(db, portfolio_id=portfolio_id)
    if db_portfolio is None or db_portfolio.user_id != user_id:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    crud_portfolio.remove_asset_from_portfolio(db=db, portfolio_id=portfolio_id, asset_id=asset_id)
    return
