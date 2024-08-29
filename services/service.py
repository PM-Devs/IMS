# services.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from database.models import User, Student, Supervisor, Evaluation, Notification, VisitLocation, AppCredentials, Token, LogBookEntry, MonthlySummary, FinalAssessment, AttachmentReport
from database.config import MONGODB_URI, DATABASE_NAME, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS

# Create a MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

def create_access_token(data: dict):
    to_encode = data.copy()
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

async def get_supervisor_dashboard(supervisor_id: str):
    supervisor = await db.supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    total_students = len(supervisor["assigned_students"])
    completed_supervisions = await db.evaluations.count_documents({"supervisor_id": ObjectId(supervisor_id)})
    pending_supervisions = total_students - completed_supervisions

    students = await db.students.find({"_id": {"$in": supervisor["assigned_students"]}}).to_list(None)
    notifications = await db.notifications.find({"user_id": ObjectId(supervisor_id)}).to_list(None)

    return {
        "location": supervisor["department"],
        "total_students": total_students,
        "completed_supervisions": completed_supervisions,
        "pending_supervisions": pending_supervisions,
        "students": students,
        "notifications": notifications
    }

async def search_students(supervisor_id: str, query: str):
    supervisor = await db.supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    students = await db.students.find({
        "_id": {"$in": supervisor["assigned_students"]},
        "$or": [
            {"first_name": {"$regex": query, "$options": "i"}},
            {"last_name": {"$regex": query, "$options": "i"}},
            {"contact_info.phone": {"$regex": query, "$options": "i"}},
            {"academic_info.institution": {"$regex": query, "$options": "i"}}
        ]
    }).to_list(None)
    return students

async def get_student_list(supervisor_id: str, status: Optional[str] = None):
    supervisor = await db.supervisors.find_one({"_id": ObjectId(supervisor_id)})
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

async def get_visit_locations(supervisor_id: str):
    visit_locations = await db.visit_locations.find({"supervisor_id": ObjectId(supervisor_id)}).to_list(None)
    return visit_locations

async def create_visit_location(supervisor_id: str, visit_location: VisitLocation):
    visit_location_dict = visit_location.dict()
    visit_location_dict["supervisor_id"] = ObjectId(supervisor_id)
    result = await db.visit_locations.insert_one(visit_location_dict)
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

async def get_supervisor_profile(supervisor_id: str):
    supervisor = await db.supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    user = await db.users.find_one({"_id": supervisor["user_id"]})
    return {**supervisor, **user}

async def update_supervisor_profile(supervisor_id: str, profile_data: dict):
    result = await db.supervisors.update_one(
        {"_id": ObjectId(supervisor_id)},
        {"$set": profile_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    return True

async def delete_supervisor(supervisor_id: str):
    supervisor = await db.supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    result = await db.supervisors.delete_one({"_id": ObjectId(supervisor_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    await db.users.delete_one({"_id": supervisor["user_id"]})
    return True

async def logout(token: str):
    await db.token_blacklist.insert_one({"token": token, "invalidated_at": datetime.utcnow()})
    return True

async def is_token_blacklisted(token: str):
    blacklisted_token = await db.token_blacklist.find_one({"token": token})
    return blacklisted_token is not None

# Supervisory Functions
async def view_student_logs(supervisor_id: str, student_id: str, log_type: str):
    supervisor = await db.supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    if log_type == "daily":
        logs = await db.logbook_entries.find({"student_id": ObjectId(student_id), "status": "Submitted"}).to_list(None)
    elif log_type == "weekly":
        logs = await db.monthly_summaries.find({"student_id": ObjectId(student_id), "status": "Submitted"}).to_list(None)
    elif log_type == "monthly":
        logs = await db.monthly_summaries.find({"student_id": ObjectId(student_id), "status": "Submitted"}).to_list(None)
    else:
        raise HTTPException(status_code=400, detail="Invalid log type")

    return logs

async def mark_logbook(supervisor_id: str, logbook_id: str, status: str, comments: Optional[str] = None):
    result = await db.logbook_entries.update_one(
               {"_id": ObjectId(logbook_id), "supervisor_id": ObjectId(supervisor_id)},
        {"$set": {"status": status, "comments": comments}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Logbook entry not found or not assigned to this supervisor")
    return {"message": "Logbook entry updated successfully"}

async def create_final_report(supervisor_id: str, student_id: str, report_data: dict):
    supervisor = await db.supervisors.find_one({"_id": ObjectId(supervisor_id)})
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

async def generate_evaluation_report(supervisor_id: str, student_id: str):
    supervisor = await db.supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")

    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    evaluations = await db.evaluations.find({"student_id": ObjectId(student_id)}).to_list(None)
    if not evaluations:
        raise HTTPException(status_code=404, detail="No evaluations found for this student")

    return {
        "student": student,
        "evaluations": evaluations
    }

