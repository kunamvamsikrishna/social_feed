# Social Feed - Community-Based Social Platform

A full-stack web application that allows users to create and join communities, share posts, and interact with content through likes. Built with Django REST Framework and React, this platform provides a modern, secure, and scalable solution for community-driven social networking.

## 📋 Features

### User Management
- **Secure Authentication**: JWT-based authentication with access and refresh tokens
- **User Registration**: Create accounts with email verification
- **Profile Management**: Update user information and view profile details

### Community Features
- **Create Communities**: Users can create their own communities with custom names and descriptions
- **Join/Leave Communities**: Discover and join communities of interest
- **Community Feed**: View posts specific to each community
- **Membership Management**: Automatic creator membership and member tracking
- **Community Statistics**: Real-time member count and post count

### Post & Interaction Features
- **Create Posts**: Share thoughts and content within communities (members only)
- **Delete Posts**: Authors can remove their own posts
- **Like System**: Like and unlike posts with real-time count updates
- **Protected Actions**: Only community members can view, post, and like content
- **Real-time Updates**: Instant UI updates without page refresh

### Security & Access Control
- **Protected Routes**: Authentication required for sensitive pages
- **Membership Validation**: Backend validation for community-specific actions
- **Token Blacklisting**: Secure logout with token invalidation
- **CORS Configuration**: Secure cross-origin resource sharing

## 🛠️ Tech Stack

### Frontend
- **React 19** - Modern UI library with hooks
- **Vite (Rolldown)** - Fast build tool and dev server
- **React Router v7** - Client-side routing
- **Axios** - HTTP client with interceptors
- **Context API** - Global state management for authentication

### Backend
- **Django 6.0** - High-level Python web framework
- **Django REST Framework 3.16** - RESTful API toolkit
- **Simple JWT 5.5** - JSON Web Token authentication
- **Django CORS Headers 4.9** - Cross-Origin Resource Sharing
- **SQLite** - Development database (easily switchable to PostgreSQL/MySQL)

### Authentication
- **JWT (JSON Web Tokens)** with access and refresh token rotation
- **Token Blacklisting** for secure logout
- **Access Token Lifetime**: 1 day
- **Refresh Token Lifetime**: 7 days

### Additional Tools
- **Python 3.12** - Backend runtime
- **Node.js** - Frontend runtime
- **Git** - Version control

## 📁 Folder Structure

### Frontend Structure
```
FRONTEND/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Navbar.jsx       # Navigation bar with user menu
│   │   ├── PostCard.jsx     # Post display component
│   │   ├── CreatePost.jsx   # Post creation modal
│   │   └── ProtectedRoute.jsx  # Route guard component
│   ├── context/             # React Context providers
│   │   └── AuthContext.jsx  # Authentication state management
│   ├── pages/               # Page components
│   │   ├── Login.jsx        # Login page
│   │   ├── Register.jsx     # Registration page
│   │   ├── Communities.jsx  # Communities list page
│   │   └── CommunityDetail.jsx  # Community detail and feed
│   ├── services/            # API and external services
│   │   └── api.js           # Axios instance and API calls
│   ├── App.jsx              # Main app component with routing
│   ├── main.jsx             # Application entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
└── package.json             # Dependencies and scripts
```

### Backend Structure
```
BACKEND/
├── social_feed_prj/         # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── users/                   # User app
│   ├── serializers.py       # User data serialization
│   ├── views.py             # Auth endpoints (register, login, logout)
│   └── urls.py              # User routing
├── communities/             # Communities app
│   ├── models.py            # Community and CommunityMember models
│   ├── serializers.py       # Community serialization
│   ├── views.py             # Community CRUD and join/leave
│   ├── urls.py              # Community routing
│   └── admin.py             # Django admin configuration
├── posts/                   # Posts app
│   ├── models.py            # Post and Like models
│   ├── serializers.py       # Post serialization
│   ├── views.py             # Post CRUD and like toggle
│   ├── urls.py              # Post routing
│   └── admin.py             # Django admin configuration
├── manage.py                # Django management script
├── db.sqlite3               # SQLite database
└── myenv/                   # Python virtual environment
```

## 🔐 Environment Variables

### Backend (.env - Optional)
While the current setup uses default Django settings, for production deployment, create a `.env` file in the `BACKEND/` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/social_feed

# JWT Settings
ACCESS_TOKEN_LIFETIME_MINUTES=1440
REFRESH_TOKEN_LIFETIME_DAYS=7

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com
```

### Frontend (.env - Optional)
Create a `.env` file in the `FRONTEND/` directory for API configuration:

```env
# API Base URL
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 🚀 Frontend Setup

### Prerequisites
- **Node.js** (v18 or higher)
- **npm** or **yarn** package manager

### Installation Steps

1. **Navigate to Frontend Directory**
   ```bash
   cd FRONTEND
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Access the Application**
   - Open browser and navigate to: `http://localhost:5173`

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## ⚙️ Backend Setup

### Prerequisites
- **Python 3.12** or higher
- **pip** package manager

### Installation Steps

1. **Navigate to Backend Directory**
   ```bash
   cd BACKEND
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv myenv
   ```

3. **Activate Virtual Environment**
   - Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
   ```

5. **Apply Database Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Admin Account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow prompts to create an admin account for accessing Django admin panel.

7. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the API**
   - API Base: `http://127.0.0.1:8000/api/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`

## 🗄️ Database Design Overview

### Models and Relationships

#### **User Model** (Django built-in)
- Default Django user with authentication fields
- Fields: `id`, `username`, `email`, `first_name`, `last_name`, `password`

#### **Community Model**
- Represents a community created by users
- Fields: `id`, `name`, `description`, `created_at`, `created_by`
- Relationships:
  - One creator (User) per community
  - Many members through CommunityMember
  - Many posts

#### **CommunityMember Model**
- Manages user membership in communities
- Fields: `id`, `user`, `community`, `joined_at`
- Relationships:
  - Links User to Community (many-to-many through table)
  - Unique constraint: One user can only join a community once

#### **Post Model**
- Represents content created by users in communities
- Fields: `id`, `content`, `created_at`, `author`, `community`
- Relationships:
  - Belongs to one User (author)
  - Belongs to one Community
  - Has many Likes
- Validation: Author must be a member of the community

#### **Like Model**
- Represents user likes on posts
- Fields: `id`, `user`, `post`, `created_at`
- Relationships:
  - Links User to Post
  - Unique constraint: One user can only like a post once

### Database Indexes
- `created_at` fields indexed for efficient sorting
- Composite index on `(community, created_at)` for post queries
- Unique constraints on membership and likes to prevent duplicates

## 🔑 Authentication Flow

### Registration Process
1. User submits registration form with:
   - First name, Last name
   - Username (unique)
   - Email (unique)
   - Password (with confirmation)

2. Backend validates data and creates user account

3. System generates JWT access and refresh tokens

4. Tokens stored in localStorage on frontend

5. User automatically logged in and redirected to communities page

### Login Process
1. User enters username and password

2. Backend authenticates credentials

3. If valid, generates new JWT tokens

4. Frontend stores tokens in localStorage

5. User redirected to communities page

### Token Management
- **Access Token**: Short-lived (1 day), sent with every API request
- **Refresh Token**: Long-lived (7 days), used to get new access tokens
- **Axios Interceptor**: Automatically attaches access token to requests
- **Auto Refresh**: Intercepts 401 errors and refreshes tokens automatically
- **Token Storage**: localStorage (access_token, refresh_token)

### Logout Process
1. User clicks logout

2. Frontend sends refresh token to backend

3. Backend blacklists the token (prevents reuse)

4. Frontend clears localStorage

5. User redirected to login page

### Protected Routes
- Frontend: `ProtectedRoute` component checks authentication state
- Backend: `IsAuthenticated` permission class on views
- Unauthenticated users redirected to login page

## 📡 API Endpoints

### Authentication Routes
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login user | No |
| POST | `/api/auth/logout/` | Logout and blacklist token | Yes |
| GET | `/api/auth/profile/` | Get current user profile | Yes |
| PUT | `/api/auth/profile/` | Update user profile | Yes |

### Community Routes
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/communities/` | List all communities (paginated) | No |
| POST | `/api/communities/` | Create new community | Yes |
| GET | `/api/communities/{id}/` | Get community details | No |
| PUT | `/api/communities/{id}/` | Update community (creator only) | Yes |
| DELETE | `/api/communities/{id}/` | Delete community (creator only) | Yes |
| POST | `/api/communities/{id}/join/` | Join community | Yes |
| POST | `/api/communities/{id}/leave/` | Leave community | Yes |
| GET | `/api/communities/{id}/members/` | List community members | No |

### Post Routes
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/posts/` | List all posts (optional community filter) | No |
| POST | `/api/posts/` | Create new post (members only) | Yes |
| GET | `/api/posts/{id}/` | Get post details | No |
| PUT | `/api/posts/{id}/` | Update post (author only) | Yes |
| DELETE | `/api/posts/{id}/` | Delete post (author only) | Yes |
| POST | `/api/posts/{id}/like/` | Toggle like on post (members only) | Yes |
| GET | `/api/posts/{id}/likes/` | List users who liked post | No |
| GET | `/api/posts/community/{id}/` | Get community feed (members only) | Yes |

### Request/Response Examples

**Register User**
```json
POST /api/auth/register/
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123",
  "password2": "securepass123"
}

Response: 201 Created
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully"
}
```

**Create Community**
```json
POST /api/communities/
Authorization: Bearer <access_token>
{
  "name": "Tech Enthusiasts",
  "description": "A community for technology lovers"
}

Response: 201 Created
{
  "id": 1,
  "name": "Tech Enthusiasts",
  "description": "A community for technology lovers",
  "created_at": "2025-12-18T10:30:00Z",
  "created_by": "johndoe",
  "created_by_id": 1,
  "member_count": 1,
  "post_count": 0,
  "is_member": true
}
```

## 🏃 Running the Full Project

### Development Mode

1. **Start Backend Server**
   ```bash
   # Terminal 1: Navigate to backend and activate venv
   cd BACKEND
   myenv\Scripts\activate  # Windows
   python manage.py runserver
   ```

2. **Start Frontend Server**
   ```bash
   # Terminal 2: Navigate to frontend
   cd FRONTEND
   npm run dev
   ```

3. **Access Application**
   - Frontend: `http://localhost:5173`
   - Backend API: `http://127.0.0.1:8000/api/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`

### Execution Order
1. Always start the **backend server first** (Django)
2. Then start the **frontend dev server** (Vite)
3. Frontend will make API calls to backend automatically

### Testing the Application

1. **Register a new account** at `/register`
2. **Login** with your credentials at `/login`
3. **Create a community** from the communities page
4. **Join existing communities** to see their content
5. **Create posts** within communities you've joined
6. **Like and interact** with posts from other members
7. **Access admin panel** at `/admin/` with superuser credentials

## 🚀 Future Improvements

### Features
- **User Profiles**: Enhanced profile pages with bio, avatar, and activity feed
- **Comments System**: Add threaded comments on posts
- **Real-time Notifications**: WebSocket integration for instant updates
- **Media Uploads**: Support for images and videos in posts
- **Search Functionality**: Full-text search for communities and posts
- **Trending Communities**: Algorithm-based community recommendations
- **Private Communities**: Invite-only communities with approval system
- **Moderation Tools**: Report system and community moderators
- **Direct Messaging**: Private messages between users
- **Activity Feed**: Personalized feed based on joined communities

### Technical Enhancements
- **PostgreSQL Migration**: Switch from SQLite to PostgreSQL for production
- **Redis Caching**: Improve performance with caching layer
- **Docker Containerization**: Simplify deployment with Docker
- **CI/CD Pipeline**: Automated testing and deployment
- **Email Verification**: Verify email addresses during registration
- **Password Reset**: Forgot password functionality
- **Rate Limiting**: Prevent abuse with API rate limiting
- **File Storage**: AWS S3 or similar for media storage
- **Mobile App**: React Native version for iOS and Android
- **PWA Support**: Progressive Web App capabilities

### UI/UX Improvements
- **Dark Mode**: Theme switching capability
- **Infinite Scroll**: Load more posts dynamically
- **Skeleton Loaders**: Better loading states
- **Rich Text Editor**: Enhanced post creation with formatting
- **Emoji Support**: Reactions and emoji picker
- **Responsive Design**: Better mobile experience
- **Accessibility**: WCAG 2.1 compliance

---

## 📝 Usage Notes

### For Developers
- This project uses Django's development server and SQLite, which are **not suitable for production**
- For production deployment, configure:
  - PostgreSQL or MySQL database
  - Gunicorn or uWSGI as WSGI server
  - Nginx as reverse proxy
  - Environment variables for sensitive data
  - HTTPS/SSL certificates

### Best Practices
- Always activate the virtual environment before running Django commands
- Keep frontend and backend terminals separate for easier debugging
- Check browser console for frontend errors
- Check terminal output for backend errors
- Use Django admin panel for data inspection and management

### Common Commands
```bash
# Backend
python manage.py makemigrations  # Create new migrations
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin user
python manage.py shell          # Django shell for testing

# Frontend
npm install <package>           # Add new package
npm run build                   # Build for production
```

---

## 🤝 Contributing

This is a learning project. Feel free to fork, experiment, and enhance the codebase!

## 📄 License

This project is open source and available for educational purposes.

---

**Built with ❤️ using Django and React**
#   s o c i a l _ f e e d  
 #   s o c i a l _ f e e d  
 