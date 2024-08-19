# Software Requirements Specification (SRS)
---
## Comprehensive Internship Management System (IMS)

### 1. Introduction

#### 1.1 Purpose

The purpose of this Software Requirements Specification (SRS) document is to provide a detailed description of the Comprehensive Internship Management System (IMS). This document outlines the system's functionalities, features, and constraints to ensure a clear understanding of the system's requirements and expected performance.

#### 1.2 Scope

The IMS is designed to streamline the internship management process for students, companies, university staff, and the Industrial Liaison Office. The system provides a centralized platform for managing internship applications, monitoring progress, and facilitating support through advanced technologies. The key features of the IMS include:

- Student registration and profile management
- Internship search, application, and placement
- Company registration and internship posting
- Application tracking and management
- Progress reporting and evaluation
- Supervision management (school-based and company-based)
- Department evaluation
- Industrial Liaison Office oversight
- Staff support and system administration
- GPS and route navigation for staff

#### 1.3 Definitions, Acronyms, and Abbreviations

- **IMS:** Internship Management System
- **NLP:** Natural Language Processing
- **Attachy:** NLP-powered assistant integrated into the IMS
- **GPS:** Global Positioning System
- **ILO:** Industrial Liaison Office

#### 1.4 References

- Project Proposal Overview Document
- Final Year Project - Chapter One Document
- Industrial Attachment Forms and Guidelines

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

- Student management and internship application
- Company management and internship posting
- Application tracking and monitoring
- Progress reporting and evaluation
- Supervision management (school-based and company-based)
- Department evaluation
- Industrial Liaison Office oversight
- Staff support and system administration
- GPS and route navigation for staff

#### 2.3 User Classes and Characteristics

- **Students:** Undergraduate and postgraduate students seeking internships.
- **Companies:** Organizations offering internship opportunities.
- **Company-based Supervisors:** Employees of the company overseeing student internships.
- **School-based Supervisors:** University staff assigned to supervise students during internships.
- **Departments:** Academic departments responsible for evaluating student reports.
- **Industrial Liaison Office:** University department overseeing all internship activities.

#### 2.4 Operating Environment

The IMS will operate in a web-based environment, accessible through modern web browsers on various devices, including desktops, laptops, tablets, and smartphones.

#### 2.5 Design and Implementation Constraints

- Integration with existing university systems and databases
- Compliance with data protection and privacy regulations
- High availability and performance requirements
- Mobile-friendly interface for supervisors using GPS navigation

#### 2.6 User Documentation

User manuals, online help, and video tutorials will be provided to guide users in using the system. Specific documentation will be created for each user class.

#### 2.7 Assumptions and Dependencies

- Users will have access to the internet and modern web browsers.
- The university will provide necessary APIs for system integration.
- Companies will cooperate in providing accurate information and timely evaluations.

### 3. System Features

#### 3.1 Student Management

**Description:** Allows students to register, create, and manage their profiles, apply for internships, and manage their internship activities.

**Functional Requirements:**

- Students can log in to the system using credentials provided by the school.
- Students can update personal and academic information.
- Students can upload and manage resumes and other documents.
- Students can view a list of available companies seeking interns.
- Students can search for internships using various filters (e.g., location, industry, duration).
- Students can apply for internships directly through the platform.
- Students can track the status of their applications.
- Students can fill out an "Assumption of Duty" form on the first day of internship.
- Students can fill in daily activity logs.
- Students can edit their daily logs until supervised by their assigned supervisor.
- Students can submit monthly work experience summaries.
- Students can view their logbook results after supervision.
- Students can submit final attachment reports through the platform.

#### 3.2 Company Management

**Description:** Allows companies to register, create profiles, post internship opportunities, and manage interns.

**Functional Requirements:**

- Companies can register and create profiles.
- Companies can post and manage internship opportunities.
- Companies can view and manage student applications.
- Companies can schedule and manage interviews with applicants.
- Companies can designate a company-based supervisor for each intern.
- Company-based supervisors can view and comment on students' weekly activities.
- Company-based supervisors can endorse students' login books weekly.
- Company-based supervisors can write final comments and grade students at the end of the internship.

#### 3.3 Supervision Management

**Description:** Manages the assignment and activities of school-based and company-based supervisors.

**Functional Requirements:**

- The system assigns school-based supervisors to students based on department and geographic location.
- School-based supervisors can view assigned students' locations and use GPS for navigation.
- School-based supervisors can view students' daily logs and activities.
- School-based supervisors can mark logbooks, endorse them, and provide comments.
- School-based supervisors can grade students' performance using a standardized form.
- The system balances supervisor workload based on student distribution and location.
- Supervisors can generate and submit evaluation reports.

#### 3.4 Department Management

**Description:** Allows academic departments to evaluate student reports and provide final grades.

**Functional Requirements:**

- Departments can access and grade students' final attachment reports.
- Departments can view supervisor evaluations and logbook grades.
- The system calculates final grades based on logbook marks and report grades according to scales set by the Industrial Liaison Office.
- Departments can generate performance reports for their students.

#### 3.5 Industrial Liaison Office Management

**Description:** Provides overall system management and oversight capabilities for the Industrial Liaison Office.

**Functional Requirements:**

- The ILO can manage and oversee all system operations.
- Administrators can alter any data in the system.
- The office can finalize all operations and halt processes when necessary.
- The system supports different roles within the office (directors, admins, officers, etc.).
- The ILO can set and adjust grading scales and evaluation criteria.
- The ILO can generate comprehensive reports on internship programs.

#### 3.6 Application Tracking and Monitoring

**Description:** Enables all stakeholders to track and monitor the status of internship applications and placements.

**Functional Requirements:**

- Students can view the status of their applications.
- Companies can update the status of student applications.
- The ILO can monitor the application process and provide support as needed.
- The system generates notifications for status changes and upcoming deadlines.

#### 3.7 Progress Reporting and Evaluation

**Description:** Facilitates the reporting and evaluation of student progress throughout the internship.

**Functional Requirements:**

- Students can submit daily logs and monthly summaries.
- Company-based supervisors can provide weekly endorsements and feedback.
- School-based supervisors can evaluate student performance during site visits.
- The system calculates and combines scores from various evaluation components.
- Stakeholders can view progress reports and evaluations according to their roles.

#### 3.8 Staff Support and System Administration

**Description:** Provides tools for university staff to manage the system, support users, and oversee the internship process.

**Functional Requirements:**

- Staff can manage student, company, and supervisor profiles.
- Staff can oversee internship postings and applications.
- Staff can generate reports and analytics.
- Staff can configure system settings and user access.
- The system provides a help desk function for user support.

#### 3.9 GPS and Route Navigation

**Description:** Provides navigation tools for school-based supervisors to locate and travel to internship sites.

**Functional Requirements:**

- School-based supervisors can view the location of internship sites on a map.
- The system provides optimal routes for supervisors to visit multiple sites.
- Supervisors can use GPS navigation to travel to sites.
- The system tracks and logs supervisor visits for reporting purposes.

### 4. External Interface Requirements

#### 4.1 User Interfaces

- **Web Interface:** The IMS will provide a responsive web interface accessible through modern web browsers.
- **Mobile Interface:** A mobile-friendly interface will be provided for supervisors using GPS navigation.

#### 4.2 Hardware Interfaces

- **Server Requirements:** The IMS will be hosted on servers meeting performance and scalability requirements.
- **GPS Integration:** The system will interface with mobile device GPS for navigation features.

#### 4.3 Software Interfaces

- **University Systems:** Integration with existing university systems and databases will be facilitated through APIs.
- **Mapping Services:** Integration with mapping services for GPS and route navigation features.

#### 4.4 Communications Interfaces

- **Internet Connectivity:** Users will access the IMS through an internet connection.
- **Email Integration:** The system will send notifications and alerts via email.

### 5. System Requirements

#### 5.1 Functional Requirements

- The system must implement all features described in Section 3: System Features.
- The system must support the complete workflow for student application, placement, supervision, and evaluation.
- The system must implement all forms as described, including the Organization Profile, Industrial Attachment Orientation Form, and Supervisor Assessment Form.
- The system must calculate and combine scores from logbooks, supervisor assessments, and final reports according to the Industrial Liaison Office's scaling system.
- The system must provide role-based access control for all user types.
- The system must generate appropriate notifications and alerts for all stakeholders.

#### 5.2 Non-Functional Requirements

- **Performance:** The system must handle high volumes of users and transactions efficiently.
- **Scalability:** The system must be scalable to accommodate increasing numbers of users and data.
- **Security:** The system must ensure data protection and privacy, implementing robust authentication and authorization mechanisms.
- **Usability:** The system must provide an intuitive and user-friendly interface for all user types.
- **Reliability:** The system must ensure high availability and minimal downtime.
- **Maintainability:** The system must be designed for ease of maintenance and updates.

### 6. Other Non-Functional Requirements

#### 6.1 Security Requirements

- The system must implement robust authentication and authorization mechanisms.
- The system must encrypt sensitive data in transit and at rest.
- The system must maintain an audit trail of all significant actions.

#### 6.2 Reliability Requirements

- The system must ensure high availability with an uptime of at least 99.9%.
- The system must include backup and disaster recovery mechanisms.

#### 6.3 Maintainability Requirements

- The system must be designed with a modular architecture to facilitate updates and expansions.
- The system must provide comprehensive logging and error reporting.

#### 6.4 Portability Requirements

- The system must be accessible on various devices, including desktops, laptops, tablets, and smartphones.
- The system must support major web browsers (Chrome, Firefox, Safari, Edge).

### Conclusion

This comprehensive Software Requirements Specification (SRS) document outlines the detailed functional and non-functional requirements of the Internship Management System (IMS). The system is designed to meet the needs of all stakeholders involved in the internship process, including students, companies, supervisors, departments, and the Industrial Liaison Office. By implementing these requirements, the IMS will streamline the internship management process, enhance communication between stakeholders, and provide valuable insights through reporting and analytics.