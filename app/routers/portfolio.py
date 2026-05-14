from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PortfolioResponse
from app.auth import get_current_user
from app.models import User
from app.crud import get_portfolio_summary

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/", response_model=PortfolioResponse)
def get_portfolio(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_portfolio_summary(db, current_user.id)