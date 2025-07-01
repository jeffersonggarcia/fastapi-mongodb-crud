from bson import ObjectId
from datetime import datetime

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "birth_date": user["birth_date"].isoformat() if isinstance(user["birth_date"], datetime) else str(user["birth_date"]),
        "city": user["city"],
        "created_at": user.get("created_at", "").isoformat() if user.get("created_at") else None,
        "updated_at": user.get("updated_at", "").isoformat() if user.get("updated_at") else None
    }