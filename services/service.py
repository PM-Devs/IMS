from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from geopy.distance import geodesic
from database.models import (
    PyObjectId, Rating, User, Student, SchoolSupervisor, Evaluation, Notification, VisitLocation, AppCredentials, Token,
    LogBookEntry, MonthlySummary, FinalAssessment, AttachmentReport, WhiteList, Zone, Area, ChatMessage, ChatRoom,
    Company, Internship, Application, SupervisorDistribution, DistributionRun, SupervisorWorkload,
    ChatRoom

)
from database.config import MONGODB_URI, DATABASE_NAME, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS

# MongoDB setup
client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication and Authorization
async def verify_app_credentials(app_id: str, app_key: str) -> bool:
    app_cred = await db.app_credentials.find_one({"app_id": app_id, "app_key": app_key})
    if app_cred:
        await db.app_credentials.update_one(
            {"_id": app_cred["_id"]},
            {"$set": {"last_used": datetime.utcnow()}}
        )
        return True
    return False

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(email: str):
    user_dict = await db.users.find_one({"email": email})
    if user_dict:
        return User(**user_dict)

async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user or not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer", expires_at=expire)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(email=email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_supervisor(current_user: User = Depends(get_current_user)):
    if current_user.role != "supervisor-school":
        raise HTTPException(status_code=400, detail="User is not a supervisor")
    return current_user

async def logout(token: str):
    await db.token_blacklist.insert_one({"token": token, "invalidated_at": datetime.utcnow()})
    return True

async def is_token_blacklisted(token: str):
    blacklisted_token = await db.token_blacklist.find_one({"token": token})
    return blacklisted_token is not None

# Supervisor Dashboard
async def get_supervisor_dashboard(supervisor_id: str):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    # Get basic supervision stats
    total_students = len(supervisor["assigned_students"])
    completed_supervisions = await db.evaluations.count_documents({"supervisor_id": ObjectId(supervisor_id)})
    pending_supervisions = total_students - completed_supervisions

    # Get students details
    students = await db.students.find({"_id": {"$in": supervisor["assigned_students"]}}).to_list(None)
    
    # Get notifications
    notifications = await db.notifications.find(
        {"user_id": ObjectId(supervisor_id)}
    ).sort("created_at", -1).limit(5).to_list(None)

    # Find the area the supervisor is posted to
    zone = None
    area = None
    if supervisor.get("zone_id"):
        zone = await db.zones.find_one({"_id": supervisor["zone_id"]})
    if supervisor.get("area_id"):
        area = await db.areas.find_one({"_id": supervisor["area_id"]})

    location_posted = {
        "zone": zone["name"] if zone else None,
        "area": area["name"] if area else None
    }

    # Get recent activities
    recent_activities = []
    
    # Check recent evaluations
    recent_evals = await db.evaluations.find(
        {"supervisor_id": ObjectId(supervisor_id)}
    ).sort("created_at", -1).limit(3).to_list(None)
    for eval in recent_evals:
        student = await db.students.find_one({"_id": eval["application_id"]})
        if student:
            recent_activities.append({
                "type": "evaluation",
                "description": f"Assessed student {student.get('first_name', '')} {student.get('last_name', '')}",
                "timestamp": eval["created_at"]
            })

    # Check recent visit locations
    recent_visits = await db.visit_locations.find(
        {"supervisor_id": ObjectId(supervisor_id)}
    ).sort("visit_date", -1).limit(3).to_list(None)
    for visit in recent_visits:
        student = await db.students.find_one({"_id": visit["student_id"]})
        if student:
            recent_activities.append({
                "type": "visit",
                "description": f"Visited student {student.get('first_name', '')} {student.get('last_name', '')}",
                "timestamp": visit["visit_date"]
            })

    # Sort all activities by timestamp
    recent_activities.sort(key=lambda x: x["timestamp"], reverse=True)

    return {
        "total_students": total_students,
        "completed_supervisions": completed_supervisions,
        "pending_supervisions": pending_supervisions,
        "students": students,
        "notifications": notifications,
        "area_posted_to": location_posted,
        "recent_activities": recent_activities[:10]  # Limit to 5 most recent activities
    }
async def get_student_list(supervisor_id: str, status: Optional[str] = None):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    query = {"_id": {"$in": supervisor["assigned_students"]}}
    if status:
        query.update({"status": status})

    students = await db.students.find(query).to_list(None)
    return students

async def update_student_status(student_id: str, status: str):
    result = await db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"status": status}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student status updated successfully"}

async def get_student_location(student_id: str):
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student or not student.get("current_location"):
        raise HTTPException(status_code=404, detail="Student location not found")
    return student["current_location"]

async def is_student_at_company(student_id: str, company_id: str, max_distance: float = 200):
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    company = await db.companies.find_one({"_id": ObjectId(company_id)})
    
    if not student or not company:
        raise HTTPException(status_code=404, detail="Student or company not found")
    
    if not student.get("current_location") or not company.get("address"):
        return False
    
    student_location = (student["current_location"].latitude, student["current_location"].longitude)
    company_location = (company["address"].coordinate.latitude, company["address"].coordinate.longitude)
    
    distance = geodesic(student_location, company_location).meters
    return distance <= max_distance

# Visit Locations
async def get_visit_locations(supervisor_id: str):
    visit_locations = await db.visit_locations.find({"supervisor_id": ObjectId(supervisor_id)}).to_list(None)
    return visit_locations

async def create_visit_location(supervisor_id: str, visit_data: dict):
    visit_location = VisitLocation(
        supervisor_id=ObjectId(supervisor_id),
        student_id=ObjectId(visit_data["student_id"]),
        internship_id=ObjectId(visit_data["internship_id"]),
        company_id=ObjectId(visit_data["company_id"]),
        source_location=visit_data["source_location"],
        destination_location=visit_data["destination_location"],
        visit_date=visit_data["visit_date"],
        status="Pending",
        notes=visit_data.get("notes")
    )
    result = await db.visit_locations.insert_one(visit_location.dict(by_alias=True))
    return str(result.inserted_id)

async def update_visit_location(visit_location_id: str, visit_location: VisitLocation):
    result = await db.visit_locations.update_one(
        {"_id": ObjectId(visit_location_id)},
        {"$set": visit_location.dict(exclude={"id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Visit location not found")
    return True

async def delete_visit_location(visit_location_id: str):
    result = await db.visit_locations.delete_one({"_id": ObjectId(visit_location_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Visit location not found")
    return True

async def update_visit_status(visit_id: str, status: str):
    result = await db.visit_locations.update_one(
        {"_id": ObjectId(visit_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Visit location not found")
    return {"message": "Visit status updated successfully"}

# Supervisor Profile
async def get_supervisor_profile(supervisor_id: str):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    user = await db.users.find_one({"_id": supervisor["user_id"]})
    return {**supervisor, **user}

async def update_supervisor_profile(supervisor_id: str, profile_data: dict):
    result = await db.school_supervisors.update_one(
        {"_id": ObjectId(supervisor_id)},
        {"$set": profile_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    return True

async def delete_supervisor(supervisor_id: str):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    result = await db.school_supervisors.delete_one({"_id": ObjectId(supervisor_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    await db.users.delete_one({"_id": supervisor["user_id"]})
    return True

# Student Logs
async def view_student_logs(student_id: str, log_type: str):
    if log_type == "daily":
        logs = await db.logbook_entries.find({"student_id": ObjectId(student_id), "status": "Submitted"}).to_list(None)
    elif log_type == "monthly":
        logs = await db.monthly_summaries.find({"student_id": ObjectId(student_id), "status": "Submitted"}).to_list(None)
    else:
        raise HTTPException(status_code=400, detail="Invalid log type")
    return logs

async def mark_logbook(supervisor_id: str, logbook_id: str, status: str, comments: Optional[str] = None):
    result = await db.logbook_entries.update_one(
        {"_id": ObjectId(logbook_id)},
        {"$set": {"status": status, "supervisor_comments": comments, "updated_at": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Logbook entry not found")
    return {"message": "Logbook entry updated successfully"}

# Final Reports
async def create_final_report(supervisor_id: str, student_id: str, report_data: dict):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    final_assessment = await db.final_assessments.find_one({"student_id": ObjectId(student_id)})
    if not final_assessment:
        raise HTTPException(status_code=404, detail="Final assessment not found")

    if final_assessment["status"] != "Approved":
        raise HTTPException(status_code=403, detail="Final assessment not approved")

    report_data["supervisor_id"] = ObjectId(supervisor_id)
    report_data["student_id"] = ObjectId(student_id)
    result = await db.attachment_reports.insert_one(report_data)
    return str(result.inserted_id)

async def update_final_report(report_id: str, report_data: dict):
    result = await db.attachment_reports.update_one(
        {"_id": ObjectId(report_id)},
        {"$set": report_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Final report not found")
    return {"message": "Final report updated successfully"}

async def get_final_report(report_id: str):
    report = await db.attachment_reports.find_one({"_id": ObjectId(report_id)})
    if not report:
        raise HTTPException(status_code=404, detail="Final report not found")
    return report

async def delete_final_report(report_id: str):
    result = await db.attachment_reports.delete_one({"_id": ObjectId(report_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Final report not found")
    return {"message": "Final report deleted successfully"}


async def create_evaluation(supervisor_id: str, application_id: str, evaluation_data: dict):
    evaluation = Evaluation(
        supervisor_id=ObjectId(supervisor_id),
        application_id=ObjectId(application_id),
        evaluation_type=evaluation_data["evaluation_type"],
        evaluation_date=datetime.utcnow(),
        criteria=evaluation_data["criteria"],
        total_score=evaluation_data["total_score"],
        max_total_score=evaluation_data["max_total_score"],
        comments=evaluation_data.get("comments"),
        strengths=evaluation_data.get("strengths", []),
        areas_for_improvement=evaluation_data.get("areas_for_improvement", [])
    )
    result = await db.evaluations.insert_one(evaluation.dict(by_alias=True))
    return str(result.inserted_id)



async def assign_area_and_students_to_supervisor(zone_leader: User, zone_id: str, area_data: dict, supervisor_id: str):
    zone = await db.zones.find_one({"_id": ObjectId(zone_id)})
    if not zone or str(zone.zone_leader) != str(zone_leader.id):
        raise HTTPException(status_code=403, detail="Not authorized to assign areas")
    
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id), "zone_id": ObjectId(zone_id)})
    if not supervisor:
        raise HTTPException(status_code=400, detail="Supervisor is not part of this Zone")
    
    new_area = Area(**area_data, zone_id=ObjectId(zone_id), supervisors=[ObjectId(supervisor_id)])
    result = await db.areas.insert_one(new_area.dict(by_alias=True))
    area_id = str(result.inserted_id)
    
    students = await db.students.find({
        "zone_id": ObjectId(zone_id),
        "area_id": None,
        "assigned_supervisor": None
    }).limit(10).to_list(None)  # Limit to 10 students for example
    
    if students:
        student_ids = [student["_id"] for student in students]
        await db.school_supervisors.update_one(
            {"_id": ObjectId(supervisor_id)},
            {"$push": {"assigned_students": {"$each": student_ids}}}
        )
        await db.students.update_many(
            {"_id": {"$in": student_ids}},
            {"$set": {"area_id": ObjectId(area_id), "assigned_supervisor": ObjectId(supervisor_id)}}
        )
        await db.areas.update_one(
            {"_id": ObjectId(area_id)},
            {"$push": {"students": {"$each": student_ids}}}
        )
        return {
            "message": "Area assigned and students assigned to supervisor successfully",
            "area_id": area_id,
            "assigned_students": len(students)
        }
    else:
        return {
            "message": "Area assigned successfully, but no new students found to assign",
            "area_id": area_id,
            "assigned_students": 0
        }

async def get_assigned_students(supervisor_id: str):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    students = await db.students.find({"_id": {"$in": supervisor["assigned_students"]}}).to_list(None)
    return students

async def get_supervisor_workload(supervisor_id: str):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    
    workload = await db.supervisor_workloads.find_one({"supervisor_id": ObjectId(supervisor_id)})
    if not workload:
        workload = SupervisorWorkload(
            supervisor_id=ObjectId(supervisor_id),
            total_students=len(supervisor["assigned_students"]),
            total_supervision_time=0,
            zones=[supervisor["zone_id"]],
            areas=[supervisor["area_id"]] if supervisor.get("area_id") else []
        )
        await db.supervisor_workloads.insert_one(workload.dict(by_alias=True))
    
    return workload



async def create_rating(rating_data: dict) -> Rating:
    rating = Rating(**rating_data)
    result = await db.ratings.insert_one(rating.dict(by_alias=True))
    rating.id = result.inserted_id
    return rating

async def create_whitelist(whitelist_data: dict) -> WhiteList:
    whitelist = WhiteList(**whitelist_data)
    result = await db.whitelists.insert_one(whitelist.dict(by_alias=True))
    whitelist.id = result.inserted_id
    return whitelist

async def create_supervisor(supervisor_data: dict):
    # Check if email already exists
    existing_user = await db.users.find_one({"email": supervisor_data["email"]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    user_data = {
        "email": supervisor_data["email"],
        "password": get_password_hash(supervisor_data["password"]),
        "role": "supervisor-school",
        "first_name": supervisor_data["first_name"],
        "last_name": supervisor_data["last_name"],
        "contact_info": supervisor_data.get("contact_info"),
        "address": supervisor_data.get("address"),
        "profile_picture": supervisor_data.get("profile_picture"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    user_result = await db.users.insert_one(user_data)
    
    # Create supervisor document
    supervisor_specific_data = {
        "user_id": user_result.inserted_id,
        "department_id": ObjectId(supervisor_data["department_id"]),
        "position": supervisor_data.get("position"),
        "qualifications": supervisor_data.get("qualifications", []),
        "areas_of_expertise": supervisor_data.get("areas_of_expertise", []),
        "zone_id": ObjectId(supervisor_data["zone_id"]) if supervisor_data.get("zone_id") else None,
        "area_id": ObjectId(supervisor_data["area_id"]) if supervisor_data.get("area_id") else None,
        "assigned_students": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    supervisor_result = await db.school_supervisors.insert_one(supervisor_specific_data)
    
    # Create notification for new supervisor
    notification_data = {
        "user_id": user_result.inserted_id,
        "title": "Welcome to the Supervision System",
        "description": "Your supervisor account has been created successfully.",
        "notification_type": "welcome",
        "created_at": datetime.utcnow()
    }
    await db.notifications.insert_one(notification_data)
    
    # Fetch and return the complete supervisor profile
    supervisor = await db.school_supervisors.find_one({"_id": supervisor_result.inserted_id})
    user = await db.users.find_one({"_id": user_result.inserted_id})
    
    return {
        "supervisor_id": str(supervisor_result.inserted_id),
        "user_id": str(user_result.inserted_id),
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "role": user["role"],
        "department_id": str(supervisor["department_id"]),
        "zone_id": str(supervisor["zone_id"]) if supervisor.get("zone_id") else None,
        "area_id": str(supervisor["area_id"]) if supervisor.get("area_id") else None
    }