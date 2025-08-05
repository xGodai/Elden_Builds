# Elden Ring Builds Community ⚡

A Django-based web application for the Elden Ring community to share, discover, and discuss character builds. Users can create detailed build guides, grace (like) their favorites, comment on builds, and connect with fellow Tarnished.

## ✨ Features

### 🏗️ Build Creation & Management
- **Detailed Build Forms**: Create comprehensive builds with weapons, armor, talismans, and spells
- **Auto-Complete Integration**: Smart suggestions powered by the Elden Ring Fan API
- **Image Uploads**: Upload multiple build screenshots via Cloudinary
- **Category System**: Organize builds by type (PvP, PvE, Boss Slaying, etc.)

### 🤝 Community Features
- **Grace System**: Like and bookmark favorite builds (themed as "Grace")
- **Comments & Discussions**: Engage with the community through build comments
- **User Profiles**: Personalized profiles with build collections and statistics
- **Build Discovery**: Browse, filter, and search through community builds

### 🎨 Elden Ring Theming
- **Authentic Design**: Dark theme with golden accents matching the game's aesthetic
- **Grace-Blessed Terminology**: Custom "Grace" system instead of generic likes
- **Responsive UI**: Mobile-friendly Bootstrap design with custom styling

## 🛠️ Tech Stack

- **Backend**: Django 5.2.4 (Python)
- **Database**: PostgreSQL with SQLite for development
- **Frontend**: Bootstrap 5 with custom CSS and JavaScript
- **File Storage**: Cloudinary for image management
- **API Integration**: Elden Ring Fan API for autocomplete
- **Deployment**: Configured for Heroku with Gunicorn and WhiteNoise

## 📁 Project Structure

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

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL (for production)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/xGodai/Elden_Builds.git
   cd Elden_Builds
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   CLOUDINARY_URL=cloudinary://your-cloudinary-credentials
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://localhost:8000` to view the application.

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key for security
- `DEBUG`: Set to `False` in production
- `DATABASE_URL`: PostgreSQL connection string for production
- `CLOUDINARY_URL`: Cloudinary credentials for image storage

### API Integration
The application integrates with the [Elden Ring Fan API](https://eldenring.fanapis.com/api) for:
- Weapon autocomplete suggestions
- Armor and equipment data
- Talisman information
- Spell and incantation data

## 📱 Usage

### Creating a Build
1. Register an account or log in
2. Click "Create New Build" from the navigation
3. Fill out the build form with:
   - Title and description
   - Weapon loadout (with autocomplete)
   - Armor sets
   - Talismans and equipment
   - Spells and incantations
4. Upload screenshots of your build
5. Select appropriate category tags

### Community Interaction
- **Grace Builds**: Click the ⚡ button to grace builds you enjoy
- **Comment**: Share strategies and feedback on builds
- **Follow Users**: Track your favorite build creators
- **Browse & Filter**: Discover builds by category, popularity, or recent updates

## 🎯 Key Features Deep Dive

### Grace System
The application uses "Grace" instead of traditional "likes" to match Elden Ring's lore, where Grace guides and blesses players on their journey.

### Smart Autocomplete
Powered by the Elden Ring Fan API, the build forms provide intelligent suggestions as you type weapon names, making build creation fast and accurate.

### Responsive Design
The interface adapts seamlessly from desktop to mobile, ensuring a great experience for users on any device.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **FromSoftware** for creating Elden Ring
- **Elden Ring Fan API** for providing Game Data
- **Django Community** for the excellent Web Framework
- **Bootstrap Team** for the responsive CSS Framework

## 📞 Support

For support, please open an issue on GitHub.

---

*May the Grace guide your builds* ⚡