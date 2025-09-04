# AetherNotes Backend

This directory contains the source code for the AetherNotes backend service. It is a modern, containerized API built with FastAPI and Python 3.11, designed to handle user authentication, document management, and AI-powered interactions.

## ⚙️ Tech Stack

  * **Framework:** [FastAPI](https://fastapi.tiangolo.com/) for building high-performance, asynchronous APIs.
  * **Database:** [PostgreSQL](https://www.postgresql.org/) for robust, relational data storage.
  * **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) for safe and Pythonic database interactions.
  * **Data Validation:** [Pydantic](https://www.google.com/search?q=https://docs.pydantic.dev/) for data validation and API schema definition.
  * **Authentication:** JWT-based sessions with two passwordless flows (Email OTP and Google OAuth 2.0).
  * **Containerization:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) for a consistent development and production environment.

-----

## 🚀 Local Development Setup

While the recommended way to run the entire project is with Docker Compose from the root directory, you can run the backend service standalone for development and testing.

1.  **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

      * Create a `.env` file in the project's **root directory** (one level above this one).
      * Copy the contents of `.env.example` into it and fill in your local secrets. The backend requires these to connect to the database and other services.

5.  **Run the development server:**

      * This command starts the FastAPI server with live reloading on code changes.

    <!-- end list -->

    ```bash
    uvicorn app.main:app --reload
    ```

    The API will be available at `http://localhost:8000`.

-----

## API Structure

The API is versioned to ensure future compatibility. All endpoints are prefixed with `/api/v1`.

The code is organized into a scalable structure:

  * `app/api/v1/endpoints/`: Contains the API routers for different features (e.g., `auth.py`, `google.py`).
  * `app/api/v1/deps.py`: Contains reusable FastAPI dependencies like `get_db` and `get_current_user`.
  * `app/core/`: Holds core application logic like security and configuration.
  * `app/crud/`: Handles all database (Create, Read, Update, Delete) operations.
  * `app/db/`: Contains the database models (`base.py`) and session management (`session.py`).
  * `app/schemas/`: Contains the Pydantic models for API data validation.

-----

## 🔑 Environment Variables

The application is configured using environment variables. These must be present in a `.env` file in the project's root directory.

| Variable | Description |
| :--- | :--- |
| `MAILGUN_API_KEY` | Your private API key for the Mailgun email service. |
| `MAILGUN_DOMAIN` | Your sandbox or custom domain from Mailgun. |
| `MAIL_FROM_EMAIL` | The "From" address to use when sending OTP emails. |
| `GOOGLE_CLIENT_ID`| Your OAuth 2.0 Client ID from the Google Cloud Console. |
| `GOOGLE_CLIENT_SECRET`| Your OAuth 2.0 Client Secret from the Google Cloud Console. |