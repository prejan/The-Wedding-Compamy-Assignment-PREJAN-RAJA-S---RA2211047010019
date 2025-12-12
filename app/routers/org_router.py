from fastapi import APIRouter, HTTPException, status, Depends
from app.database import master_db
from app.utils import hash_password
from app.models.organization import OrgCreate, OrgUpdate
from app.models.responses import OrgCreateResponse
from app.auth import get_current_admin

router = APIRouter(prefix="/org", tags=["Organization"])


# -------------------- CREATE ORGANIZATION --------------------
@router.post(
    "/create",
    response_model=OrgCreateResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_org(data: OrgCreate):
    org_name = data.organization_name.strip().lower()

    # Check if organization already exists
    if await master_db.organizations.find_one({"name": org_name}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization already exists"
        )

    collection_name = f"org_{org_name}"

    # Create admin user
    admin_data = {
        "email": data.email,
        "password": hash_password(data.password),
        "org": org_name
    }
    admin_result = await master_db.admins.insert_one(admin_data)

    # Store organization metadata in master DB
    await master_db.organizations.insert_one({
        "name": org_name,
        "collection": collection_name,
        "admin_id": str(admin_result.inserted_id)
    })

    # Create dynamic organization collection
    await master_db[collection_name].insert_one({"initialized": True})

    return {
        "message": "Organization created successfully",
        "organization": {
            "name": org_name,
            "collection": collection_name,
            "admin_email": data.email
        }
    }


# -------------------- GET ORGANIZATION --------------------
@router.get("/get")
async def get_org(organization_name: str):
    org = await master_db.organizations.find_one(
        {"name": organization_name.lower()},
        {"_id": 0}
    )

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    return org


# -------------------- UPDATE ORGANIZATION (JWT PROTECTED) --------------------
@router.put("/update")
async def update_org(
    data: OrgUpdate,
    admin=Depends(get_current_admin)
):
    org_name = data.organization_name.strip().lower()

    # Authorization check
    if admin.get("organization") != org_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this organization"
        )

    org = await master_db.organizations.find_one({"name": org_name})
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    # Update admin credentials
    await master_db.admins.update_one(
        {"org": org_name},
        {"$set": {
            "email": data.email,
            "password": hash_password(data.password)
        }}
    )

    return {"message": "Organization updated successfully"}


# -------------------- DELETE ORGANIZATION (JWT PROTECTED) --------------------
@router.delete("/delete")
async def delete_org(
    organization_name: str,
    admin=Depends(get_current_admin)
):
    org_name = organization_name.strip().lower()

    # Authorization check
    if admin.get("organization") != org_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this organization"
        )

    org = await master_db.organizations.find_one({"name": org_name})
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    # Drop dynamic collection
    await master_db[org["collection"]].drop()

    # Delete metadata and admin
    await master_db.organizations.delete_one({"name": org_name})
    await master_db.admins.delete_many({"org": org_name})

    return {"message": "Organization deleted successfully"}
