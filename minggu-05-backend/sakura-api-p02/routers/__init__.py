from fastapi import APIRouter, HTTPException, Query

from schemas import Status, Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])
