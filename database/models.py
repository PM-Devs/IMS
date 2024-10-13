from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict, GetCoreSchemaHandler
from typing import Any, Dict, Optional, List, Annotated
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema

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
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True  # Allows population by alias
    )


class Coordinate(BaseModelWithConfig):
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Address(BaseModelWithConfig):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    coordinate: Optional[Coordinate] = None

class Zone(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    boundaries: Optional[List[Coordinate]] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Area(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    boundaries: Optional[List[Coordinate]] = None
    zone_id: Optional[PyObjectId] = None
    supervisors: Optional[List[PyObjectId]] = None
    students: Optional[List[PyObjectId]] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ContactInfo(BaseModelWithConfig):
    phone: Optional[str] = None
    alternative_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    alternative_email: Optional[EmailStr] = None

class Department(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    name: Optional[str] = None
    faculty_id: Optional[PyObjectId] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Faculty(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Programme(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    name: Optional[str] = None
    department_id: Optional[PyObjectId] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class User(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    role: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture: Optional[str] = None
    contact_info: Optional[ContactInfo] = None
    address: Optional[Address] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class AcademicInfo(BaseModelWithConfig):
    institution: Optional[str] = None
    degree: Optional[str] = None
    major: Optional[str] = None
    year_of_study: Optional[int] = None
    gpa: Optional[float] = None

class Company(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    user_id: Optional[PyObjectId] = None
    company_name: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    year_founded: Optional[int] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    address: Optional[Address] = None
    contact_info: Optional[ContactInfo] = None
    internships_posted: Optional[List[PyObjectId]] = None
    company_supervisors: Optional[List[PyObjectId]] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Internship(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    company_id: Optional[PyObjectId] = None
    title: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    location: Optional[Address] = None
    industry: Optional[str] = None
    internship_type: Optional[str] = None
    duration: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    stipend: Optional[float] = None
    application_deadline: Optional[datetime] = None
    max_applications: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Application(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    student_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    status: Optional[str] = None
    application_date: Optional[datetime] = None
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    acceptance_date: Optional[datetime] = None
    rejection_date: Optional[datetime] = None
    withdrawal_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class EvaluationCriteria(BaseModelWithConfig):
    criterion: Optional[str] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    weight: Optional[float] = None

class Evaluation(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    application_id: Optional[PyObjectId] = None
    supervisor_id: Optional[PyObjectId] = None
    evaluation_type: Optional[str] = None
    evaluation_date: Optional[datetime] = None
    criteria: Optional[List[EvaluationCriteria]] = None
    total_score: Optional[float] = None
    max_total_score: Optional[float] = None
    comments: Optional[str] = None
    strengths: Optional[List[str]] = None
    areas_for_improvement: Optional[List[str]] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Notification(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    user_id: Optional[PyObjectId] = None
    title: Optional[str] = None
    description: Optional[str] = None
    notification_type: Optional[str] = None
    picture_url: Optional[str] = None
    link: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    read: Optional[bool] = False
    read_at: Optional[datetime] = None

class VisitLocation(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    supervisor_id: Optional[PyObjectId] = None
    student_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    company_id: Optional[PyObjectId] = None
    source_location: Optional[Address] = None
    destination_location: Optional[Address] = None
    visit_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class AppCredentials(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    app_id: Optional[str] = None
    app_key: Optional[str] = None
    app_name: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    is_active: Optional[bool] = True

class LogBookEntry(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    student_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    date: Optional[datetime] = None
    activities: Optional[List[str]] = None
    learning_outcomes: Optional[List[str]] = None
    challenges: Optional[str] = None
    hours_worked: Optional[float] = None
    status: Optional[str] = None
    supervisor_comments: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class MonthlySummary(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    student_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    month: Optional[str] = None
    summary: Optional[str] = None
    key_learnings: Optional[List[str]] = None
    challenges: Optional[str] = None
    goals_for_next_month: Optional[List[str]] = None
    status: Optional[str] = None
    supervisor_comments: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class FinalAssessment(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    student_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    assessment_date: Optional[datetime] = None
    final_report_url: Optional[HttpUrl] = None
    overall_performance: Optional[str] = None
    final_grade: Optional[float] = None
    supervisor_comments: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class AttachmentReport(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    student_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    submission_date: Optional[datetime] = None
    report_url: Optional[str] = None
    executive_summary: Optional[str] = None
    activities_summary: Optional[str] = None
    learnings: Optional[List[str]] = None
    challenges: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    status: Optional[str] = None
    department_comments: Optional[str] = None
    final_grade: Optional[float] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Token(BaseModelWithConfig):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_at: Optional[datetime] = None

class SchoolSupervisor(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    user_id: Optional[PyObjectId] = None
    department_id: Optional[PyObjectId] = None
    position: Optional[str] = None
    assigned_students: Optional[List[PyObjectId]] = None
    qualifications: Optional[List[str]] = None
    areas_of_expertise: Optional[List[str]] = None
    zone_id: Optional[PyObjectId] = None
    area_id: Optional[PyObjectId] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Student(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    user_id: Optional[PyObjectId] = None
    registration_number: Optional[str] = None
    academic_info: Optional[AcademicInfo] = None
    resume_url: Optional[str] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    homeTown: Optional[str] = None
    homeTown_GPS_Address: Optional[str] = None
    internships: Optional[List[PyObjectId]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    department_id: Optional[PyObjectId] = None
    programme_id: Optional[PyObjectId] = None
    zone_id: Optional[PyObjectId] = None
    area_id: Optional[PyObjectId] = None
    current_location: Optional[Coordinate] = None
    assigned_supervisor: Optional[PyObjectId] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ChatMessage(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    sender_id: Optional[PyObjectId] = None
    receiver_id: Optional[PyObjectId] = None
    content: Optional[str] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    read: Optional[bool] = False
    read_at: Optional[datetime] = None

class ChatRoom(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    participants: Optional[List[PyObjectId]] = None
    messages: Optional[List[PyObjectId]] = None
    room_type: Optional[str] = None
    zone_id: Optional[PyObjectId] = None
    area_id: Optional[PyObjectId] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class WhiteList(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    company_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    comments: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Rating(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    student_id: Optional[PyObjectId] = None
    company_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    rating_score: Optional[float] = Field(None, ge=0, le=5)
    comments: Optional[str] = None
    rating_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Resource(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    resource_type: Optional[str] = None
    url: Optional[str] = None
    uploaded_by: Optional[PyObjectId] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class AssumptionOfDuty(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    student_id: Optional[PyObjectId] = None
    internship_id: Optional[PyObjectId] = None
    file_path: Optional[str] = None
    submission_date: Optional[datetime] = None
    status: Optional[str] = "Submitted"
    reviewer_id: Optional[PyObjectId] = None
    review_date: Optional[datetime] = None
    comments: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class SupervisorDistribution(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    zone_id: Optional[PyObjectId] = None
    area_id: Optional[PyObjectId] = None
    supervisor_id: Optional[PyObjectId] = None
    assigned_students: Optional[List[PyObjectId]] = None
    total_students: Optional[int] = None
    correlation_score: Optional[float] = None
    supervision_time: Optional[float] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class DistributionRun(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    run_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    total_supervisors: Optional[int] = None
    total_students: Optional[int] = None
    distribution_results: Optional[List[PyObjectId]] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class SupervisorWorkload(BaseModelWithConfig):
    id: Optional[Annotated[PyObjectId, Field(alias="_id")]] = None
    supervisor_id: Optional[PyObjectId] = None
    total_students: Optional[int] = None
    total_supervision_time: Optional[float] = None
    zones: Optional[List[PyObjectId]] = None
    areas: Optional[List[PyObjectId]] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)