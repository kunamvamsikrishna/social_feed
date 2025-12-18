"""
QUICK START GUIDE
=================

Follow these steps to get the API running in 5 minutes!

STEP 1: VERIFY INSTALLATION
----------------------------
✓ Python 3.8+ installed
✓ Virtual environment activated (myenv)
✓ All packages installed (see requirements.minimal.txt)

STEP 2: DATABASE SETUP
----------------------
# Already completed! Migrations have been run.
# Database file: db.sqlite3

STEP 3: START SERVER
--------------------
Command:
    python manage.py runserver

Expected output:
    Starting development server at http://127.0.0.1:8000/

✅ Server is currently running!

STEP 4: TEST THE API
--------------------

Option A: Using Browser
- Visit: http://127.0.0.1:8000/api/communities/
- You should see an empty list: {"count": 0, "results": []}

Option B: Using curl (in new terminal)

1. Register a user:
curl -X POST http://127.0.0.1:8000/api/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"email\":\"test@test.com\",\"password\":\"Test123!@#\",\"password2\":\"Test123!@#\",\"first_name\":\"Test\",\"last_name\":\"User\"}"

2. Save the access token from response, then create a community:
curl -X POST http://127.0.0.1:8000/api/communities/ ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE" ^
  -d "{\"name\":\"Python Community\",\"description\":\"Learn Python together\"}"

3. View communities:
curl http://127.0.0.1:8000/api/communities/

Option C: Using Python script
Run: python test_api.py
(Edit the script with your preferred test data)

STEP 5: ADMIN INTERFACE (Optional)
-----------------------------------
1. Create superuser:
   python manage.py createsuperuser

2. Visit admin:
   http://127.0.0.1:8000/admin/

3. Login with superuser credentials

4. Explore Communities, Posts, Likes data

STEP 6: FOR FRONTEND DEVELOPERS
--------------------------------
Base URL: http://127.0.0.1:8000/api

Key Endpoints:
- Register: POST /api/auth/register/
- Login: POST /api/auth/login/
- Communities: GET /api/communities/
- Join Community: POST /api/communities/{id}/join/
- Community Feed: GET /api/posts/community/{id}/
- Create Post: POST /api/posts/
- Like Post: POST /api/posts/{id}/like/

Authentication:
- Include header: Authorization: Bearer {access_token}

CORS:
- Configured for: http://localhost:3000
- Ready for React development

TROUBLESHOOTING
---------------

Problem: Server not starting
Solution: Check if port 8000 is free, or use: python manage.py runserver 8001

Problem: Module not found
Solution: Activate virtual environment, run: pip install -r requirements.minimal.txt

Problem: Database error
Solution: Delete db.sqlite3, run: python manage.py migrate

Problem: 401 Unauthorized
Solution: Check token is included in Authorization header

Problem: 403 Forbidden
Solution: Check user has permission (e.g., must be member to post)

USEFUL COMMANDS
---------------

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell (for testing models)
python manage.py shell

# Check for errors
python manage.py check

# Run tests (if you add tests)
python manage.py test

NEXT STEPS
----------

1. Create some test data via admin interface
2. Test all endpoints using Postman/Thunder Client
3. Review API_ENDPOINTS.py for complete documentation
4. Start building your React frontend!

SUPPORT
-------

Documentation:
- API_ENDPOINTS.py - Complete API reference
- README.md - Full project documentation
- PROJECT_SUMMARY.py - Feature overview
- test_api.py - Example usage

Database Schema:
- DATABASE_SCHEMA.md - Complete schema documentation

CURRENT STATUS
--------------

✅ Server Running: http://127.0.0.1:8000/
✅ Database: Initialized and migrated
✅ Apps: users, communities, posts
✅ Endpoints: 20+ RESTful endpoints
✅ Authentication: JWT with refresh tokens
✅ CORS: Configured for frontend
✅ Admin: Available at /admin/

Ready to go! 🚀
"""

if __name__ == "__main__":
    print(__doc__)
