# 🚀 AURA – AI-Powered Student Doubt Analysis & Academic Insight Platform

AURA is a full-stack platform that uses AI to answer student queries in real time and analyzes aggregated doubts to help instructors identify learning gaps at scale.

## Problem Statement

Teaching Assistants (TAs) and instructors often struggle to manually track and identify recurring questions and points of confusion across hundreds of student interactions. This makes it difficult to proactively address widespread learning gaps. At the same time, students need immediate, 24/7 support for common questions.

## Solution Overview

AURA provides a dual-interface system to address this. For students, it offers an AI chatbot powered by Google Gemini for instant answers. For TAs, it features a dashboard that aggregates student doubts, generates analytical summaries, and exports them as PDF reports via email. This allows educators to quickly pinpoint topics that need further clarification.

## ⚡ Quick Overview

- 🤖 AI-powered chatbot using Google Gemini for real-time student support  
- 📊 Aggregates and analyzes student doubts for instructors  
- 📄 Generates automated PDF reports with key learning insights  
- ⚡ Asynchronous email delivery using FastAPI background tasks  
- 🧱 Decoupled architecture (Vue.js + FastAPI + ORM)  

## System Architecture

The system uses a decoupled architecture with a frontend single-page application (SPA) and a backend REST API.

1.  **Frontend**: A **Vue.js SPA** provides the user interface for both students and TAs. It uses **Pinia** for state management and communicates with the backend via RESTful API calls.
2.  **Backend**: A **FastAPI (Python)** server acts as the core of the system.
    *   **API Layer**: Exposes REST endpoints for student chats and TA analytics. Data validation is handled by **Pydantic**.
    *   **Business Logic**:
        *   For student queries, it calls the **Google Gemini API**.
        *   For TA reports, it queries the database, aggregates doubt data, and generates summary statistics.
    *   **Asynchronous Task**: Email delivery for PDF reports is handled as a background task using `fastapi-mail` to avoid blocking API responses.
    *   **Data Access Layer**: **SQLAlchemy ORM** manages all communication with the database.
3.  **Database**: A **SQLite** database stores application data like student questions and user information. **Alembic** is used for managing database schema migrations.
  

## 🔄 System Flow

1. Student submits question → frontend sends request to backend  
2. Backend calls Gemini API → generates response  
3. Question is stored in database  
4. TA dashboard aggregates questions  
5. Reports generated → emailed asynchronously  

### Data Flow: Report Generation

1.  **Request**: A TA requests a report from the Vue.js frontend, triggering a `POST` request to the `/api/ta/doubts/export/email` endpoint.
2.  **Validation**: The FastAPI backend validates the incoming request payload (e.g., `course_code`, `recipient_email`) using Pydantic models.
3.  **Data Aggregation**: The application queries the SQLite database via SQLAlchemy to fetch and process student doubts for the specified period.
4.  **Report Generation**: A PDF report and a styled HTML email are generated based on the aggregated data.
5.  **Asynchronous Dispatch**: The email and PDF attachment are handed off to `fastapi-mail`, which sends the email via a configured SMTP server. The API returns an immediate success response to the frontend.

## 🔧 Key Engineering Highlights

- **AI Integration**: Integrated Google Gemini API for real-time question answering  
- **Asynchronous Processing**: Implemented non-blocking email delivery using FastAPI background tasks  
- **Data Aggregation Pipeline**: Designed backend logic to process and summarize large volumes of student queries  
- **Type-Safe APIs**: Used Pydantic for strict request/response validation  
- **ORM + Migrations**: Managed database schema using SQLAlchemy and Alembic  
- **Scalable Architecture**: Decoupled frontend and backend for modular development  

## Tech Stack

| Area         | Technology                                                                                             |
|--------------|--------------------------------------------------------------------------------------------------------|
| **Frontend** | Vue.js, Pinia (State Management), Vue Router, Tailwind CSS                                             |
| **Backend**  | Python, FastAPI, Pydantic (Data Validation)                                                            |
| **Database** | SQLite, SQLAlchemy (ORM), Alembic (Migrations)                                                         |
| **AI/LLM**   | Google Gemini                                                                                          |
| **Tooling**  | Uvicorn (ASGI Server), `fastapi-mail` (Emailing)                                                       |

## Key Engineering Decisions

*   **Why FastAPI?** Chosen for its high performance, native async support, and automatic data validation with Pydantic. This is ideal for I/O-bound tasks like making calls to the Gemini API and sending emails.
*   **Why SQLAlchemy and Alembic?** This combination provides a powerful, production-ready ORM and ensures that database schema changes are systematic, version-controlled, and reproducible.
*   **Why a Decoupled Frontend?** A separate Vue.js SPA creates a clean API-driven contract between the client and server, allowing for independent development cycles and technology choices.

## Limitations & Future Improvements

*   **Limitation**: The current system uses SQLite, which is not suitable for production environments with concurrent writes.
    *   **Improvement**: Migrate to a production-grade database like **PostgreSQL**.
*   **Limitation**: Email sending relies on FastAPI's simple background tasks, which do not guarantee execution if the server restarts.
    *   **Improvement**: Integrate a dedicated task queue like **Celery** with **Redis** for durable, persistent background job processing.
*   **Limitation**: The project setup is manual and not containerized.
    *   **Improvement**: Add a `Dockerfile` and `docker-compose.yml` to standardize the development and deployment environment.

##  Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9+
- Node.js v18+ and npm (or Yarn)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/soft-engg-project-sep-2025-se-SEP-12.git
cd soft-engg-project-sep-2025-se-SEP-12
```

### 2. Backend Setup

The backend is a Python application powered by FastAPI.

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv # On macOS/Linux: source venv/bin/activate | On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

Now, create and open a `.env` file in the `backend/` directory and fill in the required environment variables. See the **Configuration** section below for details.

#### Database Migration

The project uses Alembic to manage database schemas. Apply the migrations to create your database tables:

```bash
alembic upgrade head
```

#### Running the Backend

```bash
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`. You can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

### 3. Frontend Setup

The frontend is a Vue.js single-page application.

```bash
# Navigate to the frontend directory from the root
cd ../frontend

# Install dependencies
npm install
# or
yarn install

# Run the development server
npm run dev
# or
yarn dev
```

The frontend application will be available at `http://localhost:5173` (or another port if 5173 is in use).

##  Configuration

Create a `.env` file in the `backend/` directory. This file stores sensitive credentials and environment-specific settings.

```ini
# backend/.env

# Application
APP_NAME=AURA
DEBUG=True
API_PREFIX=/api

# Database (SQLite by default)
# The path is relative to the `backend` directory.
DATABASE_URL=sqlite:///./app.db

# AI/LLM - Get your key from Google AI Studio
GOOGLE_API_KEY="your-gemini-api-key"

# Email Configuration (for report exporting)
# See EMAIL_CONFIGURATION.md for detailed setup guides for Gmail, etc.
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-16-digit-app-password"
EMAILS_FROM_EMAIL="your-email@gmail.com"
EMAILS_FROM_NAME="AURA - Academic Assistant"
SMTP_TLS=True
SMTP_SSL=False
```

> ** Important:** Never commit your `.env` file to version control. The `.gitignore` file is already configured to ignore it. For more details on setting up email, refer to `EMAIL_CONFIGURATION.md`.

##  Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request


