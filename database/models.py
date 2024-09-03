#models.py
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict
from typing import Any, Dict, Optional, List, Annotated
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict
from typing import Any, Dict, Optional, List, Annotated
from datetime import datetime
from geopy.distance import geodesic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema: Any, _handler: Any) -> Dict[str, Any]:
        return {"type": "string"}

class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class Address(BaseModelWithConfig):
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ContactInfo(BaseModelWithConfig):
    phone: str
    alternative_phone: Optional[str] = None
    email: EmailStr
    alternative_email: Optional[EmailStr] = None

class Department(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    name: str
    faculty_id: PyObjectId
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Faculty(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Programme(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    name: str
    department_id: PyObjectId
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    role: str  # E.g., 'Student', 'Company', 'Supervisor', 'Department','ILO'
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    profile_picture: Optional[HttpUrl] = None
    contact_info: ContactInfo
    address: Address
    date_of_birth: datetime
    gender: str
    nationality: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AcademicInfo(BaseModelWithConfig):
    institution: str
    degree: str
    major: str
    year_of_study: int
    gpa: float



class Company(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    user_id: PyObjectId
    company_name: str
    industry: str
    company_size: str
    year_founded: int
    website: HttpUrl
    logo_url: Optional[HttpUrl] = None
    description: str
    address: Address
    contact_info: ContactInfo
    internships_posted: List[PyObjectId] = []  # List of internship IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Internship(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    company_id: PyObjectId
    title: str
    description: str
    responsibilities: List[str]
    requirements: List[str]
    location: Address
    industry: str
    internship_type: str
    duration: str
    start_date: datetime
    end_date: datetime
    stipend: Optional[float] = None
    application_deadline: datetime
    max_applications: int
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Application(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    internship_id: PyObjectId
    status: str  # E.g., 'Applied', 'Accepted', 'Rejected', 'Withdrawn'
    application_date: datetime
    cover_letter: str
    resume_url: HttpUrl
    acceptance_date: Optional[datetime] = None
    rejection_date: Optional[datetime] = None
    withdrawal_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)



class EvaluationCriteria(BaseModelWithConfig):
    criterion: str
    score: float
    max_score: float
    weight: float

class Evaluation(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    application_id: PyObjectId
    supervisor_id: PyObjectId
    evaluation_type: str  # E.g., 'Midterm', 'Final'
    evaluation_date: datetime
    criteria: List[EvaluationCriteria]
    total_score: float
    max_total_score: float
    comments: Optional[str] = None
    strengths: List[str] = []
    areas_for_improvement: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Notification(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    user_id: PyObjectId
    title: str
    description: str
    notification_type: str  # E.g., 'Application Status', 'Reminder'
    picture_url: Optional[HttpUrl] = None
    link: Optional[HttpUrl] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read: bool = False
    read_at: Optional[datetime] = None

class VisitLocation(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    supervisor_id: PyObjectId
    student_id: PyObjectId
    internship_id: PyObjectId
    company_id: PyObjectId
    source_location: Address
    destination_location: Address
    visit_date: datetime
    status: str  # E.g., 'Completed', 'Pending'
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AppCredentials(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    app_id: str
    app_key: str
    app_name: str
    description: str
    created_by: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    is_active: bool = True

class LogBookEntry(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    internship_id: PyObjectId
    date: datetime
    activities: List[str]
    learning_outcomes: List[str]
    challenges: Optional[str] = None
    hours_worked: float
    status: str  # E.g., 'Submitted', 'Reviewed'
    supervisor_comments: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MonthlySummary(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    internship_id: PyObjectId
    month: str  # Format: 'YYYY-MM'
    summary: str
    key_learnings: List[str]
    challenges: Optional[str] = None
    goals_for_next_month: List[str]
    status: str  # E.g., 'Submitted', 'Reviewed'
    supervisor_comments: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class FinalAssessment(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    internship_id: PyObjectId
    assessment_date: datetime
    final_report_url: HttpUrl
    overall_performance: str  # E.g., 'Excellent', 'Good', 'Satisfactory', 'Needs Improvement'
    final_grade: Optional[float] = None
    supervisor_comments: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AttachmentReport(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    internship_id: PyObjectId
    submission_date: datetime
    report_url: HttpUrl
    executive_summary: str
    activities_summary: str
    learnings: List[str]
    challenges: List[str]
    recommendations: List[str]
    status: str  # E.g., 'Submitted', 'Reviewed', 'Approved', 'Rejected'
    department_comments: Optional[str] = None
    final_grade: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Token(BaseModelWithConfig):
    access_token: str
    token_type: str
    expires_at: datetime
    


class Zone(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    name: str
    description: Optional[str] = None
    locations: List[Address]  # List of locations covered by this zone
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Supervisor(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    user_id: PyObjectId
    type: str  # E.g., 'Company' or 'School'
    department_id: Optional[PyObjectId] = None
    position: str
    company_id: Optional[PyObjectId] = None
    assigned_students: List[PyObjectId] = []  # List of student IDs
    qualifications: List[str] = []
    areas_of_expertise: List[str] = []
    zone_id: PyObjectId  # New field to associate supervisor with a zone
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Student(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    user_id: PyObjectId
    registration_number: str
    academic_info: AcademicInfo
    resume_url: Optional[HttpUrl] = None
    skills: List[str] = []
    interests: List[str] = []
    homeTown: str
    homeTown_GPS_Address: str
    internships: List[PyObjectId] = []  # List of internship IDs
    projects: List[Dict[str, Any]] = []
    department_id: PyObjectId
    programme_id: PyObjectId
    zone_id: PyObjectId  # New field to associate student with a zone
    current_location: Optional[Address] = None  # New field for real-time location
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

  

class ChatMessage(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    sender_id: PyObjectId
    receiver_id: PyObjectId
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    read: bool = False
    read_at: Optional[datetime] = None

class ChatRoom(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    participants: List[PyObjectId]  # List of user IDs
    messages: List[PyObjectId]  # List of message IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ZoneChat(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    zone_id: PyObjectId
    participants: List[PyObjectId]  # List of supervisor IDs in this zone
    messages: List[PyObjectId]  # List of message IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Rating(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    company_id: PyObjectId
    internship_id: PyObjectId
    rating_score: float = Field(..., ge=0, le=5)  # Rating from 0 to 5
    comments: str
    rating_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WhiteList(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    company_id: PyObjectId
    internship_id: PyObjectId
    comments: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
