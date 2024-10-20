from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List,Dict,Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from geopy.distance import geodesic
from database.models import (
    PyObjectId, Rating, User, Student, SchoolSupervisor, Evaluation, Notification, VisitLocation, AppCredentials, Token,
    LogBookEntry, MonthlySummary, FinalAssessment, AttachmentReport, WhiteList, Zone,
    Company, Internship, Application
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

def get_password_hash(password):
    # Combine password and key
    rounds= 1000
    key="TTU_IMS"
    combined = password + key
    hashed = combined
    
    # Perform multiple rounds of a simple mixing function
    for _ in range(rounds):
        new_hash = ""
        for i in range(len(hashed)):
            char = hashed[i]
            # Simple mixing: rotate ASCII value and wrap around
            new_char = chr((ord(char) + i + len(hashed)) % 128)
            new_hash += new_char
        hashed = new_hash
    
    # Convert to a hexadecimal string
    return ''.join(format(ord(c), '02x') for c in hashed)

def verify_password(plain_password, hashed_password):
    return get_password_hash(plain_password) == hashed_password



async def get_user(email: str):
    user_dict = await db.users.find_one({"email": email})
        # Convert _id to id
    if user_dict and '_id' in user_dict:
        user_dict['id'] = str(user_dict.pop('_id')) 
    print(user_dict)
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
    if current_user.role != "Supervisor-School-Base":
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
    supervisor_id = supervisor_id.strip()
    supervisor = await db.school_supervisors.find_one({"user_id": supervisor_id})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    # Get basic supervision stats
    assigned_students = supervisor.get("assigned_students", [])
    if not isinstance(assigned_students, list):
        assigned_students = []
    
    total_students = len(assigned_students)
    completed_supervisions = await db.evaluations.count_documents({"supervisor_id": ObjectId(supervisor_id)})
    pending_supervisions = total_students - completed_supervisions

    # Get students details
    if assigned_students:
        students = await db.students.find({"_id": {"$in": [ObjectId(id) for id in assigned_students]}}).to_list(None)
    else:
        students = []

    # Get notifications
    notifications = await db.notifications.find(
        {"user_id": ObjectId(supervisor_id)}
    ).sort("created_at", -1).limit(5).to_list(None)

    # Find the area the supervisor is posted to
    zone = None
  
    if supervisor.get("zone_id"):
        zone = await db.zones.find_one({"_id": supervisor["zone_id"]})
   

    location_posted = {
        "zone": zone["name"] if zone else None,
        
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
        "recent_activities": recent_activities[:5]  # Limit to 5 most recent activities
    }
async def get_student_list(supervisor_id: str, status: Optional[str] = None):
    supervisor = await db.school_supervisors.find_one({"user_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    query = {"_id": {"$in": supervisor["assigned_students"]}}
    if status:
        query.update({"status": status})

    students = await db.students.find(query).to_list(None)
    return students


async def get_student_location(student_id: str):
    student = await db.students.find_one({"user_id": ObjectId(student_id)})
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


async def update_visit_location(visit_location_id: str, visit_location: VisitLocation):
    result = await db.visit_locations.update_one(
        {"_id": ObjectId(visit_location_id)},
        {"$set": visit_location.dict(exclude={"id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=202, detail="Visit location not found")
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

# Supervisor Profile function
async def get_supervisor_profile(supervisor_id: str):
    # Strip whitespaces from supervisor_id
    supervisor_id = supervisor_id.strip()

    # Log the supervisor ID for debugging
  
    
    # Fetch supervisor using the supervisor_id (string)
    supervisor = await db.school_supervisors.find_one({"user_id": supervisor_id})
    
    # If supervisor is not found, raise an HTTPException
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found in school_supervisors collection")
    
    # Attempt to fetch user details from the 'users' collection
    try:
        # Convert supervisor_id to ObjectId before querying users collection
        user = await db.users.find_one({"_id": ObjectId(supervisor_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid supervisor_id format: {e}")
    
    # If both supervisor and user are found, merge them
    if user:
        # Merge dictionaries and avoid overriding fields from one collection with the other
        merged_data = {**supervisor, **user}
        # Optionally, convert ObjectId to string
        merged_data["_id"] = str(merged_data["_id"])
        return merged_data
    else:
        raise HTTPException(status_code=405, detail="User details for supervisor not found in users collection")

async def update_supervisor_profile(supervisor_id: str, profile_data: dict):
    result = await db.school_supervisors.update_one(
        {"_id": ObjectId(supervisor_id)},
        {"$set": profile_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    return True

async def delete_supervisor(supervisor_id: str):
    supervisor = await db.school_supervisors.find_one({"user_id": supervisor_id})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    result = await db.school_supervisors.delete_one({"user_id": supervisor_id})
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
        raise HTTPException(status_code=202, detail="Logbook entry not found")
    return {"message": "Logbook entry updated successfully"}

# Final Reports
async def create_final_report(supervisor_id: str, student_id: str, report_data: dict):
    supervisor = await db.school_supervisors.find_one({"user_id": supervisor_id})
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
        raise HTTPException(status_code=202, detail="Final report not found")
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


async def get_assigned_students(supervisor_id: str):
    try:
        # Validate supervisor_id
        if not ObjectId.is_valid(supervisor_id):
            raise HTTPException(status_code=400, detail="Invalid supervisor ID")

        supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
        if not supervisor:
            raise HTTPException(status_code=404, detail="Supervisor not found")

        current_date = datetime.utcnow()

        pipeline = [
            {"$match": {"_id": ObjectId(supervisor_id)}},
            {"$unwind": "$students"},
            {"$lookup": {
                "from": "students",
                "localField": "students",
                "foreignField": "_id",
                "as": "student_info"
            }},
            {"$unwind": "$student_info"},
            {"$lookup": {
                "from": "internships",
                "localField": "student_info.active_internship",
                "foreignField": "_id",
                "as": "active_internship"
            }},
            {"$unwind": "$active_internship"},
            {"$lookup": {
                "from": "visit_locations",
                "let": { "student_id": "$students", "internship_id": "$active_internship._id" },
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$and": [
                                { "$eq": ["$student_id", "$$student_id"] },
                                { "$eq": ["$internship_id", "$$internship_id"] },
                                { "$eq": ["$status", "completed"] }
                            ]
                        }
                    }},
                    { "$limit": 1 }
                ],
                "as": "visit"
            }},
            {"$lookup": {
                "from": "evaluations",
                "let": { "student_id": "$students", "internship_id": "$active_internship._id" },
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$and": [
                                { "$eq": ["$application_id", "$$student_id"] },
                                { "$eq": ["$internship_id", "$$internship_id"] }
                            ]
                        }
                    }},
                    { "$limit": 1 }
                ],
                "as": "assessment"
            }},
            {"$project": {
                "student_id": "$students",
                "student_name": "$student_info.name",
                "internship_title": "$active_internship.title",
                "company_name": "$active_internship.company_name",
                "start_date": "$active_internship.start_date",
                "end_date": "$active_internship.end_date",
                "duration": {
                    "$divide": [
                        { "$subtract": ["$active_internship.end_date", "$active_internship.start_date"] },
                        86400000  # milliseconds in a day
                    ]
                },
                "days_left": {
                    "$ceil": {
                        "$divide": [
                            { "$subtract": ["$active_internship.end_date", current_date] },
                            86400000
                        ]
                    }
                },
                "supervision_status": {
                    "$switch": {
                        "branches": [
                            {
                                "case": {"$and": [
                                    { "$gt": [{ "$size": "$visit" }, 0] },
                                    { "$gt": [{ "$size": "$assessment" }, 0] }
                                ]},
                                "then": "100%"
                            },
                            {
                                "case": {"$and": [
                                    { "$gt": [{ "$size": "$visit" }, 0] },
                                    { "$eq": [{ "$size": "$assessment" }, 0] }
                                ]},
                                "then": "50%"
                            }
                        ],
                        "default": "0%"
                    }
                },
                "assessment_status": {
                    "$cond": {
                        "if": { "$gt": [{ "$size": "$assessment" }, 0] },
                        "then": "Completed",
                        "else": "Not started"
                    }
                },
                "visit_status": {
                    "$cond": {
                        "if": { "$gt": [{ "$size": "$visit" }, 0] },
                        "then": "Completed",
                        "else": "Not visited"
                    }
                }
            }}
        ]

        students = await db.school_supervisors.aggregate(pipeline).to_list(None)

        if not students:
            raise HTTPException(status_code=404, detail="No assigned students found")

        return students

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

async def get_supervisor_workload(supervisor_id: str) -> Dict[str, Any]:
    # Convert string ID to PyObjectId
    supervisor_object_id = PyObjectId(supervisor_id)

    # Fetch the supervisor from the database
    supervisor_data = await db.school_supervisors.find_one({"_id": supervisor_object_id})
    if not supervisor_data:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    # Create a SchoolSupervisor instance
    supervisor = SchoolSupervisor(**supervisor_data)

    # Calculate workload information
    total_students = len(supervisor.assigned_students) if supervisor.assigned_students else 0
    
    # Fetch all applications for the assigned students
    student_ids = [PyObjectId(student_id) for student_id in supervisor.assigned_students]
    applications = await db.applications.find({"student_id": {"$in": student_ids}}).to_list(None)

    # Calculate total supervision time (assuming each application requires 1 hour of supervision)
    total_supervision_time = len(applications)

    # Prepare the workload information
    workload_info = {
        "supervisor_id": str(supervisor.id),
        "total_students": total_students,
        "total_supervision_time": total_supervision_time,
        "zone_id": str(supervisor.zone_id) if supervisor.zone_id else None,
        "department_id": str(supervisor.department_id) if supervisor.department_id else None
    }

    return workload_info