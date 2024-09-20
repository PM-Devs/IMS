from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from database.models import User, Student, SchoolSupervisor, Evaluation, Notification, VisitLocation, Token, LogBookEntry, MonthlySummary, FinalAssessment, AttachmentReport, ChatMessage, ChatRoom
from services import service
from middleware.log import log_middleware
from middleware.auth import auth_middleware
from middleware.requestValidity import request_validity_middleware
from database.config import get_database
from pydantic import BaseModel

app = FastAPI(title="Supervisor API", description="API for managing supervisor activities in the internship system")

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

class CustomLoginRequest(BaseModel):
    grant_type: str
    username: str
    password: str
    scope: Optional[str] = None

    def get_scope(self):
        return self.scope or "R-WR-R-R"

@app.post("/login", response_model=Token, summary="Authenticate and obtain access token")
async def login_for_access_token(request: CustomLoginRequest):
    if request.grant_type != "password":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant_type. Expected 'password'."
        )
    
    user = await service.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = service.create_access_token(data={"sub": user.email})
    return access_token

@app.post("/logout", summary="Logout and invalidate the current token")
async def logout_user(current_user: User = Depends(service.get_current_active_supervisor)):
    await service.logout(current_user.token)
    return {"message": "Successfully logged out"}

@app.get("/dashboard", summary="Get supervisor dashboard information")
async def dashboard(current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_supervisor_dashboard(str(current_user.id))

@app.get("/students/search", summary="Search for students")
async def search_students_endpoint(query: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.search_students(str(current_user.id), query)

@app.get("/students", summary="Get list of students")
async def student_list(status: Optional[str] = None, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_student_list(str(current_user.id), status)

@app.put("/students/{student_id}/status", summary="Update student status")
async def update_student_status_endpoint(student_id: str, status: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.update_student_status(student_id, status)

@app.get("/students/{student_id}/location", summary="Get student's current location")
async def get_student_location_endpoint(student_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_student_location(student_id)

@app.get("/students/{student_id}/at-company/{company_id}", summary="Check if student is at company")
async def is_student_at_company_endpoint(student_id: str, company_id: str, max_distance: float = 200, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.is_student_at_company(student_id, company_id, max_distance)

@app.get("/visit-locations", summary="Get visit locations")
async def visit_locations(current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_visit_locations(str(current_user.id))

@app.post("/visit-locations", summary="Create a new visit location")
async def create_visit_location_endpoint(visit_data: dict, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.create_visit_location(str(current_user.id), visit_data)

@app.put("/visit-locations/{visit_location_id}", summary="Update a visit location")
async def update_visit_location_endpoint(visit_location_id: str, visit_location: VisitLocation, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.update_visit_location(visit_location_id, visit_location)

@app.delete("/visit-locations/{visit_location_id}", summary="Delete a visit location")
async def delete_visit_location_endpoint(visit_location_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.delete_visit_location(visit_location_id)

@app.put("/visit-locations/{visit_id}/status", summary="Update visit status")
async def update_visit_status_endpoint(visit_id: str, status: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.update_visit_status(visit_id, status)

@app.get("/profile", summary="Get supervisor profile")
async def get_profile(current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_supervisor_profile(str(current_user.id))

@app.put("/profile", summary="Update supervisor profile")
async def update_profile(profile_data: dict, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.update_supervisor_profile(str(current_user.id), profile_data)

@app.delete("/profile", summary="Delete supervisor profile")
async def delete_profile(current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.delete_supervisor(str(current_user.id))

@app.get("/logs/{student_id}/{log_type}", summary="View student logs")
async def get_student_logs(student_id: str, log_type: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.view_student_logs(student_id, log_type)

@app.put("/logs/{logbook_id}/mark", summary="Mark logbook entry")
async def mark_logbook_entry(logbook_id: str, status: str, comments: Optional[str] = None, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.mark_logbook(str(current_user.id), logbook_id, status, comments)

@app.post("/final-reports", summary="Create final report")
async def create_final_report_endpoint(student_id: str, report_data: dict, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.create_final_report(str(current_user.id), student_id, report_data)

@app.put("/final-reports/{report_id}", summary="Update final report")
async def update_final_report_endpoint(report_id: str, report_data: dict, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.update_final_report(report_id, report_data)

@app.get("/final-reports/{report_id}", summary="Get final report")
async def get_final_report_endpoint(report_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_final_report(report_id)

@app.delete("/final-reports/{report_id}", summary="Delete final report")
async def delete_final_report_endpoint(report_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.delete_final_report(report_id)

@app.post("/evaluations", summary="Create evaluation")
async def create_evaluation_endpoint(application_id: str, evaluation_data: dict, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.create_evaluation(str(current_user.id), application_id, evaluation_data)


@app.get("/zones/{zone_id}/supervisors", summary="Get supervisors in zone")
async def get_supervisors_in_zone_endpoint(zone_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_supervisors_in_zone(zone_id)

@app.get("/supervisors/{supervisor_id}/assigned-students", summary="Get assigned students")
async def get_assigned_students_endpoint(supervisor_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_assigned_students(supervisor_id)

@app.get("/supervisors/{supervisor_id}/workload", summary="Get supervisor workload")
async def get_supervisor_workload_endpoint(supervisor_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_supervisor_workload(supervisor_id)

@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Welcome to the Supervisor API. Please refer to the /docs for API documentation."}