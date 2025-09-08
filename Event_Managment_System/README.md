# Event Management System

A Django REST API for managing events, attendees, and organizers with JWT authentication.

## Features

- User authentication with JWT
- Event management (CRUD operations)
- Attendee registration
- Category-based event organization
- RESTful API endpoints
- API documentation with Swagger/OpenAPI

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Event_Managment_System
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

After starting the development server, access the API documentation at:
- Swagger UI: http://localhost:8000/api/schema/swagger/
- ReDoc: http://localhost:8000/api/schema/redoc/

## Deployment to PythonAnywhere

1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Sign up for a PythonAnywhere account (free tier available)
3. In the PythonAnywhere dashboard:
   - Go to "Web" tab and click "Add a new web app"
   - Select "Manual Configuration (including virtualenvs)"
   - Choose Python 3.10 (or your preferred version)
   - Set up your virtualenv and install requirements
   - Configure your WSGI file (use the provided wsgi.py)
   - Set up static files mapping:
     - URL: /static/
     - Directory: /home/yourusername/Event_Managment_System/staticfiles
   - Set up media files mapping:
     - URL: /media/
     - Directory: /home/yourusername/Event_Managment_System/media

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEBUG=False
SECRET_KEY=your-secret-key-here
```

## License

This project is licensed under the MIT License.
