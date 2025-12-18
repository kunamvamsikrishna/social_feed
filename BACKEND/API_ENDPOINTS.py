"""
API Endpoints Documentation
===========================

This file documents all available API endpoints for the Social Feed Platform.

BASE URL: http://localhost:8000/api

AUTHENTICATION
==============
All endpoints except login, register, and list communities require JWT authentication.
Include the token in the Authorization header: "Bearer <access_token>"

---

1. AUTHENTICATION ENDPOINTS
============================

1.1 Register User
-----------------
POST /api/auth/register/
Body: {
    "username": "string",
    "email": "string",
    "password": "string",
    "password2": "string",
    "first_name": "string",
    "last_name": "string"
}
Response: {
    "user": {...},
    "tokens": {
        "refresh": "string",
        "access": "string"
    },
    "message": "User registered successfully"
}

1.2 Login
---------
POST /api/auth/login/
Body: {
    "username": "string",
    "password": "string"
}
Response: {
    "user": {...},
    "tokens": {
        "refresh": "string",
        "access": "string"
    },
    "message": "Login successful"
}

1.3 Logout
----------
POST /api/auth/logout/
Headers: Authorization: Bearer <access_token>
Body: {
    "refresh": "string"
}
Response: {
    "message": "Logout successful"
}

1.4 Get User Profile
--------------------
GET /api/auth/profile/
Headers: Authorization: Bearer <access_token>
Response: {
    "id": integer,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "date_joined": "datetime"
}

1.5 Update User Profile
-----------------------
PATCH /api/auth/profile/
Headers: Authorization: Bearer <access_token>
Body: {
    "first_name": "string",
    "last_name": "string",
    "email": "string"
}

1.6 Refresh Token
-----------------
POST /api/auth/token/refresh/
Body: {
    "refresh": "string"
}
Response: {
    "access": "string",
    "refresh": "string"
}

---

2. COMMUNITY ENDPOINTS
======================

2.1 List All Communities
------------------------
GET /api/communities/
Query Params: ?page=1 (optional)
Response: {
    "count": integer,
    "next": "url",
    "previous": "url",
    "results": [
        {
            "id": integer,
            "name": "string",
            "description": "string",
            "created_at": "datetime",
            "created_by": "username",
            "created_by_id": integer,
            "member_count": integer,
            "post_count": integer,
            "is_member": boolean
        }
    ]
}

2.2 Get Community Details
-------------------------
GET /api/communities/{id}/
Response: {
    "id": integer,
    "name": "string",
    "description": "string",
    "created_at": "datetime",
    "created_by": "username",
    "created_by_id": integer,
    "member_count": integer,
    "post_count": integer,
    "members": [
        {
            "id": integer,
            "user": "username",
            "username": "string",
            "joined_at": "datetime"
        }
    ],
    "is_member": boolean
}

2.3 Create Community
--------------------
POST /api/communities/
Headers: Authorization: Bearer <access_token>
Body: {
    "name": "string",
    "description": "string"
}
Response: {
    "id": integer,
    "name": "string",
    "description": "string"
}

2.4 Update Community
--------------------
PATCH /api/communities/{id}/
Headers: Authorization: Bearer <access_token>
Body: {
    "name": "string",
    "description": "string"
}
Note: Only creator can update

2.5 Delete Community
--------------------
DELETE /api/communities/{id}/
Headers: Authorization: Bearer <access_token>
Note: Only creator can delete

2.6 Join Community
------------------
POST /api/communities/{id}/join/
Headers: Authorization: Bearer <access_token>
Response: {
    "message": "Successfully joined <community_name>"
}

2.7 Leave Community
-------------------
POST /api/communities/{id}/leave/
Headers: Authorization: Bearer <access_token>
Response: {
    "message": "Successfully left <community_name>"
}
Note: Creator cannot leave their own community

2.8 Get Community Members
-------------------------
GET /api/communities/{id}/members/
Response: [
    {
        "id": integer,
        "user": "username",
        "username": "string",
        "joined_at": "datetime"
    }
]

---

3. POST ENDPOINTS
=================

3.1 List All Posts
------------------
GET /api/posts/
Query Params: 
  - ?page=1 (optional)
  - ?community=<id> (optional - filter by community)
Response: {
    "count": integer,
    "next": "url",
    "previous": "url",
    "results": [
        {
            "id": integer,
            "content": "string",
            "created_at": "datetime",
            "author": {
                "id": integer,
                "username": "string",
                "first_name": "string",
                "last_name": "string"
            },
            "community": integer,
            "community_name": "string",
            "like_count": integer,
            "is_liked": boolean
        }
    ]
}

3.2 Get Community Feed (Posts)
------------------------------
GET /api/posts/community/{community_id}/
Query Params: ?page=1 (optional)
Response: Same as 3.1 but filtered to specific community

3.3 Get Post Details
--------------------
GET /api/posts/{id}/
Response: Single post object (same structure as list item)

3.4 Create Post
---------------
POST /api/posts/
Headers: Authorization: Bearer <access_token>
Body: {
    "content": "string",
    "community": integer
}
Response: {
    "id": integer,
    "content": "string",
    "created_at": "datetime",
    "author": {...},
    "community": integer,
    "community_name": "string",
    "like_count": 0,
    "is_liked": false
}
Note: User must be a member of the community

3.5 Update Post
---------------
PATCH /api/posts/{id}/
Headers: Authorization: Bearer <access_token>
Body: {
    "content": "string"
}
Note: Only author can update

3.6 Delete Post
---------------
DELETE /api/posts/{id}/
Headers: Authorization: Bearer <access_token>
Note: Only author can delete

3.7 Like/Unlike Post (Toggle)
-----------------------------
POST /api/posts/{id}/like/
Headers: Authorization: Bearer <access_token>
Response: {
    "message": "Post liked" | "Post unliked",
    "is_liked": boolean,
    "like_count": integer
}

3.8 Get Post Likes
------------------
GET /api/posts/{id}/likes/
Response: [
    {
        "id": integer,
        "user": "username",
        "username": "string",
        "post": integer,
        "created_at": "datetime"
    }
]

---

TYPICAL USER FLOW
=================

1. Register/Login
   POST /api/auth/register/ or /api/auth/login/
   Save access and refresh tokens

2. View Communities
   GET /api/communities/

3. Join a Community
   POST /api/communities/{id}/join/

4. View Community Feed
   GET /api/posts/community/{community_id}/

5. Create a Post
   POST /api/posts/
   Body: {"content": "...", "community": id}

6. Like a Post
   POST /api/posts/{id}/like/

7. View Post Details with Likes
   GET /api/posts/{id}/
   GET /api/posts/{id}/likes/

---

ERROR RESPONSES
===============

All errors follow this format:
{
    "error": "Error message"
}

OR for validation errors:
{
    "field_name": ["Error message"]
}

Common HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

---

PAGINATION
==========

All list endpoints are paginated with 20 items per page.
Response includes:
- count: Total number of items
- next: URL to next page (null if last page)
- previous: URL to previous page (null if first page)
- results: Array of items

Use ?page=<number> to navigate pages.
"""
