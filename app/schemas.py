from datetime import date, datetime

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "birth_date": user["birth_date"].isoformat() if isinstance(user["birth_date"], (date, datetime)) else str(user["birth_date"]),
        "city": user["city"],
        "created_at": user.get("created_at").isoformat() if isinstance(user.get("created_at"), (date, datetime)) else None,
        "updated_at": user.get("updated_at").isoformat() if isinstance(user.get("updated_at"), (date, datetime)) else None
    }