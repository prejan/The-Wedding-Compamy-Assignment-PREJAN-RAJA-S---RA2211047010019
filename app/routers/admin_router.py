from fastapi import APIRouter, HTTPException
from app.database import master_db
from app.utils import verify_password, create_jwt
from app.models.user import AdminLogin

router = APIRouter(prefix="/admin")

@router.post("/login")
async def admin_login(data: AdminLogin):
    admin = await master_db.admins.find_one({"email": data.email})
    if not admin:
        raise HTTPException(401, "Invalid credentials")

    if not verify_password(data.password, admin["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_jwt({
        "admin": str(admin["_id"]),
        "organization": admin["org"]
    })

    return {"token": token}
