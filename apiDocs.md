# Sample responses and explanations for Supervisor API endpoints

# 1. Login endpoint
@app.post("/login")
async def login_for_access_token(request: CustomLoginRequest):
    # Sample response
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "expires_at": "2023-09-01T12:00:00Z"
    }
    # Explanation: This endpoint authenticates the user and returns an access token,
    # which is used for subsequent API calls. The token includes an expiration time.

# 2. Dashboard endpoint
@app.get("/dashboard")
async def dashboard(current_user: User = Depends(service.get_current_active_supervisor)):
    # Sample response
    {
        "assigned_students": 15,
        "pending_evaluations": 3,
        "upcoming_visits": 2,
        "recent_logbook_entries": [
            {"student_name": "John Doe", "date": "2023-08-30", "status": "Pending Review"},
            {"student_name": "Jane Smith", "date": "2023-08-29", "status": "Approved"}
        ]
    }
    # Explanation: This endpoint provides an overview of the supervisor's current workload
    # and recent activities, including the number of assigned students, pending tasks,
    # and recent student submissions.

# 3. Search students endpoint
@app.get("/students/search")
async def search_students_endpoint(query: str, current_user: User = Depends(service.get_current_active_supervisor)):
    # Sample response
    [
        {
            "id": "60d5ecb8e6e8f32b9811f789",
            "name": "John Doe",
            "registration_number": "S12345",
            "programme": "Computer Science",
            "internship_status": "Ongoing"
        },
        {
            "id": "60d5ecb8e6e8f32b9811f790",
            "name": "Jane Smith",
            "registration_number": "S12346",
            "programme": "Electrical Engineering",
            "internship_status": "Completed"
        }
    ]
    # Explanation: This endpoint allows supervisors to search for students based on a query string.
    # It returns a list of matching students with basic information.

# 4. Update student status endpoint
@app.put("/students/{student_id}/status")
async def update_student_status_endpoint(student_id: str, status: str, current_user: User = Depends(service.get_current_active_supervisor)):
    # Sample response
    {
        "id": "60d5ecb8e6e8f32b9811f789",
        "name": "John Doe",
        "registration_number": "S12345",
        "new_status": "Completed",
        "updated_at": "2023-09-01T10:30:00Z"
    }
    # Explanation: This endpoint allows supervisors to update a student's internship status.
    # It returns the updated student information, including the new status and update timestamp.

# 5. Create visit location endpoint
@app.post("/visit-locations")
async def create_visit_location_endpoint(visit_data: dict, current_user: User = Depends(service.get_current_active_supervisor)):
    # Sample response
    {
        "id": "60d5ecb8e6e8f32b9811f791",
        "student_id": "60d5ecb8e6e8f32b9811f789",
        "company_id": "60d5ecb8e6e8f32b9811f792",
        "visit_date": "2023-09-15T14:00:00Z",
        "status": "Scheduled",
        "notes": "First visit to discuss project progress"
    }
    # Explanation: This endpoint allows supervisors to create a new visit location for student supervision.
    # It returns the details of the created visit, including its ID and scheduled date.

# 6. Mark logbook entry endpoint
@app.put("/logs/{logbook_id}/mark")
async def mark_logbook_entry(logbook_id: str, status: str, comments: Optional[str] = None, current_user: User = Depends(service.get_current_active_supervisor)):
    # Sample response
    {
        "id": "60d5ecb8e6e8f32b9811f793",
        "student_id": "60d5ecb8e6e8f32b9811f789",
        "date": "2023-08-30",
        "status": "Approved",
        "supervisor_comments": "Great progress on the project. Keep up the good work!",
        "marked_at": "2023-09-01T11:45:00Z"
    }
    # Explanation: This endpoint allows supervisors to mark a student's logbook entry.
    # It returns the updated logbook entry information, including the new status and any comments added.

# 7. Create evaluation endpoint
@app.post("/evaluations")
async def create_evaluation_endpoint(student_id: str, evaluation_data: dict, current_user: User = Depends(service.get_current_active_supervisor)):
    # Sample response
    {
        "id": "60d5ecb8e6e8f32b9811f794",
        "student_id": "60d5ecb8e6e8f32b9811f789",
        "evaluation_type": "Midterm",
        "total_score": 85.5,
        "max_total_score": 100,
        "comments": "Showing good progress and initiative. Communication skills need improvement.",
        "created_at": "2023-09-01T15:30:00Z"
    }
    # Explanation: This endpoint allows supervisors to create an evaluation for a student.
    # It returns the details of the created evaluation, including scores and comments.

# 8. Get zone chat messages endpoint
@app.get("/zones/{zone_id}/chat/messages")
async def get_zone_chat_messages_endpoint(zone_id: str, limit: int = 50, skip: int = 0, current_user: User = Depends(service.get_current_active_supervisor)):
    # Sample response
    {
        "zone_id": "60d5ecb8e6e8f32b9811f795",
        "messages": [
            {
                "id": "60d5ecb8e6e8f32b9811f796",
                "sender_id": "60d5ecb8e6e8f32b9811f797",
                "sender_name": "Alice Johnson",
                "content": "Has anyone visited Company XYZ recently?",
                "timestamp": "2023-09-01T09:30:00Z"
            },
            {
                "id": "60d5ecb8e6e8f32b9811f798",
                "sender_id": "60d5ecb8e6e8f32b9811f799",
                "sender_name": "Bob Smith",
                "content": "Yes, I was there last week. They have a great internship program.",
                "timestamp": "2023-09-01T09:35:00Z"
            }
        ],
        "total_messages": 2,
        "has_more": false
    }
    # Explanation: This endpoint retrieves chat messages for a specific zone.
    # It returns a list of messages with sender information and timestamps, as well as pagination details.