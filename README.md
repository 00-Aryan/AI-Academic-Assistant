# AURA - Academic Assistant

![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

**AURA** is an intelligent platform designed to streamline academic support. It provides students with an AI-powered chat interface to get instant help on their coursework, while offering powerful summarization and analytics tools for Teaching Assistants (TAs) and instructors.

##  Features

- **AI-Powered Student Chat**: Students can ask questions and receive instant, context-aware answers from an AI assistant powered by Google Gemini.
- **Doubt Summarization**: TAs can generate insightful summaries of student doubts over various periods (daily, weekly, monthly).
- **Email & PDF Export**: Summaries can be exported as a formatted PDF and sent directly to an email address.
- **Role-Based Access**: Separate interfaces and functionalities for students and TAs.
- **Theming**: A modern UI with both light and dark modes.
- **High-Performance Backend**: Built with FastAPI, ensuring a fast and scalable API.

##  Tech Stack

| Area         | Technology                                                                                             |
|--------------|--------------------------------------------------------------------------------------------------------|
| **Frontend** | Vue.js, Pinia, Vue Router, Tailwind CSS |
| **Backend**  | Python, FastAPI, SQLAlchemy, Alembic |
| **Database** | SQLite (default), easily configurable for PostgreSQL, etc.          |
| **AI/LLM**   | Google Gemini                                                                |
| **Emailing** | fastapi-mail                                                 |

##  Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9+
- Node.js v18+ (which includes npm) or Yarn
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
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file. You can copy the example:
# cp .env.example .env
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
