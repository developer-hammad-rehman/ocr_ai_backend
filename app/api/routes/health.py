from fastapi import APIRouter

health_router = APIRouter(tags=["Health Router"])


@health_router.get("/")
def health_root_route():
    return {"Response" : "Ok"}


@health_router.get("/status")
def health_status_route():
    return {"Status" : "Healthy"}