from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Listing, User
from app.auth import get_current_user # Use whatever your auth dependency is named

router = APIRouter()

@router.post("/listings/{listing_id}/sell")
def sell_listing(
    listing_id: int, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    listing = session.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    if listing.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to sell this listing")
    
    if listing.status == "sold":
        raise HTTPException(status_code=400, detail="Listing is already sold")
    
    listing.status = "sold"
    session.add(listing)
    session.commit()
    
    return {"message": "listing removed from customer"}