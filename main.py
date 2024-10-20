from fastapi import FastAPI, Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from database.models import User, Student, SchoolSupervisor, Evaluation, Notification, VisitLocation, Token, LogBookEntry, MonthlySummary, FinalAssessment, AttachmentReport
from services import service
from middleware.log import log_middleware
from middleware.auth import auth_middleware
from middleware.requestValidity import request_validity_middleware
from database.config import get_database
from pydantic import BaseModel, EmailStr

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
    email: str
    password: str
    scope: Optional[str] = None

    def get_scope(self):
        return self.scope or "R-WR-R-R"

@app.post("/login", response_model=Token, summary="Authenticate and obtain access token")
async def login_for_access_token(request:Request,Login_request: CustomLoginRequest):
    if Login_request.grant_type != "password":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant_type  Expected 'password'."
        )
    
    user = await service.authenticate_user(Login_request.email, Login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
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


@app.get("/students/{student_id}/location", summary="Get student's current location")
async def get_student_location_endpoint(student_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_student_location(student_id)

@app.get("/students/{student_id}/at-company/{company_id}", summary="Check if student is at company")
async def is_student_at_company_endpoint(student_id: str, company_id: str, max_distance: float = 200, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.is_student_at_company(student_id, company_id, max_distance)

@app.get("/visit-locations", summary="Get visit locations")
async def visit_locations(current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_visit_locations(str(current_user.id))


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


@app.get("/supervisors/{supervisor_id}/assigned-students", summary="Get assigned students")
async def get_assigned_students_endpoint(supervisor_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_assigned_students(supervisor_id)

@app.get("/supervisors/{supervisor_id}/workload", summary="Get supervisor workload")
async def get_supervisor_workload_endpoint(supervisor_id: str, current_user: User = Depends(service.get_current_active_supervisor)):
    return await service.get_supervisor_workload(supervisor_id)


@app.get("/supervisor/{supervisor_id}/assigned-students", response_model=List[dict])
async def get_supervisor_students(supervisor_id: str):
    """
    Retrieve assigned students for a given supervisor.
    
    Parameters:
    - supervisor_id: The ID of the supervisor
    
    Returns:
    - A list of assigned students with their internship details
    
    Raises:
    - 400: If the supervisor ID is invalid
    - 404: If the supervisor is not found or has no assigned students
    - 500: For any other unexpected errors
    """
    try:
        students = await service.get_assigned_students(supervisor_id)
        return students
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Welcome to the Supervisor API. Please refer to the /docs for API documentation."}