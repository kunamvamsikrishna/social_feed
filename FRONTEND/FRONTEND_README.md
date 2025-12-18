# Social Feed - Frontend (React + Vite)

## 🎉 Complete Frontend Implementation

All pages and features have been built successfully!

## 📱 Pages Created

### 1. **Login Page** (`/login`)
- Username/password authentication
- Error handling
- Link to register
- Auto-redirect after login

### 2. **Register Page** (`/register`)
- Full user registration form
- Password confirmation
- Field validation
- Auto-login after registration

### 3. **Communities List** (`/communities`)
- Browse all communities
- View stats (members, posts)
- Join communities
- Create new community (modal)
- Member badge display

### 4. **Community Detail** (`/communities/:id`)
- View community info
- Join/Leave functionality
- Community feed (posts)
- Create post (members only)
- Delete own posts
- Like/unlike posts

## 🧩 Components Created

### **Navbar**
- Branding and navigation
- User menu with avatar
- Login/Register buttons (guests)
- Logout functionality

### **PostCard**
- Display post content
- Author info with avatar
- Like button with count
- Delete button (author only)
- Relative timestamps

### **CreatePost**
- Modal form for creating posts
- Character count (5000 limit)
- Community context
- Error handling

### **ProtectedRoute**
- Authentication guard
- Auto-redirect to login
- Loading state

## 🔧 Services & Context

### **API Service** (`services/api.js`)
- Axios instance with interceptors
- Token management
- Auto token refresh on 401
- All CRUD endpoints:
  - Auth: register, login, logout, profile
  - Communities: CRUD + join/leave
  - Posts: CRUD + like/unlike

### **AuthContext** (`context/AuthContext.jsx`)
- Global authentication state
- User management
- Login/Register/Logout functions
- Token storage
- Auto-load user on mount

## 🎨 Styling

All pages have custom CSS with:
- Modern gradient design
- Responsive layouts
- Smooth transitions
- Hover effects
- Mobile-friendly

## 🚀 How to Run

```bash
cd FRONTEND

# Install dependencies (already done)
npm install

# Start development server
npm run dev
```

Server will run at: **http://localhost:5173**

## 🔗 API Integration

Backend API: `http://127.0.0.1:8000/api`

All API calls are configured in `services/api.js` with:
- Automatic JWT token injection
- Token refresh logic
- CORS handling
- Error handling

## 📋 Features Implemented

✅ User Authentication (JWT)
✅ Community Browsing
✅ Community Creation
✅ Join/Leave Communities
✅ View Community Feeds
✅ Create Posts (members only)
✅ Delete Posts (author only)
✅ Like/Unlike Posts
✅ Responsive Design
✅ Error Handling
✅ Loading States
✅ Protected Routes

## 🎯 User Flow

1. **First Time User**:
   - Visit app → See communities list
   - Click Register → Create account
   - Auto-login → Redirected to communities

2. **Existing User**:
   - Click Login → Enter credentials
   - Redirected to communities
   - Browse and join communities

3. **Community Interaction**:
   - View community → See details & feed
   - Join community → Gain posting access
   - Create post → Share content
   - Like posts → Interact with community
   - Leave community → Remove membership

## 📁 Project Structure

```
FRONTEND/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          # Navigation bar
│   │   ├── Navbar.css
│   │   ├── PostCard.jsx        # Post display
│   │   ├── PostCard.css
│   │   ├── CreatePost.jsx      # Create post modal
│   │   ├── CreatePost.css
│   │   └── ProtectedRoute.jsx  # Auth guard
│   ├── pages/
│   │   ├── Login.jsx           # Login page
│   │   ├── Register.jsx        # Registration page
│   │   ├── Auth.css            # Auth pages styles
│   │   ├── Communities.jsx     # Communities list
│   │   ├── Communities.css
│   │   ├── CommunityDetail.jsx # Community & feed
│   │   └── CommunityDetail.css
│   ├── context/
│   │   └── AuthContext.jsx     # Auth state management
│   ├── services/
│   │   └── api.js              # API service layer
│   ├── App.jsx                 # Main app & routing
│   ├── App.css
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles
├── package.json
└── vite.config.js
```

## 🛠️ Technologies Used

- **React 18** - UI library
- **React Router v6** - Routing
- **Axios** - HTTP client
- **Vite** - Build tool
- **CSS3** - Styling

## ✨ Next Steps (Optional Enhancements)

- [ ] Add post comments
- [ ] User profiles
- [ ] Search functionality
- [ ] Image uploads
- [ ] Notifications
- [ ] Dark mode
- [ ] Real-time updates (WebSocket)

## 🐛 Troubleshooting

**CORS Errors**:
- Ensure backend is running on port 8000
- Check CORS settings in Django settings.py

**Authentication Issues**:
- Clear localStorage and login again
- Check token expiry settings

**API Errors**:
- Verify backend is running
- Check API endpoint URLs

## 📞 Support

Built as part of the Mini Community Social Feed project.
Backend API documentation: See BACKEND/API_ENDPOINTS.py

---

**Status**: ✅ All pages complete and ready to use!

**Frontend URL**: http://localhost:5173
**Backend URL**: http://127.0.0.1:8000
