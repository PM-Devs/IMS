from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from database.models import User, Student, Supervisor, Evaluation, Notification, VisitLocation, Token, LogBookEntry, MonthlySummary, FinalAssessment, AttachmentReport
from services.service import (
    get_current_active_supervisor, get_supervisor_dashboard, search_students,
    get_student_list, update_student_status, get_visit_locations, create_visit_location,
    update_visit_location, delete_visit_location, get_supervisor_profile,
    update_supervisor_profile, delete_supervisor, authenticate_user, create_access_token,
    logout, view_student_logs, mark_logbook, create_final_report, update_final_report,
    get_final_report, delete_final_report, generate_evaluation_report
)
from middleware.log import log_middleware
from middleware.auth import auth_middleware
from middleware.requestValidity import request_validity_middleware
from database.config import get_database

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middlewares
app.middleware("http")(log_middleware)
app.middleware("http")(auth_middleware)
app.middleware("http")(request_validity_middleware)

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    async with get_database() as db:
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return create_access_token(data={"sub": user.email})

@app.post("/logout")
async def logout_user(current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        await logout(db, current_user.id)
        return {"message": "Successfully logged out"}

@app.get("/dashboard")
async def dashboard(current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await get_supervisor_dashboard(db, str(current_user.id))

@app.get("/students/search")
async def search_students_endpoint(query: str, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await search_students(db, str(current_user.id), query)

@app.get("/students")
async def student_list(status: Optional[str] = None, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await get_student_list(db, str(current_user.id), status)

@app.put("/students/{student_id}/status")
async def update_student_status_endpoint(student_id: str, status: str, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await update_student_status(db, student_id, status)

@app.get("/visit-locations")
async def visit_locations(current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await get_visit_locations(db, str(current_user.id))

@app.post("/visit-locations")
async def create_visit_location_endpoint(visit_location: VisitLocation, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await create_visit_location(db, str(current_user.id), visit_location)

@app.put("/visit-locations/{visit_location_id}")
async def update_visit_location_endpoint(visit_location_id: str, visit_location: VisitLocation, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await update_visit_location(db, visit_location_id, visit_location)

@app.delete("/visit-locations/{visit_location_id}")
async def delete_visit_location_endpoint(visit_location_id: str, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await delete_visit_location(db, visit_location_id)

@app.get("/profile")
async def get_profile(current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await get_supervisor_profile(db, str(current_user.id))

@app.put("/profile")
async def update_profile(profile_data: dict, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await update_supervisor_profile(db, str(current_user.id), profile_data)

@app.delete("/profile")
async def delete_profile(current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await delete_supervisor(db, str(current_user.id))

@app.get("/logs/{student_id}/{log_type}")
async def get_student_logs(student_id: str, log_type: str, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await view_student_logs(db, str(current_user.id), student_id, log_type)

@app.put("/logs/{logbook_id}/mark")
async def mark_logbook_entry(logbook_id: str, status: str, comments: Optional[str] = None, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await mark_logbook(db, str(current_user.id), logbook_id, status, comments)

@app.post("/final-reports")
async def create_final_report_endpoint(student_id: str, report_data: dict, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await create_final_report(db, str(current_user.id), student_id, report_data)

@app.put("/final-reports/{report_id}")
async def update_final_report_endpoint(report_id: str, report_data: dict, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await update_final_report(db, report_id, report_data)

@app.get("/final-reports/{report_id}")
async def get_final_report_endpoint(report_id: str, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await get_final_report(db, report_id)

@app.delete("/final-reports/{report_id}")
async def delete_final_report_endpoint(report_id: str, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await delete_final_report(db, report_id)

@app.get("/evaluations")
async def generate_evaluation_report_endpoint(student_id: str, current_user: User = Depends(get_current_active_supervisor)):
    async with get_database() as db:
        return await generate_evaluation_report(db, str(current_user.id), student_id)
