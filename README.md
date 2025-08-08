# <center>Elden Ring Builds Community</center> 

## <center>A Django-based web application for the Elden Ring community to share, discover, and discuss character builds. Users can create detailed build guides, grace (like) their favorites, comment on builds, and connect with fellow Tarnished.</center>

### <center>[Link to the Website](https://elden-builds-85150946427d.herokuapp.com)</center>

## Features:

### User Stories:

### Authentication & User Management
- **As a new visitor**, I want to register for an account so that I can create and share my own builds
- **As a registered user**, I want to log in securely so that I can access my builds and community features
- **As a user**, I want to update my profile information so that other community members can learn about me

### Build Creation & Management
- **As a Tarnished**, I want to create detailed builds with weapons, armor, talismans, and spells so that I can share my character strategies
- **As a build creator**, I want autocomplete suggestions for equipment names so that I can quickly and accurately input my gear
- **As a user**, I want to upload screenshots of my character so that others can see how my build looks in-game
- **As a build author**, I want to categorize my builds (PvP, PvE, Boss Slaying) so that others can find builds for their playstyle
- **As a build creator**, I want to edit my published builds so that I can update them with improvements or corrections
- **As a build author**, I want to delete my builds so that I can remove outdated or unwanted content

### Build Discovery & Browsing
- **As a player**, I want to browse all community builds so that I can discover new character strategies
- **As a user**, I want to filter builds by category so that I can find builds suited for my preferred playstyle
- **As a Tarnished**, I want to search for builds by weapon or equipment name so that I can find builds using specific gear
- **As a user**, I want to view detailed build information including stats, equipment, and strategies so that I can understand how to recreate the build
- **As a mobile user**, I want the site to work well on my phone so that I can browse builds anywhere

### Community Interaction
- **As a community member**, I want to grace (like) builds that I find helpful so that I can show appreciation and bookmark favorites
- **As a user**, I want to comment on builds so that I can ask questions, provide feedback, or share experiences
- **As a build creator**, I want to receive notifications when someone comments on my builds so that I can engage with the community
- **As a commenter**, I want to edit or delete my comments so that I can correct mistakes or remove unwanted content
- **As a user**, I want to see my graced builds in my profile so that I can easily return to my favorites

### User Profile & Statistics
- **As a user**, I want to view my profile page so that I can see all my builds and activity in one place
- **As a community member**, I want to view other users' profiles so that I can see their builds and community contributions
- **As a build creator**, I want to see statistics about my builds (views, graces, comments) so that I can understand which content resonates with the community
- **As a user**, I want to see my total graces received so that I can track my contribution to the community

### Content Moderation & Quality
- **As a build creator**, I want to preview my build before publishing so that I can ensure it displays correctly
- **As a user**, I want build images to load quickly and display properly so that I have a smooth browsing experience

### Technical User Stories
- **As a user**, I want the site to load quickly so that I can browse builds efficiently
- **As a mobile user**, I want all features to work on my device so that I'm not limited by my platform
- **As a user**, I want my data to be secure so that my account and personal information are protected
- **As a user**, I want the site to work reliably so that I can depend on it for my Elden Ring needs

### Build Creation & Management
- **Detailed Build Forms**: Create comprehensive builds with weapons, armor, talismans, and spells
- **Auto-Complete Integration**: Smart suggestions powered by the Elden Ring Fan API
- **Image Uploads**: Upload multiple build screenshots via Cloudinary
- **Category System**: Organize builds by type (PvP, PvE, etc.)

### Community Features
- **Grace System**: Like and bookmark favorite builds (themed as "Grace")
- **Comments & Discussions**: Engage with the community through build comments
- **User Profiles**: Personalized profiles with build collections and statistics
- **Build Discovery**: Browse, filter, and search through community builds

### Elden Ring Theming
- **Authentic Design**: Dark theme with golden accents matching the game's aesthetic
- **Grace-Blessed Terminology**: Custom "Grace" system instead of generic likes
- **Responsive UI**: Mobile-friendly Bootstrap design with custom styling

## Tech Stack

- **Backend**: Django 5.2.4 (Python)
- **Database**: PostgreSQL with SQLite for development
- **Frontend**: Bootstrap 5 with custom CSS and JavaScript
- **File Storage**: Cloudinary for image management
- **API Integration**: Elden Ring Fan API for autocomplete
- **Deployment**: Configured for Heroku with Gunicorn and WhiteNoise

## Project Structure

```
Elden_Builds/
├── accounts/           # User authentication and management
├── builds/             # Core build functionality
│   ├── models.py      # Build, Comment, and related models
│   ├── views.py       # Build CRUD operations
│   ├── forms.py       # Build creation and edit forms
│   └── urls.py        # Build-related URL patterns
├── users/              # User profiles and notifications
├── static/             # CSS, JS, and image assets
│   ├── css/           # Custom stylesheets
│   ├── js/            # JavaScript functionality
│   └── images/        # Static images and icons
├── templates/          # Django templates
├── utils/              # Utility functions (Cloudinary, etc.)
└── eldenring_project/  # Main project settings
```
### API Integration
The application integrates with the [Elden Ring Fan API](https://eldenring.fanapis.com/api) for:
- Weapon autocomplete suggestions
- Armor and equipment data
- Talisman information
- Spell and incantation data

## Datebase

## User Stories

## Key Features Deep Dive

### Grace System
The application uses "Grace" instead of traditional "likes" to match Elden Ring's lore, where Grace guides and blesses players on their journey.

### Smart Autocomplete
Powered by the Elden Ring Fan API, the build forms provide intelligent suggestions as you type weapon names, making build creation fast and accurate.

### Responsive Design
The interface adapts seamlessly from desktop to mobile, ensuring a great experience for users on any device.

## UX

## WireFrames

## AI

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- **FromSoftware** for creating Elden Ring
- **Elden Ring Fan API** for providing Game Data
- **Django Community** for the excellent Web Framework
- **Bootstrap Team** for the responsive CSS Framework

---

*May the Grace guide your builds*