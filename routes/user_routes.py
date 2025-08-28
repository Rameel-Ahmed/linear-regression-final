# routes/user_routes.py

from fastapi import APIRouter, UploadFile, Form
from controller.user_controller import UserController
from fastapi.responses import HTMLResponse, StreamingResponse

user_router = APIRouter()
controller = UserController()

# Register routes
user_router.get("/", response_class=HTMLResponse)(controller.serve_homepage)
user_router.post("/analyze-data-quality")(controller.analyze_data_quality)
user_router.post("/process-data")(controller.process_data)
user_router.post("/start-training")(controller.start_training)
user_router.post("/pause-training")(controller.pause_training)
user_router.post("/resume-training")(controller.resume_training)
user_router.post("/stop-training")(controller.stop_training)
