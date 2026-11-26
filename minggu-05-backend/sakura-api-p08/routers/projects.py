from fastapi import APIRouter, HTTPException, Query

from data import PROJECTS, TASKS, id_berikutnya
from schemas import Project

router = APIRouter(prefix="/v1/projects", tags=["projects"])