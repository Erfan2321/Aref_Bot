from sqlalchemy.orm import Session
from db.models import UserProfile

PROFILE_FIELDS = {"firstname","lastname","phone","grade","field","city"}

def get_or_create_user(db: Session, telegram_id: int) -> UserProfile:
    obj = db.query(UserProfile).filter(UserProfile.telegram_id == telegram_id).one_or_none()
    if obj:
        return obj
    obj = UserProfile(telegram_id=telegram_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_user_field(db: Session, telegram_id: int, field: str, value: str) -> UserProfile:
    if field not in PROFILE_FIELDS:
        raise ValueError(f"Invalid field: {field}")
    obj = get_or_create_user(db, telegram_id)
    setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj
