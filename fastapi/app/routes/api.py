from fastapi import APIRouter
from endpoints import guest_service, task_service

router = APIRouter()
router.include_router(guest_service.router)
router.include_router(task_service.router)
