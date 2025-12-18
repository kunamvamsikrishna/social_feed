"""
Quick Test Script for API Endpoints
====================================

Run these commands to test the API (replace values as needed):

# 1. Create a superuser first
python manage.py createsuperuser

# 2. Or test with curl/httpie/Postman using these examples:

# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
# Save the access token from response

# List communities (no auth needed)
curl http://localhost:8000/api/communities/

# Create a community (requires auth)
curl -X POST http://localhost:8000/api/communities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Python Developers",
    "description": "A community for Python enthusiasts"
  }'

# Join a community
curl -X POST http://localhost:8000/api/communities/1/join/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Create a post in community
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Hello from Python!",
    "community": 1
  }'

# Get community feed
curl http://localhost:8000/api/posts/community/1/

# Like a post
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get post likes
curl http://localhost:8000/api/posts/1/likes/
"""

# Python test script using requests
TEST_SCRIPT = """
import requests

BASE_URL = "http://localhost:8000/api"

# 1. Register
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
}
response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
print("Register:", response.status_code, response.json())
tokens = response.json()['tokens']
access_token = tokens['access']

# 2. List communities
response = requests.get(f"{BASE_URL}/communities/")
print("Communities:", response.status_code)

# 3. Create community
headers = {"Authorization": f"Bearer {access_token}"}
community_data = {
    "name": "Test Community",
    "description": "A test community"
}
response = requests.post(f"{BASE_URL}/communities/", json=community_data, headers=headers)
print("Create Community:", response.status_code, response.json())
community_id = response.json()['id']

# 4. Create post
post_data = {
    "content": "Hello World!",
    "community": community_id
}
response = requests.post(f"{BASE_URL}/posts/", json=post_data, headers=headers)
print("Create Post:", response.status_code, response.json())
post_id = response.json()['id']

# 5. Like post
response = requests.post(f"{BASE_URL}/posts/{post_id}/like/", headers=headers)
print("Like Post:", response.status_code, response.json())

# 6. Get community feed
response = requests.get(f"{BASE_URL}/posts/community/{community_id}/")
print("Community Feed:", response.status_code, len(response.json()['results']), "posts")

print("\\nAll tests completed successfully!")
"""

if __name__ == "__main__":
    print("To run the Python test script:")
    print("1. Install requests: pip install requests")
    print("2. Run the TEST_SCRIPT code above")
