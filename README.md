# Comprehensive Internship Management System (IMS)

## Introduction

The Comprehensive Internship Management System (IMS) is a web-based application designed to streamline the internship management process for students, companies, and university staff. This system provides a centralized platform for managing internship applications, monitoring progress, and providing support through advanced technologies such as Natural Language Processing (NLP).

## Table of Contents

1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Contributing](#contributing)
7. [License](#license)

## Features

- **Student Management**: Register, create, and manage student profiles.
- **Internship Search and Application**: Advanced search engine for finding and applying for internships.
- **Company Management**: Register companies and post internship opportunities.
- **Application Tracking and Monitoring**: Track and monitor internship applications.
- **Progress Reporting and Evaluation**: Submit progress reports and evaluations.
- **Staff Support and System Administration**: Tools for managing the system and supporting users.
- **GPS and Route Navigation**: Navigation tools for staff to locate and travel to internship sites.
- **Attachy Assistant**: NLP-powered assistant to support users with queries and guidance.

## Technology Stack

### Backend

- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)

### Frontend

- **Framework**: React.js
- **State Management**: Redux
- **UI Framework**: Tailwindjs
- **API Client**: Axios
- **Routing**: React Router

## Installation

### Prerequisites

- Python 3.8+
- Node.js and npm
- MongoDB

### Backend Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/ims.git
    cd ims/backend
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```

### Frontend Setup

1. Navigate to the frontend directory:
    ```sh
    cd ../frontend
    ```

2. Install dependencies:
    ```sh
    npm install
    ```

3. Start the React development server:
    ```sh
    npm start
    ```

## Usage

Once both the backend and frontend servers are running, open your web browser and navigate to `http://localhost:3000` to access the IMS application.

## API Endpoints

### User API

- **POST /api/users/register**: Register a new user.
- **POST /api/users/login**: User login.

### Student API

- **GET /api/students**: Get a list of students.
- **POST /api/students**: Create a new student profile.
- **PUT /api/students/{id}**: Update student profile.
- **DELETE /api/students/{id}**: Delete student profile.

### Company API

- **GET /api/companies**: Get a list of companies.
- **POST /api/companies**: Create a new company profile.
- **PUT /api/companies/{id}**: Update company profile.
- **DELETE /api/companies/{id}**: Delete company profile.

### Internship API

- **GET /api/internships**: Get a list of internships.
- **POST /api/internships**: Post a new internship.
- **PUT /api/internships/{id}**: Update internship details.
- **DELETE /api/internships/{id}**: Delete internship.

### Staff API

- **GET /api/staff**: Get a list of staff.
- **POST /api/staff**: Add a new staff member.
- **PUT /api/staff/{id}**: Update staff details.
- **DELETE /api/staff/{id}**: Delete staff member.

### Attachy Assistant API

- **POST /api/attachy/query**: Query the Attachy assistant.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

