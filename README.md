# Elden Ring Builds Community 

A Django-based web application for the Elden Ring community to share, discover, and discuss character builds. Users can create detailed build guides, grace (like) their favorites, comment on builds, and connect with fellow Tarnished.

## Features

### Build Creation & Management
- **Detailed Build Forms**: Create comprehensive builds with weapons, armor, talismans, and spells
- **Auto-Complete Integration**: Smart suggestions powered by the Elden Ring Fan API
- **Image Uploads**: Upload multiple build screenshots via Cloudinary
- **Category System**: Organize builds by type (PvP, PvE, Boss Slaying, etc.)

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

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- **FromSoftware** for creating Elden Ring
- **Elden Ring Fan API** for providing Game Data
- **Django Community** for the excellent Web Framework
- **Bootstrap Team** for the responsive CSS Framework

---

*May the Grace guide your builds* 