# Comprehensive Internship Management System (IMS) Architecture

## Backend Design

### Technology Stack

- **Backend Framework:** Python - FastAPI
- **Database:** MongoDB
- **Authentication:** JWT (JSON Web Tokens)
- **Middleware:** Custom middleware for logging, authentication, and request validation

### Architecture

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

- Logs each request and response for monitoring and debugging purposes.

#### Authentication Middleware

- Verifies JWT tokens to ensure the user is authenticated before accessing protected routes.

#### Request Validation Middleware

- Validates incoming requests for required fields and correct data types.

### API Layer

Defines routes and endpoints for different functionalities, e.g., user registration, internship application, etc.

### Service Layer

Contains business logic and orchestrates data flow between the API layer and the data access layer.

### Data Access Layer

Interacts with MongoDB to perform CRUD operations.

### Example of a FastAPI Middleware

```python
from fastapi import FastAPI, Request
import logging

app = FastAPI()

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("my_logger")
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

### Architecture

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
    |-- Pages
    |     |-- Home Page
    |     |-- Login Page
    |     |-- Registration Page
    |     |-- Dashboard Page
    |     |-- Internship Search Page
    |     |-- Application Status Page
    |     |-- Staff Management Page
    |
    |-- Services
    |     |-- UserService
    |     |-- StudentService
    |     |-- CompanyService
    |     |-- InternshipService
    |     |-- StaffService
    |     |-- AttachyService
    |
    |-- State Management (Redux)
          |-- Actions
          |-- Reducers
          |-- Store
    |
    V
Backend API (FastAPI)
```

### Components

Reusable UI components for different parts of the application.

### Pages

Higher-level components representing different routes in the application.

### Services

Utility functions to make API calls using Axios.

### State Management

Uses Redux for managing global state, including actions, reducers, and the store.

### Example of a React Component

```jsx
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchInternships } from '../actions/internshipActions';
import InternshipCard from '../components/InternshipCard';

const InternshipSearchPage = () => {
    const dispatch = useDispatch();
    const internships = useSelector(state => state.internships);

    useEffect(() => {
        dispatch(fetchInternships());
    }, [dispatch]);

    return (
        <div>
            <h1>Search Internships</h1>
            <div>
                {internships.map(internship => (
                    <InternshipCard key={internship.id} internship={internship} />
                ))}
            </div>
        </div>
    );
};

export default InternshipSearchPage;
```

### Example of Axios Service

```jsx
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const fetchInternships = async () => {
    const response = await axios.get(`${API_URL}/internships`);
    return response.data;
};

export default fetchInternships;
```

## Summary

The IMS system will use FastAPI for the backend, MongoDB for the database, and React.js for the frontend. The backend will have middleware for logging, authentication, and request validation. The frontend will use Redux for state management and Axios for API calls. This architecture ensures a scalable, maintainable, and efficient internship management system.
