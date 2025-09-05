# 🎟️ Events Management API Documentation

A RESTful API for managing **events, attendees, and organizers** with **role-based authentication**.

Built with **Django REST Framework (DRF)** and **JWT authentication**.

**Base URL:** `http://localhost:8000/api/auth/`

---

## 🔐 Authentication

All endpoints require **JWT authentication** except **user registration**.

### Get Access Token

`POST /token/`

**Request:**

```json
{
  "username": "your_username",
  "password": "your_password"
}

```

**Response:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "access": "eyJhbGciOiJIUzI1NiIs..."
}

```

### Refresh Access Token

`POST /token/refresh/`

**Request:**

```json
{
  "refresh": "your_refresh_token_here"
}

```

---

## 👥 User Management

### Register New User

`POST /users/`

**Request:**

```json
{
  "username": "newuser",
  "password": "securepassword123",
  "email": "user@example.com"
}

```

**Response:**

```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com"
}

```

### Create Organizer Profile

**Requires authentication**

`POST /organizers/`

**Request:**

```json
{
  "organization_name": "Tech Events Inc"
}

```

**Response:**

```json
{
  "id": 1,
  "user": "newuser",
  "organization_name": "Tech Events Inc"
}

```

### Create Attendee Profile

**Requires authentication**

`POST /attendees/`

**Response:**

```json
{
  "id": 1,
  "user": "newuser"
}

```

---

## 📅 Events Management

### List All Events

`GET /events/`

**Response (paginated):**

```json
{
  "count": 15,
  "next": "http://localhost:8000/api/auth/events/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Tech Conference 2024",
      "description": "Annual technology conference",
      "location": "Convention Center",
      "organizer": "Tech Events Inc",
      "categories": [1, 2],
      "start_date": "2024-12-15T09:00:00Z",
      "end_date": "2024-12-17T17:00:00Z",
      "created_at": "2024-08-29T10:30:00Z",
      "updated_at": "2024-08-29T10:30:00Z"
    }
  ]
}

```

### Create Event (Organizers Only)

`POST /events/`

**Request:**

```json
{
  "title": "New Developer Workshop",
  "description": "Hands-on coding workshop",
  "location": "Tech Hub Building",
  "categories": [1, 3],
  "start_date": "2024-12-20T10:00:00Z",
  "end_date": "2024-12-20T16:00:00Z"
}

```

### Event Details

- **Get event** → `GET /events/{id}/`
- **Update event (organizer only)** → `PATCH /events/{id}/`
- **Delete event (organizer only)** → `DELETE /events/{id}/`

---

## 🏷️ Categories

### List Categories with Events

`GET /categories/`

**Response:**

```json
[
  {
    "id": 1,
    "name": "Conference",
    "events": [
      {
        "id": 1,
        "title": "Tech Conference 2024",
        "start_date": "2024-12-15T09:00:00Z",
        "end_date": "2024-12-17T17:00:00Z",
        "location": "Convention Center",
        "organizer": "Tech Events Inc"
      }
    ]
  },
  {
    "id": 2,
    "name": "Workshop",
    "events": []
  }
]

```

---

## ✅ RSVP Management

### Create RSVP (Attendees Only)

`POST /rsvps/`

**Request:**

```json
{
  "event": 1,
  "status": "going"
}

```

**Status Options:** `"going"`, `"maybe"`, `"declined"`

**Response:**

```json
{
  "id": 1,
  "event": 1,
  "event_title": "Tech Conference 2024",
  "attendee": 1,
  "attendee_name": "attendee_user",
  "organizer_name": "Tech Events Inc",
  "status": "going",
  "created_at": "2024-08-29T11:45:00Z"
}

```

### Manage RSVPs

- **List RSVPs** → `GET /rsvps/`
    - Attendees: see their own RSVPs
    - Organizers: see RSVPs for their events
- **Update RSVP (attendee only)** → `PATCH /rsvps/{id}/`
- **Delete RSVP (attendee only)** → `DELETE /rsvps/{id}/`

---

## 🚨 Error Responses

- **400 Bad Request**

```json
{
  "error": "Validation error message",
  "code": "validation_error",
  "details": {"field_name": ["Error description"]}
}

```

- **401 Unauthorized**

```json
{"error": "Authentication credentials were not provided","code": "not_authenticated"}

```

- **403 Forbidden**

```json
{"error": "You do not have permission to perform this action","code": "permission_denied"}

```

- **404 Not Found**

```json
{"error": "Resource not found","code": "not_found"}

```

- **405 Method Not Allowed**

```json
{"error": "Method GET not allowed","code": "method_not_allowed"}

```

---

## 🧪 Example Workflow

1. **Register and Authenticate**

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"event_organizer","password":"securepass123","email":"organizer@example.com"}'

```

1. **Get Tokens**

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"event_organizer","password":"securepass123"}'

```

1. **Create Organizer Profile**

```bash
curl -X POST http://localhost:8000/api/auth/organizers/ \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"organization_name":"Tech Events Inc"}'

```

1. **Create an Event**

```bash
curl -X POST http://localhost:8000/api/auth/events/ \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Developer Workshop",
    "description": "Learn Python basics",
    "location": "Tech Innovation Center",
    "categories": [1, 2],
    "start_date": "2024-09-15T10:00:00Z",
    "end_date": "2024-09-15T16:00:00Z"
  }'

```

---

## 📋 Rate Limits

- **Unauthenticated requests:** 100/hour
- **Authenticated requests:** 1000/hour
- **Organizer endpoints:** 500/hour

---

## 🔧 Setup Instructions

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver

```

---

## 📝 Notes

- **JWT Tokens:** Access tokens expire after 5 minutes. Use refresh tokens to get new access tokens.
- **Permissions:**
    - Organizers → manage their own events
    - Attendees → manage their own RSVPs
    - All authenticated users → browse events and categories
- **RSVP Limits:** One RSVP per attendee per event
