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
    Rating, User, Student, SchoolSupervisor, Evaluation, Notification, VisitLocation, AppCredentials, Token,
    LogBookEntry, MonthlySummary, FinalAssessment, AttachmentReport, WhiteList, Zone, Area, ChatMessage, ChatRoom, ZoneChat
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

def create_access_token(data: dict, scopes: str = "R-WR-R-R"):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "scope": scopes})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer", expires_at=expire, scope=scopes)

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

    total_students = len(supervisor["assigned_students"])
    completed_supervisions = await db.evaluations.count_documents({"supervisor_id": ObjectId(supervisor_id)})
    pending_supervisions = total_students - completed_supervisions

    students = await db.students.find({"_id": {"$in": supervisor["assigned_students"]}}).to_list(None)
    notifications = await db.notifications.find({"user_id": ObjectId(supervisor_id)}).to_list(None)

    return {
        "location": supervisor["location"],
        "total_students": total_students,
        "completed_supervisions": completed_supervisions,
        "pending_supervisions": pending_supervisions,
        "students": students,
        "notifications": notifications
    }

# Student Management
async def search_students(supervisor_id: str, query: str):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
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
    
    student_location = (student["current_location"]["latitude"], student["current_location"]["longitude"])
    company_location = (company["address"]["latitude"], company["address"]["longitude"])
    
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

# Evaluations
async def create_evaluation(supervisor_id: str, student_id: str, evaluation_data: dict):
    evaluation = Evaluation(
        supervisor_id=ObjectId(supervisor_id),
        application_id=ObjectId(evaluation_data["application_id"]),
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


async def generate_evaluation_report(supervisor_id: str, student_id: str):
    evaluations = await db.evaluations.find({
        "supervisor_id": ObjectId(supervisor_id),
        "student_id": ObjectId(student_id)
    }).to_list(None)
    
    if not evaluations:
        raise HTTPException(status_code=404, detail="No evaluations found for this student")
    
    report = {
        "student_id": student_id,
        "supervisor_id": supervisor_id,
        "evaluations": evaluations,
        "generated_at": datetime.utcnow()
    }
    
    result = await db.evaluation_reports.insert_one(report)
    return str(result.inserted_id)


async def get_supervisors_in_zone(zone_id: str):
    supervisors = await db.school_supervisors.find({"zone_id": ObjectId(zone_id)}).to_list(None)
    return supervisors

# Zone Management
async def assign_area_and_students_to_supervisor(zone_leader: User, zone_id: str, area_data: dict, supervisor_id: str):
    # Check if the zone leader is authorized
    zone = await db.zones.find_one({"_id": ObjectId(zone_id)})
    if zone.zone_leader != zone_leader.id:
        raise HTTPException(status_code=403, detail="Not authorized to assign areas")
    
    # Check if the Supervisor is part of the Zone
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id), "zone_id": ObjectId(zone_id)})
    if not supervisor:
        raise HTTPException(status_code=400, detail="Supervisor is not part of this Zone")
    
    new_area = Area(**area_data)
    new_area.source_location = supervisor_id
    new_area.destination_locations = [supervisor_id]
    result = await db.areas.insert_one(new_area.dict())
    area_id = str(result.inserted_id)
    
    # Assign students to the supervisor
    students = await db.students.find({
        "internship.company_id": {"$in": new_area.destination_locations},
        "_id": {"$nin": new_area.assigned_students}
    }).to_list(None)
    
    if students:
        student_ids = [student["_id"] for student in students]
        object_student_ids = [ObjectId(id) for id in student_ids]
        result = await db.school_supervisors.update_one(
            {"_id": ObjectId(supervisor_id)},
            {"$addToSet": {"assigned_students": {"$each": object_student_ids}}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Supervisor not found")
        await db.areas.update_one(
            {"_id": ObjectId(area_id)},
            {"$addToSet": {"assigned_students": {"$each": object_student_ids}}}
        )
        return {
            "message": "Area assigned and students assigned to supervisor successfully",
            "area_id": area_id,
            "assigned_students": len(students)
        }
    else:
        return {
            "message": "Area assigned successfully, but no new students found in the assigned area",
            "area_id": area_id,
            "assigned_students": 0
        }

async def get_assigned_students(supervisor_id: str):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    students = await db.students.find({"_id": {"$in": supervisor["assigned_students"]}}).to_list(None)
    return students

# Workload Management
async def get_supervisor_workload(supervisor_id: str):
    supervisor = await db.school_supervisors.find_one({"_id": ObjectId(supervisor_id)})
    if not supervisor:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    assigned_students_count = len(supervisor["assigned_students"])
    completed_evaluations = await db.evaluations.count_documents({"supervisor_id": ObjectId(supervisor_id)})
    return {
        "assigned_students": assigned_students_count,
        "completed_evaluations": completed_evaluations
    }

async def create_zone_chat_for_new_zone(zone: Zone):
    zone_chat = ZoneChat(
        zone_id=zone.id,
        participants=[supervisor.id for supervisor in zone.supervisors],
        messages=[],
        created_at=zone.created_at,
        updated_at=zone.updated_at
    )
    result = await db.zone_chats.insert_one(zone_chat.dict())
    zone_chat.id = result.inserted_id
    return zone_chat

# Chat functionality
async def create_chat_room(participants: List[PyObjectId]) -> ChatRoom:
    chat_room = ChatRoom(
        participants=participants,
        messages=[],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    result = await db.chat_rooms.insert_one(chat_room.dict())
    chat_room.id = result.inserted_id
    return chat_room

async def send_chat_message(chat_room_id: str, sender_id: str, content: str) -> ChatMessage:
    chat_message = ChatMessage(
        sender_id=ObjectId(sender_id),
        receiver_id=None,  # Set receiver_id to None for group chats
        content=content,
        timestamp=datetime.utcnow()
    )
    result = await db.chat_messages.insert_one(chat_message.dict())
    chat_message.id = result.inserted_id

    # Update the chat room
    await db.chat_rooms.update_one(
        {"_id": ObjectId(chat_room_id)},
        {"$push": {"messages": chat_message.id}, "$set": {"updated_at": datetime.utcnow()}}
    )

    return chat_message

async def get_chat_history(chat_room_id: str) -> List[ChatMessage]:
    chat_room = await db.chat_rooms.find_one({"_id": ObjectId(chat_room_id)})
    if not chat_room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    chat_messages = await db.chat_messages.find({"_id": {"$in": chat_room["messages"]}}).to_list(None)
    return chat_messages

async def mark_chat_message_as_read(chat_room_id: str, message_id: str, user_id: str):
    result = await db.chat_messages.update_one(
        {"_id": ObjectId(message_id), "receiver_id": ObjectId(user_id)},
        {"$set": {"read": True, "read_at": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Chat message not found")
    return True

async def get_unread_notifications(user_id: str) -> List[Notification]:
    notifications = await db.notifications.find({"user_id": ObjectId(user_id), "read": False}).to_list(None)
    return notifications

async def mark_notification_as_read(notification_id: str, user_id: str):
    result = await db.notifications.update_one(
        {"_id": ObjectId(notification_id), "user_id": ObjectId(user_id)},
        {"$set": {"read": True, "read_at": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return True

# Rating and Whitelist
async def create_rating(rating_data: dict) -> Rating:
    rating = Rating(**rating_data)
    result = await db.ratings.insert_one(rating.dict())
    rating.id = result.inserted_id
    return rating

async def get_ratings_for_student(student_id: str) -> List[Rating]:
    ratings = await db.ratings.find({"student_id": ObjectId(student_id)}).to_list(None)
    return ratings

async def create_whitelist(whitelist_data: dict) -> WhiteList:
    whitelist = WhiteList(**whitelist_data)
    result = await db.whitelists.insert_one(whitelist.dict())
    whitelist.id = result.inserted_id
    return whitelist

async def get_whitelisted_internships(company_id: str) -> List[WhiteList]:
    whitelisted_internships = await db.whitelists.find({"company_id": ObjectId(company_id)}).to_list(None)
    return whitelisted_internships