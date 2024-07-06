# Software Requirements Specification (SRS)

## Comprehensive Internship Management System (IMS)

### 1. Introduction

#### 1.1 Purpose

The purpose of this Software Requirements Specification (SRS) document is to provide a detailed description of the Comprehensive Internship Management System (IMS). This document will outline the system's functionalities, features, and constraints to ensure a clear understanding of the system's requirements and expected performance.

#### 1.2 Scope

The IMS is designed to streamline the internship management process for students, companies, and university staff. The system will provide a centralized platform for managing internship applications, monitoring progress, and providing support through advanced technologies such as Natural Language Processing (NLP). The key features of the IMS include:

- Student registration and profile management
- Internship search and application
- Company registration and internship posting
- Application tracking and management
- Progress reporting and evaluation
- Staff support and system administration
- GPS and route navigation for staff

#### 1.3 Definitions, Acronyms, and Abbreviations

- **IMS:** Internship Management System
- **NLP:** Natural Language Processing
- **Attachy:** NLP-powered assistant integrated into the IMS
- **GPS:** Global Positioning System

#### 1.4 References

- Project Proposal Overview Document
- Final Year Project - Chapter One Document

#### 1.5 Overview

This SRS document is organized into the following sections:

1. Introduction
2. Overall Description
3. System Features
4. External Interface Requirements
5. System Requirements
6. Other Non-Functional Requirements

### 2. Overall Description

#### 2.1 Product Perspective

The IMS will be a web-based application accessible through standard web browsers. It will integrate with existing university systems and databases to retrieve and store information. The system will use a modular architecture to ensure scalability and flexibility.

#### 2.2 Product Functions

The IMS will provide the following core functions:

- Student management
- Internship search and application
- Company management
- Application tracking and monitoring
- Progress reporting and evaluation
- Staff support and system administration
- GPS and route navigation for staff

#### 2.3 User Classes and Characteristics

- **Students:** Undergraduate and postgraduate students seeking internships.
- **Companies:** Organizations offering internship opportunities.
- **University Staff:** Internship coordinators, academic advisors, and administrative staff.

#### 2.4 Operating Environment

The IMS will operate in a web-based environment, accessible through modern web browsers on various devices, including desktops, laptops, tablets, and smartphones.

#### 2.5 Design and Implementation Constraints

- Integration with existing university systems and databases
- Compliance with data protection and privacy regulations
- High availability and performance requirements

#### 2.6 User Documentation

User manuals, online help, and video tutorials will be provided to guide users in using the system.

#### 2.7 Assumptions and Dependencies

- Users will have access to the internet and modern web browsers.
- The university will provide necessary APIs for system integration.

### 3. System Features

#### 3.1 Student Management

**Description:** Allows students to register, create, and manage their profiles, including personal information, academic background, and resumes.

**Functional Requirements:**

- Students can register and create profiles.
- Students can update personal and academic information.
- Students can upload and manage resumes and other documents.

#### 3.2 Internship Search and Application

**Description:** Provides a search engine with advanced filtering options for students to find and apply for internships.

**Functional Requirements:**

- Students can search for internships using various filters (e.g., location, industry, duration).
- Students can view detailed internship descriptions.
- Students can apply for internships directly through the platform.
- Students can track the status of their applications.

#### 3.3 Company Management

**Description:** Allows companies to register, create profiles, and post internship opportunities.

**Functional Requirements:**

- Companies can register and create profiles.
- Companies can post and manage internship opportunities.
- Companies can view and manage student applications.
- Companies can schedule and manage interviews with applicants.

#### 3.4 Application Tracking and Monitoring

**Description:** Enables students, companies, and staff to track and monitor the status of internship applications.

**Functional Requirements:**

- Students can view the status of their applications.
- Companies can update the status of student applications.
- Staff can monitor the application process and provide support as needed.

#### 3.5 Progress Reporting and Evaluation

**Description:** Allows students and companies to track and report progress throughout the internship.

**Functional Requirements:**

- Students can submit progress reports.
- Companies can provide feedback and evaluations.
- Staff can generate and review progress reports.

#### 3.6 Staff Support and System Administration

**Description:** Provides tools for university staff to manage the system, support users, and oversee the internship process.

**Functional Requirements:**

- Staff can manage student and company profiles.
- Staff can oversee internship postings and applications.
- Staff can generate reports and analytics.
- Staff can configure system settings and user access.

#### 3.7 GPS and Route Navigation

**Description:** Provides navigation tools for staff to locate and travel to internship sites.

**Functional Requirements:**

- Staff can view the location of internship sites.
- Staff can use GPS and route navigation to travel to sites.
- Staff can report or grade student performance on-site.

#### 3.8 Attachy Assistant

**Description:** Integrates an NLP-powered assistant to support users with queries and guidance.

**Functional Requirements:**

- Attachy can answer user queries using natural language processing.
- Attachy can assist students with application processes and company selection.
- Attachy can provide support and guidance to users.

### 4. External Interface Requirements

#### 4.1 User Interfaces

- **Web Interface:** The IMS will provide a responsive web interface accessible through modern web browsers.

#### 4.2 Hardware Interfaces

- **Server Requirements:** The IMS will be hosted on servers meeting performance and scalability requirements.

#### 4.3 Software Interfaces

- **APIs:** Integration with university systems and databases will be facilitated through APIs.

#### 4.4 Communications Interfaces

- **Internet Connectivity:** Users will access the IMS through an internet connection.

### 5. System Requirements

#### 5.1 Functional Requirements

- The system must allow users to register and manage profiles.
- The system must provide a search engine for finding internships.
- The system must enable application submission and tracking.
- The system must support progress reporting and evaluation.
- The system must offer GPS and route navigation for staff.
- The system must integrate the Attachy assistant for user support.

#### 5.2 Non-Functional Requirements

- **Performance:** The system must handle high volumes of users and transactions efficiently.
- **Scalability:** The system must be scalable to accommodate increasing numbers of users.
- **Security:** The system must ensure data protection and privacy.
- **Usability:** The system must provide an intuitive and user-friendly interface.

### 6. Other Non-Functional Requirements

#### 6.1 Security Requirements

- The system must implement robust authentication and authorization mechanisms.
- The system must encrypt sensitive data in transit and at rest.

#### 6.2 Reliability Requirements

- The system must ensure high availability and minimal downtime.
- The system must include backup and disaster recovery mechanisms.

#### 6.3 Maintainability Requirements

- The system must be designed for ease of maintenance and updates.
- The system must provide comprehensive logging and error reporting.

#### 6.4 Portability Requirements

- The system must be accessible on various devices, including desktops, laptops, tablets, and smartphones.

### Conclusion

This Software Requirements Specification (SRS) document outlines the functional and non-functional requirements of the Comprehensive Internship Management System (IMS). The detailed description of the system features and requirements will guide the development, implementation, and maintenance of the IMS to ensure it meets the needs of students, companies, and university staff.

**Technology Stack:**

- **Backend:** Python - FastAPI
- **Database:** MongoDB
- **Frontend:** React.js
