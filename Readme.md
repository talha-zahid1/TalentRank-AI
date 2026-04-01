TalentRank AI

TalentRank AI is a backend-only AI-powered resume screening system that automates resume parsing, skill extraction, candidate ranking, and job application workflows for recruiters.

🚀 Features
Resume upload (PDF/DOCX)
Resume parsing and text extraction
Skill extraction from resumes
Candidate ranking based on job requirements
Job posting management
Recruiter and candidate role-based authentication (RBAC)
Google OAuth login integration
Resume search using Elasticsearch
Email notification system:
Welcome email on signup & Google login
Confirmation email on resume upload
Candidate selection email sent by recruiter
🛠️ Tech Stack
FastAPI
PostgreSQL
Elasticsearch
Docker
OAuth 2.0 (Google Login)
🔐 Authentication & Authorization
Role-based access control:
Recruiter
Candidate/User
Supports:
Email/password authentication
Google OAuth login
📧 Email Features
Welcome email on:
User registration
Google login
Candidate selection email triggered by recruiter
📌 API Overview
Authentication
POST /register
POST /login
GET /login-with-google
GET /callback
Candidate APIs
POST /upload-resumes
GET /my-resumes
DELETE /del-resume/{file_id}
POST /apply-job/{job_id}
Recruiter APIs
POST /job-post
DELETE /del-job/{job_id}
GET /job-posts
POST /parse-resumes/{file_id}/{job_id}
GET /resume-searching/{job_id}
GET /send-selection-email/{user_email}
⚙️ System Workflow
User registers or logs in (including Google OAuth)
Candidate uploads resume
System extracts and stores resume data
Recruiter posts jobs
Recruiter parses resumes against jobs
Skills are matched and candidates are ranked
Recruiter selects candidates
Selection email is sent automatically
🚀 Deployment

The project is deployed on Vercel.


📈 Future Improvements

Advanced AI-based ranking
Candidate recommendation system


🤝 Contributing

Contributions, issues, and feature requests are welcome.

📄 License

This project is for educational and portfolio purposes.