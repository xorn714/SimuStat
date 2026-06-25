# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.adapter.api.v1.endpoint import sim_routes

api_router = APIRouter()
api_router.include_router(sim_routes.router, tags=["simulation"])
