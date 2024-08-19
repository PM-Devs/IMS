# Comprehensive Internship Management System (IMS) Architecture

## Backend Design

### Technology Stack

- **Backend Framework:** FastAPI (Python)
- **Database:** MongoDB
- **Authentication:** JWT (JSON Web Tokens)
- **Middleware:** Custom middleware for logging, authentication, and request validation

### Architecture Overview

The IMS backend architecture is structured to ensure scalability, modularity, and efficiency. The architecture is designed as follows:

```plaintext
Client (Frontend)
    |
    V
Backend (FastAPI)
    |
    |-- Middleware Layer
    |     |-- Logging Middleware
    |     |-- Authentication Middleware
    |     |-- Request Validation Middleware
    |
    |-- API Layer
    |     |-- User API
    |     |-- Student API
    |     |-- Company API
    |     |-- Internship API
    |     |-- Staff API
    |     |-- Attachy Assistant API
    |
    |-- Service Layer
    |     |-- User Service
    |     |-- Student Service
    |     |-- Company Service
    |     |-- Internship Service
    |     |-- Staff Service
    |     |-- Attachy Assistant Service
    |
    |-- Data Access Layer
          |-- User Repository
          |-- Student Repository
          |-- Company Repository
          |-- Internship Repository
          |-- Staff Repository
          |-- Attachy Assistant Logs Repository
    |
    V
MongoDB Database
```

### Middleware

#### Logging Middleware

- **Purpose:** Logs each request and response for monitoring and debugging.
- **Functionality:** Captures details such as HTTP method, URL, and status codes.

#### Authentication Middleware

- **Purpose:** Secures the system by verifying JWT tokens.
- **Functionality:** Ensures that only authenticated users can access protected routes.

#### Request Validation Middleware

- **Purpose:** Validates the structure and content of incoming requests.
- **Functionality:** Ensures that requests contain required fields and that data types are correct before they proceed to the API layer.

### API Layer

- **Purpose:** Defines the endpoints and routes that the frontend interacts with.
- **Components:**
  - **User API:** Handles user-related operations such as registration and login.
  - **Student API:** Manages student data, applications, and progress logs.
  - **Company API:** Manages company profiles and internship postings.
  - **Internship API:** Handles the entire lifecycle of internship placements.
  - **Staff API:** Manages university staff and supervision processes.
  - **Attachy Assistant API:** Integrates the NLP-powered assistant for user support.

### Service Layer

- **Purpose:** Contains the business logic that governs how data is processed and operations are handled.
- **Components:**
  - **User Service:** Manages user authentication, registration, and profile updates.
  - **Student Service:** Orchestrates the student application process, logbook management, and report submissions.
  - **Company Service:** Oversees company interactions with the system, including internship management and intern evaluations.
  - **Internship Service:** Handles the end-to-end process of internship placements, from posting to supervision.
  - **Staff Service:** Manages the allocation of supervisors, evaluation processes, and grading.
  - **Attachy Assistant Service:** Powers the NLP assistant that aids users in navigating the system and completing tasks.

### Data Access Layer

- **Purpose:** Facilitates the interaction with the MongoDB database for CRUD operations.
- **Components:**
  - **User Repository:** Handles all operations related to user data.
  - **Student Repository:** Manages the storage and retrieval of student-related data.
  - **Company Repository:** Manages company profiles and internship opportunities.
  - **Internship Repository:** Stores internship data, including applications, placements, and evaluations.
  - **Staff Repository:** Maintains records of staff members and their supervisory roles.
  - **Attachy Assistant Logs Repository:** Stores interaction logs for the Attachy assistant for analysis and improvement.

### Example of a FastAPI Middleware

Here's a sample FastAPI middleware that logs incoming requests and responses:

```python
from fastapi import FastAPI, Request
import logging

app = FastAPI()

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("ims_logger")
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Example API Route
@app.get("/students")
async def get_students():
    return {"message": "List of students"}
```

## Frontend Design

### Technology Stack

- **Frontend Framework:** React.js
- **State Management:** Redux
- **UI Framework:** Material-UI
- **API Client:** Axios
- **Routing:** React Router

### Architecture Overview

The IMS frontend architecture is designed to ensure a seamless user experience with clear separation of concerns:

```plaintext
React Application
    |
    |-- Components
    |     |-- User Components
    |     |-- Student Components
    |     |-- Company Components
    |     |-- Internship Components
    |     |-- Staff Components
    |     |-- Attachy Assistant Components
    |
    |-- State Management (Redux)
    |     |-- Actions
    |     |-- Reducers
    |     |-- Store
    |
    |-- API Client (Axios)
    |     |-- API Endpoints
    |
    |-- Routing (React Router)
          |-- Public Routes
          |-- Private Routes
          |-- Role-Based Routes
```

### Components

- **User Components:** Manage user registration, login, and profile management.
- **Student Components:** Handle student-specific views such as application forms, daily logs, and report submissions.
- **Company Components:** Facilitate company registration, internship postings, and applicant management.
- **Internship Components:** Provide interfaces for browsing, applying to, and managing internships.
- **Staff Components:** Provide tools for supervisors and ILO staff to monitor and evaluate student performance.
- **Attachy Assistant Components:** Enable interaction with the NLP assistant for user support.

### State Management (Redux)

- **Actions:** Define the types of actions that can be dispatched to the store, such as logging in or fetching internships.
- **Reducers:** Handle state transitions based on the dispatched actions, managing the application’s state.
- **Store:** Holds the overall state of the application, ensuring that data flows consistently through the app.

### API Client (Axios)

- **Purpose:** Manages all HTTP requests to the backend API.
- **Functionality:** Defines API endpoints and handles request/response logic, including error handling.

### Routing (React Router)

- **Public Routes:** Accessible to all users, e.g., login and registration pages.
- **Private Routes:** Restricted to authenticated users, e.g., dashboard and profile pages.
- **Role-Based Routes:** Further restricts access based on the user’s role, ensuring only authorized users can access specific sections, e.g., admin pages.

This architecture is designed to deliver a robust, scalable, and maintainable Internship Management System that meets the needs of all stakeholders involved.