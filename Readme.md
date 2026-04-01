TalentRank AI

TalentRank AI is a backend-only AI-powered resume screening system that automates resume parsing, skill extraction, candidate ranking, and job application workflows for recruiters.

🚀 Features
Resume Upload: Supports PDF and DOCX formats.

Resume Parsing: Automated text and skill extraction from resumes.

Candidate Ranking: Smart ranking based on specific job requirements.

Job Management: Full job posting and management system for recruiters.

Authentication (RBAC): Role-based access control for Recruiters and Candidates.

Google OAuth: Secure login integration using Google accounts.

Resume Search: Fast and efficient searching powered by Elasticsearch.

Email Notifications: * Welcome email on signup/Google login.

Confirmation email upon resume upload.

Selection emails triggered by recruiters.

🛠️ Tech Stack
Framework: FastAPI

Database: PostgreSQL

Search Engine: Elasticsearch

Containerization: Docker

Auth: OAuth 2.0 (Google Login)

Deployment: Vercel

🔐 Authentication & Authorization
RBAC: Distinct permissions for Recruiters and Candidates.

Supported Methods: Standard Email/Password and Google OAuth 2.0.

📧 Email Features
Registration: Welcome emails for new users.

Recruitment: Automated and recruiter-triggered candidate selection notifications.

📌 API Overview
Authentication
POST /register - Register new user

POST /login - User login

GET /login-with-google - Initiate Google Auth

GET /callback - OAuth callback handler

Candidate APIs
POST /upload-resumes - Upload a new resume

GET /my-resumes - View uploaded resumes

DELETE /del-resume/{file_id} - Delete a specific resume

POST /apply-job/{job_id} - Apply for a job opening

Recruiter APIs
POST /job-post - Create a job posting

DELETE /del-job/{job_id} - Remove a job posting

GET /job-posts - List all job posts

POST /parse-resumes/{file_id}/{job_id} - Parse resume against job specs

GET /resume-searching/{job_id} - Search resumes via Elasticsearch

GET /send-selection-email/{user_email} - Trigger selection email

⚙️ System Workflow
Identity: User registers or logs in (Email or Google).

Upload: Candidate uploads their resume (PDF/DOCX).

Extraction: System extracts text and skills, then stores them.

Job Posting: Recruiter creates a job description.

Matching: Recruiter parses resumes against jobs; system ranks candidates based on skill match.

Selection: Recruiter selects top candidates and the system sends automated selection emails.
🚀 Deployment

The project is deployed on Vercel.


📈 Future Improvements

Advanced AI-based ranking
Candidate recommendation system


🤝 Contributing

Contributions, issues, and feature requests are welcome.

📄 License

This project is for educational and portfolio purposes.