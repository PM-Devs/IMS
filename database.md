# Updated Database Design for Comprehensive Internship Management System (IMS)
---
## Collections and Schemas

### 1. Users

**Collection Name:** `users`

```json
{
  "user_id": "ObjectId",
  "role": "string",  // "student", "company", "school_supervisor", "company_supervisor", "department_staff", "ilo_staff"
  "email": "string",
  "password": "string",
  "profile": {
    "name": "string",
    "contact_number": "string",
    "address": "string",
    "additional_info": "string"
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 2. Students

**Collection Name:** `students`

```json
{
  "student_id": "ObjectId",
  "user_id": "ObjectId",
  "registration_number": "string",
  "academic_info": {
    "faculty": "string",
    "department": "string",
    "program": "string",
    "year_of_study": "number"
  },
  "resume_url": "string",
  "internships": [
    {
      "internship_id": "ObjectId",
      "status": "string",  // "applied", "accepted", "in_progress", "completed"
      "application_date": "datetime",
      "start_date": "datetime",
      "end_date": "datetime",
      "company_supervisor_id": "ObjectId",
      "school_supervisor_id": "ObjectId"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 3. Companies

**Collection Name:** `companies`

```json
{
  "company_id": "ObjectId",
  "user_id": "ObjectId",
  "company_name": "string",
  "industry": "string",
  "location": "string",
  "postal_address": "string",
  "contact_person": {
    "name": "string",
    "email": "string",
    "phone": "string"
  },
  "internships_posted": ["ObjectId"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 4. Internships

**Collection Name:** `internships`

```json
{
  "internship_id": "ObjectId",
  "company_id": "ObjectId",
  "title": "string",
  "description": "string",
  "location": "string",
  "industry": "string",
  "duration": "string",
  "requirements": "string",
  "application_deadline": "datetime",
  "status": "string",  // "open", "closed", "in_progress", "completed"
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 5. Applications

**Collection Name:** `applications`

```json
{
  "application_id": "ObjectId",
  "student_id": "ObjectId",
  "internship_id": "ObjectId",
  "status": "string",  // "applied", "accepted", "rejected", "in_progress", "completed"
  "application_date": "datetime",
  "acceptance_date": "datetime",
  "start_date": "datetime",
  "end_date": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 6. Daily Logs

**Collection Name:** `daily_logs`

```json
{
  "log_id": "ObjectId",
  "student_id": "ObjectId",
  "internship_id": "ObjectId",
  "date": "datetime",
  "activities": "string",
  "status": "string",  // "draft", "submitted", "approved"
  "supervisor_comments": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 7. Monthly Summaries

**Collection Name:** `monthly_summaries`

```json
{
  "summary_id": "ObjectId",
  "student_id": "ObjectId",
  "internship_id": "ObjectId",
  "month": "number",
  "year": "number",
  "content": "string",
  "status": "string",  // "draft", "submitted", "approved"
  "supervisor_comments": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 8. Supervisors

**Collection Name:** `supervisors`

```json
{
  "supervisor_id": "ObjectId",
  "user_id": "ObjectId",
  "type": "string",  // "school", "company"
  "department": "string",  // for school supervisors
  "company_id": "ObjectId",  // for company supervisors
  "assigned_students": ["ObjectId"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 9. Evaluations

**Collection Name:** `evaluations`

```json
{
  "evaluation_id": "ObjectId",
  "application_id": "ObjectId",
  "supervisor_id": "ObjectId",
  "evaluation_type": "string",  // "mid-term", "final"
  "criteria": [
    {
      "name": "string",
      "score": "number",
      "max_score": "number",
      "comments": "string"
    }
  ],
  "total_score": "number",
  "comments": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 10. Departments

**Collection Name:** `departments`

```json
{
  "department_id": "ObjectId",
  "name": "string",
  "faculty": "string",
  "head_of_department": "ObjectId",  // reference to user_id
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 11. Industrial Liaison Office

**Collection Name:** `industrial_liaison_office`

```json
{
  "ilo_id": "ObjectId",
  "staff": [
    {
      "user_id": "ObjectId",
      "role": "string"  // "director", "admin", "officer"
    }
  ],
  "grading_scales": [
    {
      "component": "string",
      "weight": "number"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 12. GPS Logs

**Collection Name:** `gps_logs`

```json
{
  "log_id": "ObjectId",
  "supervisor_id": "ObjectId",
  "internship_id": "ObjectId",
  "timestamp": "datetime",
  "latitude": "number",
  "longitude": "number",
  "created_at": "datetime"
}
```

### 13. Final Reports

**Collection Name:** `final_reports`

```json
{
  "report_id": "ObjectId",
  "student_id": "ObjectId",
  "internship_id": "ObjectId",
  "report_url": "string",
  "submission_date": "datetime",
  "status": "string",  // "submitted", "under_review", "graded"
  "department_grade": "number",
  "comments": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Relationships

1. **Users to Students/Companies/Supervisors/Staff:**
   - One-to-One relationship between `users` and `students`/`companies`/`supervisors`/`department_staff`/`ilo_staff`.

2. **Companies to Internships:**
   - One-to-Many relationship between `companies` and `internships`.

3. **Students to Internships:**
   - Many-to-Many relationship between `students` and `internships` through `applications`.

4. **Supervisors to Students:**
   - One-to-Many relationship between `supervisors` and `students`.

5. **Applications to Daily Logs and Monthly Summaries:**
   - One-to-Many relationship between `applications` and `daily_logs`/`monthly_summaries`.

6. **Applications to Evaluations:**
   - One-to-Many relationship between `applications` and `evaluations`.

7. **Departments to Students and Supervisors:**
   - One-to-Many relationship between `departments` and `students`/`supervisors`.

8. **Industrial Liaison Office to All Entities:**
   - One-to-Many relationship between `industrial_liaison_office` and all other entities for oversight.

9. **Supervisors to GPS Logs:**
   - One-to-Many relationship between `supervisors` and `gps_logs`.

10. **Students to Final Reports:**
    - One-to-One relationship between `students` and `final_reports` for each internship.

