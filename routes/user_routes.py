"""routes.user_routes
+---------------------------------------------
Public FastAPI router wiring HTTP endpoints
to :class:`controller.user_controller.UserController` methods.

This module contains *no* business logic; it only exposes a shared
`user_router` that other modules can mount under a path prefix.

Example
-------
>>> from fastapi import FastAPI
>>> from routes.user_routes import user_router
>>> app = FastAPI()
>>> app.include_router(user_router, prefix="/api/v1")
"""

from fastapi import APIRouter
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
