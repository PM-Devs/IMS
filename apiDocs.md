
## API Documentation

### Authentication

#### Login for Access Token

**Endpoint:** `POST /login`

**Headers:**
```json
{
  "X-App-ID": "your-app-id",
  "X-App-Key": "your-app-key"
}
```

**Request:**
```javascript
const login = async (username, password) => {
  try {
    const response = await axios.post('/login', null, {
      headers: {
        'X-App-ID': 'your-app-id',
        'X-App-Key': 'your-app-key'
      },
      auth: {
        username: username,
        password: password
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
};
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_at": "2024-08-29T12:34:56Z"
}
```

#### Logout

**Endpoint:** `POST /logout`

**Headers:**
```json
{
  "X-App-ID": "your-app-id",
  "X-App-Key": "your-app-key",
  "Authorization": "Bearer your-access-token"
}
```

**Request:**
```javascript
const logout = async (accessToken) => {
  try {
    const response = await axios.post('/logout', null, {
      headers: {
        'X-App-ID': 'your-app-id',
        'X-App-Key': 'your-app-key',
        'Authorization': `Bearer ${accessToken}`
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
};
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

### Supervisor

#### Get Dashboard

**Endpoint:** `GET /dashboard`

**Headers:**
```json
{
  "X-App-ID": "your-app-id",
  "X-App-Key": "your-app-key",
  "Authorization": "Bearer your-access-token"
}
```

**Request:**
```javascript
const getDashboard = async (accessToken) => {
  try {
    const response = await axios.get('/dashboard', {
      headers: {
        'X-App-ID': 'your-app-id',
        'X-App-Key': 'your-app-key',
        'Authorization': `Bearer ${accessToken}`
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
};
```

**Response:**
```json
{
  "location": "Department of Computer Science",
  "total_students": 15,
  "completed_supervisions": 10,
  "pending_supervisions": 5,
  "students": [
    {
      "id": "student_id",
      "first_name": "John",
      "last_name": "Doe",
      "contact_info": {
        "phone": "123-456-7890"
      },
      "academic_info": {
        "institution": "University",
        "degree": "BSc",
        "major": "Computer Science",
        "year_of_study": 3,
        "gpa": 3.5
      },
      "status": "Active"
    }
  ],
  "notifications": [
    {
      "id": "notification_id",
      "message": "New student assigned",
      "timestamp": "2024-08-29T12:34:56Z"
    }
  ]
}

```

#### Search Students

**Endpoint:** `GET /students/search`

**Headers:**
```json
{
  "X-App-ID": "your-app-id",
  "X-App-Key": "your-app-key",
  "Authorization": "Bearer your-access-token"
}
```

**Request:**
```javascript
const searchStudents = async (query, accessToken) => {
  try {
    const response = await axios.get('/students/search', {
      params: { query: query },
      headers: {
        'X-App-ID': 'your-app-id',
        'X-App-Key': 'your-app-key',
        'Authorization': `Bearer ${accessToken}`
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
};
```

**Response:**
```json
[
  {
    "id": "student_id",
    "registration_number": "123456",
    "academic_info": {
      "institution": "University",
      "degree": "BSc",
      "major": "Computer Science",
      "year_of_study": 3,
      "gpa": 3.5
    },
    "skills": ["JavaScript", "React"],
    "interests": ["AI", "Blockchain"],
    "internships": [
      {
        "company": "Tech Inc",
        "role": "Intern",
        "duration": "3 months"
      }
    ],
    "projects": [
      {
        "title": "Portfolio Website",
        "description": "A personal website built with React."
      }
    ],
    "created_at": "2024-08-29T12:34:56Z",
    "updated_at": "2024-08-29T12:34:56Z"
  }
]
```

#### Get Student List

**Endpoint:** `GET /students`

**Headers:**
```json
{
  "X-App-ID": "your-app-id",
  "X-App-Key": "your-app-key",
  "Authorization": "Bearer your-access-token"
}
```

**Request:**
```javascript
const getStudentList = async (status, accessToken) => {
  try {
    const response = await axios.get('/students', {
      params: { status: status },
      headers: {
        'X-App-ID': 'your-app-id',
        'X-App-Key': 'your-app-key',
        'Authorization': `Bearer ${accessToken}`
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
};
```

**Response:**
```json
[
  {
    "id": "student_id",
    "registration_number": "123456",
    "academic_info": {
      "institution": "University",
      "degree": "BSc",
      "major": "Computer Science",
      "year_of_study": 3,
      "gpa": 3.5
    },
    "skills": ["JavaScript", "React"],
    "interests": ["AI", "Blockchain"],
    "internships": [
      {
        "company": "Tech Inc",
        "role": "Intern",
        "duration": "3 months"
      }
    ],
    "projects": [
      {
        "title": "Portfolio Website",
        "description": "A personal website built with React."
      }
    ],
    "created_at": "2024-08-29T12:34:56Z",
    "updated_at": "2024-08-29T12:34:56Z"
  }
]
```

### Visit Locations

#### Get Visit Locations

**Endpoint:** `GET /visit-locations`

**Headers:**
```json
{
  "X-App-ID": "your-app-id",
  "X-App-Key": "your-app-key",
  "Authorization": "Bearer your-access-token"
}
```

**Request:**
```javascript
const getVisitLocations = async (accessToken) => {
  try {
    const response = await axios.get('/visit-locations', {
      headers: {
        'X-App-ID': 'your-app-id',
        'X-App-Key': 'your-app-key',
        'Authorization': `Bearer ${accessToken}`
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
};
```

**Response:**
```json
[
  {
    "id": "visit_location_id",
    "supervisor_id": "supervisor_id",
    "student_id": "student_id",
    "internship_id": "internship_id",
    "company_id": "company_id",
    "source_location": {
      "street": "123 Main St",
      "city": "City",
      "state": "State",
      "country": "Country",
      "postal_code": "12345"
    },
    "destination_location": {
      "street": "456 Elm St",
      "city": "City",
      "state": "State",
      "country": "Country",
      "postal_code": "67890"
    },
    "visit_date": "2024-08-29T12:34:56Z",
    "status": "Completed",
    "notes": "Visited for progress review.",
    "created_at": "2024-08-29T12:34:56Z",
    "updated_at": "2024-08-29T12:34:56Z"
  }
]
```

#### Create Visit Location

**Endpoint:** `POST /visit-locations`

**Headers:**
```json
{
  "X-App-ID": "your-app-id",
  "X-App-Key": "your-app-key",
  "Authorization": "Bearer your-access-token",
  "Content-Type": "application/json"
}
```

**Request:**
```javascript
const createVisitLocation = async (visitLocation, accessToken) => {
  try {
    const response = await axios.post('/visit-locations', visitLocation, {
      headers: {
        'X-App-ID': 'your-app-id',
        'X-App-Key': 'your-app-key',
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
};
```

**Request Body:**
```json
{
  "supervisor_id": "supervisor_id",
  "student_id": "student_id",
  "internship_id": "internship_id",
  "company_id": "company_id",
  "source_location": {
    "street": "123 Main St",
    "city": "City",
    "state": "State",
    "country": "Country",
    "postal_code": "12345"
  },
  "destination_location": {
    "street": "456 Elm St",
    "city": "City",
    "state": "State",
    "country": "Country",
    "postal_code": "67890"
 

 },
  "visit_date": "2024-08-29T12:34:56Z",
  "status": "Completed",
  "notes": "Visited for progress review."
}
```

**Response:**
```json
{
  "id": "visit_location_id",
  "supervisor_id": "supervisor_id",
  "student_id": "student_id",
  "internship_id": "internship_id",
  "company_id": "company_id",
  "source_location": {
    "street": "123 Main St",
    "city": "City",
    "state": "State",
    "country": "Country",
    "postal_code": "12345"
  },
  "destination_location": {
    "street": "456 Elm St",
    "city": "City",
    "state": "State",
    "country": "Country",
    "postal_code": "67890"
  },
  "visit_date": "2024-08-29T12:34:56Z",
  "status": "Completed",
  "notes": "Visited for progress review.",
  "created_at": "2024-08-29T12:34:56Z",
  "updated_at": "2024-08-29T12:34:56Z"
}
```

