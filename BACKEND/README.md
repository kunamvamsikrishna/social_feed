# Mini Community Social Feed - Backend API

A RESTful API for a community-based social platform built with Django REST Framework.

## 🚀 Features

- **JWT Authentication** - Secure token-based authentication with refresh tokens
- **Community Management** - Create, join, and manage communities
- **Social Feed** - Post content within communities
- **Like System** - Like/unlike posts with toggle functionality
- **Permission Control** - Role-based access (creators, members, authenticated users)
- **Optimized Queries** - Database indexes and query optimization
- **CORS Enabled** - Ready for React frontend integration

## 📋 Requirements

- Python 3.8+
- Django 5.2.3
- Django REST Framework 3.16.0

## 🔧 Installation

1. **Clone the repository**
```bash
cd BACKEND
```

2. **Create virtual environment**
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.minimal.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

Server will be running at: http://127.0.0.1:8000/

## 📚 API Documentation

See [API_ENDPOINTS.py](API_ENDPOINTS.py) for complete API documentation.

### Quick Overview

**Authentication**
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout (blacklist token)
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/token/refresh/` - Refresh access token

**Communities**
- `GET /api/communities/` - List all communities
- `POST /api/communities/` - Create community
- `GET /api/communities/{id}/` - Get community details
- `POST /api/communities/{id}/join/` - Join community
- `POST /api/communities/{id}/leave/` - Leave community
- `GET /api/communities/{id}/members/` - Get members

**Posts**
- `GET /api/posts/` - List all posts
- `GET /api/posts/community/{id}/` - Get community feed
- `POST /api/posts/` - Create post (requires membership)
- `GET /api/posts/{id}/` - Get post details
- `POST /api/posts/{id}/like/` - Like/unlike post
- `GET /api/posts/{id}/likes/` - Get post likes

## 🧪 Testing

Run the test script:
```bash
# Install requests library
pip install requests

# Run tests (see test_api.py for details)
python test_api.py
```

Or use tools like:
- Postman
- Thunder Client (VS Code)
- curl
- httpie

## 🏗️ Project Structure

```
BACKEND/
├── social_feed_prj/        # Project settings
│   ├── settings.py         # Django + DRF configuration
│   └── urls.py             # Main URL routing
├── users/                  # Authentication app
│   ├── serializers.py      # User serializers
│   ├── views.py            # Auth views
│   └── urls.py             # Auth endpoints
├── communities/            # Community management
│   ├── models.py           # Community, CommunityMember
│   ├── serializers.py      # Community serializers
│   ├── views.py            # Community viewsets
│   └── urls.py             # Community endpoints
├── posts/                  # Posts and likes
│   ├── models.py           # Post, Like models
│   ├── serializers.py      # Post serializers
│   ├── views.py            # Post viewsets
│   └── urls.py             # Post endpoints
├── manage.py
├── requirements.txt
└── requirements.minimal.txt
```

## 📊 Database Schema

### Models

1. **User** (Django built-in)
   - Authentication and user management

2. **Community**
   - name (unique)
   - description
   - created_by (FK to User)
   - created_at

3. **CommunityMember**
   - user (FK to User)
   - community (FK to Community)
   - joined_at
   - Unique constraint: (user, community)

4. **Post**
   - content
   - author (FK to User)
   - community (FK to Community)
   - created_at
   - Validation: Author must be community member

5. **Like**
   - user (FK to User)
   - post (FK to Post)
   - created_at
   - Unique constraint: (user, post)

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### How to use:

1. **Register or Login**
```bash
POST /api/auth/login/
{
    "username": "testuser",
    "password": "password123"
}
```

2. **Get tokens in response**
```json
{
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

3. **Use access token in requests**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

4. **Refresh when expired**
```bash
POST /api/auth/token/refresh/
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 🌐 CORS Configuration

CORS is configured for frontend development:
- Allowed origins: `http://localhost:3000`, `http://127.0.0.1:3000`
- Credentials allowed

Update `settings.py` `CORS_ALLOWED_ORIGINS` for production.

## 🔍 Admin Interface

Access Django admin at: http://127.0.0.1:8000/admin/

All models are registered with custom admin classes for easy data management.

## 📝 Key Features Details

### Community Creation
- Any authenticated user can create a community
- Creator is automatically added as first member
- Creator cannot leave their own community

### Posting
- Only community members can create posts
- Validation happens at serializer level
- Posts are ordered by creation date (newest first)

### Like System
- Toggle-based: Like if not liked, unlike if already liked
- Duplicate likes prevented by unique constraint
- Real-time like count updates

### Permissions
- Public: List communities, view feeds
- Authenticated: Create communities, join, post, like
- Creator: Update/delete community
- Author: Update/delete own posts

## 🚀 Frontend Integration

Ready for React integration:

1. Store JWT tokens (localStorage/context)
2. Add Authorization header to requests
3. Handle 401 errors (redirect to login)
4. Implement token refresh logic

Example fetch:
```javascript
fetch('http://localhost:8000/api/communities/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
    }
})
```

## 📦 Production Deployment

For production:

1. Set `DEBUG = False` in settings.py
2. Configure proper `SECRET_KEY`
3. Update `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Configure static files
6. Use gunicorn/uwsgi
7. Setup HTTPS
8. Configure proper CORS origins

## 🤝 Contributing

This is a project for evaluation purposes.

## 📄 License

This project is for educational/evaluation purposes.

## 👥 Authors

Built as part of the Mini Community Social Feed assignment.

---

**Server Status**: ✅ Running at http://127.0.0.1:8000/

**API Version**: 1.0

**Django Version**: 5.2.3

**Last Updated**: December 17, 2025
