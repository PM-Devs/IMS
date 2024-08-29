from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict
from typing import Any, Dict, Optional, List, Annotated
from datetime import datetime

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

class User(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    role: str
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

class Student(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    user_id: PyObjectId
    registration_number: str
    academic_info: AcademicInfo
    resume_url: Optional[HttpUrl] = None
    skills: List[str] = []
    interests: List[str] = []
    internships: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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
    internships_posted: List[PyObjectId] = []
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
    status: str
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

class Supervisor(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    user_id: PyObjectId
    type: str
    department: Optional[str] = None
    position: str
    company_id: Optional[PyObjectId] = None
    assigned_students: List[PyObjectId] = []
    qualifications: List[str] = []
    areas_of_expertise: List[str] = []
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
    evaluation_type: str
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
    notification_type: str
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
    status: str
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

class DailyLog(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    internship_id: PyObjectId
    date: datetime
    activities: List[str]
    learning_outcomes: List[str]
    challenges: Optional[str] = None
    hours_worked: float
    status: str
    supervisor_comments: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WeeklyReport(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    internship_id: PyObjectId
    week_start_date: datetime
    week_end_date: datetime
    summary: str
    key_learnings: List[str]
    challenges: Optional[str] = None
    goals_for_next_week: List[str]
    status: str
    supervisor_comments: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class FinalReport(BaseModelWithConfig):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    student_id: PyObjectId
    internship_id: PyObjectId
    submission_date: datetime
    report_url: HttpUrl
    executive_summary: str
    learnings: List[str]
    challenges: List[str]
    recommendations: List[str]
    status: str
    supervisor_comments: Optional[str] = None
    grade: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Token(BaseModelWithConfig):
    access_token: str
    token_type: str
    expires_at: datetime