# Database Design for Comprehensive Internship Management System (IMS)

## Collections and Schemas

### 1. Users

**Collection Name:** `users`

**Schema:**

```json
{
  "user_id": "ObjectId",
  "role": "string",  // "student", "company", "staff"
  "email": "string",
  "password": "string",
  "profile": {
    "name": "string",
    "contact_number": "string",
    "address": "string",
    "additional_info": "string",
    "documents": [
      {
        "document_id": "ObjectId",
        "document_name": "string",
        "document_url": "string"
      }
    ]
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 2. Students

**Collection Name:** `students`

**Schema:**

```json
{
  "student_id": "ObjectId",
  "user_id": "ObjectId",
  "academic_background": {
    "degree": "string",
    "department": "string",
    "year_of_study": "number",
    "cgpa": "number"
  },
  "resume_url": "string",
  "applied_internships": [
    {
      "internship_id": "ObjectId",
      "application_status": "string",  // "applied", "in_progress", "completed", "rejected"
      "application_date": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 3. Companies

**Collection Name:** `companies`

**Schema:**

```json
{
  "company_id": "ObjectId",
  "user_id": "ObjectId",
  "company_name": "string",
  "industry": "string",
  "location": "string",
  "contact_person": {
    "name": "string",
    "email": "string",
    "phone": "string"
  },
  "internships_posted": [
    {
      "internship_id": "ObjectId",
      "posting_date": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 4. Internships

**Collection Name:** `internships`

**Schema:**

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
  "applications": [
    {
      "student_id": "ObjectId",
      "status": "string",  // "applied", "in_progress", "completed", "rejected"
      "application_date": "datetime",
      "progress_reports": [
        {
          "report_id": "ObjectId",
          "submission_date": "datetime",
          "content": "string"
        }
      ],
      "evaluations": [
        {
          "evaluation_id": "ObjectId",
          "evaluation_date": "datetime",
          "comments": "string",
          "rating": "number"
        }
      ]
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 5. Staff

**Collection Name:** `staff`

**Schema:**

```json
{
  "staff_id": "ObjectId",
  "user_id": "ObjectId",
  "role": "string",  // "coordinator", "advisor", "admin"
  "assigned_internships": [
    {
      "internship_id": "ObjectId",
      "assignment_date": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 6. Attachy Assistant Logs

**Collection Name:** `attachy_logs`

**Schema:**

```json
{
  "log_id": "ObjectId",
  "user_id": "ObjectId",
  "query": "string",
  "response": "string",
  "timestamp": "datetime"
}
```

## Relationships

1. **Users to Students/Companies/Staff:**
   - One-to-One relationship between `users` and `students`.
   - One-to-One relationship between `users` and `companies`.
   - One-to-One relationship between `users` and `staff`.

2. **Companies to Internships:**
   - One-to-Many relationship between `companies` and `internships`.

3. **Students to Internships:**
   - Many-to-Many relationship between `students` and `internships` through `applications`.

4. **Staff to Internships:**
   - Many-to-Many relationship between `staff` and `internships` through `assigned_internships`.

5. **Internships to Applications:**
   - One-to-Many relationship between `internships` and `applications` (embedded within `internships`).

6. **Internships to Progress Reports and Evaluations:**
   - One-to-Many relationship between `applications` and `progress_reports` (embedded within `applications`).
   - One-to-Many relationship between `applications` and `evaluations` (embedded within `applications`).

This database design ensures efficient management of the IMS, supporting all required functionalities and maintaining data integrity and relationships.
