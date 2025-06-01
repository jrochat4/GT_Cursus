# University of Lausanne - Automated Course Self-Assessment System

This project aims to develop a web application for automating the self-assessment of university courses using standardized questionnaires.

## Project Overview

The system allows administrators (after logging in) to:
- Create and manage questionnaires with various question types (text, multiple choice, Likert scale).

Participants (e.g., students) can:
- Fill out assigned questionnaires.

The system also provides:
- User registration and secure login (passwords are hashed).
- Placeholder reporting features with simulated data.

Currently, the application uses an in-memory data store for users and questionnaires. Database integration is a key area for future development.

## Development Setup

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation
1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
To start the development server:
```bash
flask run
# Or, if you have run.py set up:
# python run.py
```
The application will typically be available at `http://127.0.0.1:5000/`.
Login with username `admin` and password `securepassword` to access administrative features, or register a new user.

### Running Unit Tests
To run all unit tests:
```bash
python -m unittest discover tests
```
To run a specific test file (e.g., auth tests):
```bash
python -m unittest tests.test_auth
```

## Project Structure

-   `app/`: Main Flask application package.
    -   `__init__.py`: Application factory (`create_app`) and Flask extension initialization.
    -   `main/`: Blueprint for core application routes.
        -   `routes.py`: Defines the application's web routes (questionnaires, auth, reporting placeholders).
    -   `models/`: Data models (currently Python classes).
        -   `questionnaire.py`: `Questionnaire` and `Question` classes.
        -   `user.py`: `User` class and user management functions (in-memory).
    -   `static/`: Static files (CSS, JS - currently minimal).
    -   `templates/`: HTML templates for rendering web pages.
-   `db/`: (Currently unused) Placeholder for future database-related files.
-   `tests/`: Unit tests.
    -   `test_basic_setup.py`: Tests for app initialization and public pages.
    -   `test_models.py`: Tests for data model classes (`Questionnaire`, `Question`, `User`).
    -   `test_auth.py`: Tests for authentication logic (registration, login, logout, route protection).
-   `run.py`: Script to run the Flask development server.
-   `requirements.txt`: Python package dependencies.
-   `README.md`: This file.
-   `Accreditation_Institutionnelle.md`, `Accreditation_Programmes.md`, `Canevas_Cursus.md`, `Cohortes_Et_EvaluationCursus.pdf`: Original documentation/files related to accreditation and course evaluation.

## Current Functionality
- User registration (hashed passwords) and login.
- Creation of questionnaires (title, description).
- Adding questions (Text, Multiple Choice, Likert Scale with choices) to questionnaires.
- Listing available questionnaires.
- Interface for users to fill out questionnaires (answers printed to console, not stored).
- Placeholder reporting pages with simulated data.
- Protected routes for questionnaire creation/management (login required).
- Unit tests for models, basic setup, and authentication.

## Future Development Ideas
- **Database Integration:** Replace in-memory stores with a persistent database (e.g., SQLAlchemy with SQLite or PostgreSQL).
- **Answer Storage & Real Reports:** Save questionnaire responses to the database and build actual reporting features.
- **User Roles & Permissions:** Differentiate between administrators, instructors, and students with specific permissions.
- **Questionnaire Management Enhancements:** Editing/deleting questionnaires and questions.
- **Advanced Question Types:** More complex question formats (e.g., matrix, ranking).
- **Course/Cohort Association:** Link questionnaires to specific courses or student cohorts.
- **UI/UX Improvements:** Enhance the user interface and experience.
