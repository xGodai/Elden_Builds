# Elden Ring Builds Community - Database Schema

## Database Diagram (Text Representation)

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│       User          │     │    UserProfile      │     │    Notification     │
│   (Django Built-in) │     │                     │     │                     │
├─────────────────────┤     ├─────────────────────┤     ├─────────────────────┤
│ • id (PK)          │◄────┤ • id (PK)          │     │ • id (PK)          │
│ • username         │     │ • user_id (FK)     │     │ • recipient_id (FK)│──┐
│ • email            │     │ • display_name     │     │ • sender_id (FK)   │  │
│ • first_name       │     │ • bio              │     │ • notification_type│  │
│ • last_name        │     │ • profile_picture  │     │ • build_id (FK)    │  │
│ • password         │     │ • location         │     │ • comment_id (FK)  │  │
│ • date_joined      │     │ • favorite_weapon  │     │ • message          │  │
│ • is_active        │     │ • notify_on_*      │     │ • is_read          │  │
│ • is_staff         │     │ • created_at       │     │ • created_at       │  │
│ • last_login       │     │ • updated_at       │     └─────────────────────┘  │
└─────────────────────┘     └─────────────────────┘                            │
         │                                                                     │
         │                                                                     │
         │ ┌─────────────────────┐                                            │
         └►│       Build         │◄───────────────────────────────────────────┘
           │                     │
           ├─────────────────────┤
           │ • id (PK)          │
           │ • user_id (FK)     │────┐
           │ • title            │    │
           │ • description      │    │
           │ • weapons          │    │
           │ • armor            │    │
           │ • talismans        │    │
           │ • spells           │    │
           │ • category         │    │
           │ • created_at       │    │
           └─────────────────────┘    │
                    │                 │
                    │                 │
                    ▼                 │
           ┌─────────────────────┐    │
           │    BuildImage       │    │
           │                     │    │
           ├─────────────────────┤    │
           │ • id (PK)          │    │
           │ • build_id (FK)    │────┘
           │ • image            │
           │ • is_primary       │
           │ • caption          │
           │ • uploaded_at      │
           └─────────────────────┘
                    │
                    │
                    ▼
           ┌─────────────────────┐
           │      Comment        │
           │                     │
           ├─────────────────────┤
           │ • id (PK)          │
           │ • build_id (FK)    │
           │ • user_id (FK)     │
           │ • content          │
           │ • created_at       │
           │ • updated_at       │
           └─────────────────────┘
                    │
                    │
                    ▼
           ┌─────────────────────┐
           │    CommentVote      │
           │                     │
           ├─────────────────────┤
           │ • id (PK)          │
           │ • comment_id (FK)  │
           │ • user_id (FK)     │
           │ • vote_type        │
           │ • created_at       │
           └─────────────────────┘

           ┌─────────────────────┐
           │   Build_liked_by    │
           │   (Many-to-Many)    │
           ├─────────────────────┤
           │ • id (PK)          │
           │ • build_id (FK)    │
           │ • user_id (FK)     │
           └─────────────────────┘
```

## Entity Relationships

### Core Entities

1. **User** (Django's built-in User model)
   - Primary entity for authentication and user management
   - Extended by UserProfile for additional fields

2. **UserProfile** (One-to-One with User)
   - Extended user information
   - Profile customization and notification preferences
   - Profile pictures stored in Cloudinary

3. **Build** (Many-to-One with User)
   - Core entity representing character builds
   - Contains build details (weapons, armor, talismans, spells)
   - Category classification (PvE, PvP, Both)
   - Many-to-Many relationship with User through "liked_by"

4. **BuildImage** (Many-to-One with Build)
   - Stores multiple images per build (max 3)
   - Cloudinary integration for image storage
   - Primary image designation system

5. **Comment** (Many-to-One with Build and User)
   - User comments on builds
   - Supports threaded discussions
   - Voting system through CommentVote

6. **CommentVote** (Many-to-One with Comment and User)
   - Upvote/downvote system for comments
   - Unique constraint: one vote per user per comment

7. **Notification** (Many-to-One with User)
   - Real-time notification system
   - Links to builds and comments
   - Read/unread status tracking

### Key Relationships

- **User → UserProfile**: One-to-One (Profile extension)
- **User → Build**: One-to-Many (User creates multiple builds)
- **User ↔ Build**: Many-to-Many (Users can "grace" multiple builds)
- **Build → BuildImage**: One-to-Many (Multiple images per build)
- **Build → Comment**: One-to-Many (Multiple comments per build)
- **User → Comment**: One-to-Many (User creates multiple comments)
- **Comment → CommentVote**: One-to-Many (Comments can have multiple votes)
- **User → CommentVote**: One-to-Many (Users can vote on multiple comments)
- **User → Notification**: One-to-Many (Users receive multiple notifications)

### Constraints and Business Rules

1. **BuildImage**: Maximum 3 images per build
2. **CommentVote**: Unique constraint (user + comment)
3. **Build Grace System**: Many-to-Many relationship for "liked_by"
4. **Primary Image**: Only one primary image per build
5. **Notification Types**: Limited to predefined types (build_like, build_comment, etc.)

### Indexes

- **Notification**: Indexed on (recipient, created_at) and (recipient, is_read)
- **Comment**: Ordered by created_at (descending)
- **BuildImage**: Ordered by is_primary (descending), then uploaded_at

This schema supports the "Grace" system (likes), commenting with voting, image management, user profiles, and real-time notifications - all themed around the Elden Ring universe.
