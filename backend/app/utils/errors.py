from fastapi import HTTPException

def validation_error(fields: dict):
    raise HTTPException(
        status_code=400,
        detail={
            "error": "validation failed",
            "fields": fields
        }
    )

def unauthorized():
    raise HTTPException(
        status_code=401,
        detail={"error": "unauthorized"}
    )

def forbidden():
    raise HTTPException(
        status_code=403,
        detail={"error": "forbidden"}
    )

def not_found():
    raise HTTPException(
        status_code=404,
        detail={"error": "not found"}
    )