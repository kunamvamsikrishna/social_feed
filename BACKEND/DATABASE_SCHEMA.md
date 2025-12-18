# Database Schema - Mini Community Social Feed

## Overview
This document describes the relational database schema for the community-based social platform.

## Entity Relationship Diagram

```
┌─────────────────┐
│      USER       │ (Django's built-in User model)
│  (auth_user)    │
├─────────────────┤
│ • id            │
│ • username      │
│ • email         │
│ • password      │
│ • first_name    │
│ • last_name     │
│ • date_joined   │
└────────┬────────┘
         │
         │ creates (1:Many)
         ▼
┌─────────────────────────┐
│      COMMUNITY          │
├─────────────────────────┤
│ • id (PK)               │
│ • name (unique)         │
│ • description           │
│ • created_at            │
│ • created_by (FK→User)  │
├─────────────────────────┤
│ Properties:             │
│ • member_count()        │
│ • post_count()          │
└────────┬────────────────┘
         │
         │ has (Many:Many via CommunityMember)
         │
┌────────┴─────────────────┐
│   COMMUNITYMEMBER        │
├──────────────────────────┤
│ • id (PK)                │
│ • user (FK→User)         │
│ • community (FK→Comm)    │
│ • joined_at              │
├──────────────────────────┤
│ Constraints:             │
│ • unique(user,community) │
└──────────────────────────┘
         │
         │ authorizes posting
         ▼
┌─────────────────────────┐
│         POST            │
├─────────────────────────┤
│ • id (PK)               │
│ • content               │
│ • created_at            │
│ • author (FK→User)      │
│ • community (FK→Comm)   │
├─────────────────────────┤
│ Properties:             │
│ • like_count()          │
│ • is_liked_by(user)     │
├─────────────────────────┤
│ Validation:             │
│ • Author must be member │
└────────┬────────────────┘
         │
         │ receives (1:Many)
         ▼
┌─────────────────────────┐
│         LIKE            │
├─────────────────────────┤
│ • id (PK)               │
│ • user (FK→User)        │
│ • post (FK→Post)        │
│ • created_at            │
├─────────────────────────┤
│ Constraints:            │
│ • unique(user, post)    │
└─────────────────────────┘
```

## Models Description

### 1. User (Django Built-in)
- **Purpose**: Handles authentication and user identity
- **Key Features**: 
  - Username/email/password authentication
  - Tracks all user actions across the platform

### 2. Community
- **Purpose**: Represents a community where users can gather and share content
- **Key Features**:
  - Unique community names
  - Creator tracking
  - Automatic creator membership
  - Tracks member and post counts
- **Relationships**:
  - Created by one User
  - Has many CommunityMembers
  - Has many Posts

### 3. CommunityMember
- **Purpose**: Junction table managing many-to-many relationship between Users and Communities
- **Key Features**:
  - Prevents duplicate memberships (unique constraint)
  - Tracks when users joined
  - Validates posting permissions
- **Relationships**:
  - Belongs to one User
  - Belongs to one Community

### 4. Post
- **Purpose**: Content created by users within communities
- **Key Features**:
  - Validates author is a community member before saving
  - Tracks likes received
  - Provides helper methods for like checking
- **Relationships**:
  - Created by one User (author)
  - Belongs to one Community
  - Has many Likes
- **Business Rules**:
  - Author must be a member of the community

### 5. Like
- **Purpose**: Tracks user interactions with posts
- **Key Features**:
  - Prevents duplicate likes (unique constraint)
  - Timestamped for analytics
- **Relationships**:
  - Made by one User
  - Applies to one Post

## Database Indexes

Performance optimizations through strategic indexing:

### CommunityMember
- Index on `joined_at` (descending) - Fast membership listings

### Post
- Index on `created_at` (descending) - Fast feed generation
- Composite index on `(community, created_at)` - Optimized community feeds

### Like
- Composite index on `(post, created_at)` - Fast like counts and listings

## Business Rules

1. **Community Creation**
   - Any authenticated user can create a community
   - Creator automatically becomes first member

2. **Community Membership**
   - Users can join any community
   - One membership per user per community
   - Membership required for posting

3. **Posting**
   - Only community members can create posts
   - Validated at model level (save method)
   - One post can belong to one community only

4. **Liking**
   - Authenticated users can like any post
   - One like per user per post
   - No membership requirement for viewing/liking

## API Implications

This schema supports the following operations:

1. **View Communities** - Query Community model, ordered by created_at
2. **Join Community** - Create CommunityMember record
3. **View Feed** - Query Post filtered by community, ordered by created_at
4. **Create Post** - Create Post with membership validation
5. **Like Post** - Create Like with uniqueness constraint

## Future Enhancements (Not Implemented)

Potential extensions to consider:
- Comments on posts
- Post media attachments
- Community categories/tags
- User profiles and avatars
- Follow/unfollow users
- Notifications
- Direct messaging
- Post editing history
- Soft deletes
- Community moderators/roles
