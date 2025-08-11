# <center>Elden Ring Builds Community</center> 

## <center>A Django-based web application for the Elden Ring community to share, discover, and discuss character builds. Users can create detailed build guides, grace (like) their favorites, comment on builds, and connect with fellow Tarnished.</center>

![Image of Home Page](/readme/main%20title.PNG)

### <center>[Link to the Website](https://elden-builds-85150946427d.herokuapp.com)</center>

## Index:
1. [Features](#features)
2. [User Stories](#user-stories--)
3. [UX Design](#ux-design--)
4. [Tech Stack](#tech-stack--)
5. [Database](#datebase--)
6. [Testing](#testing-and-validation--)
7. [AI](#ai--)
8. [Acknowledgments](#acknowledgments--)

## Features -

   ### Grace System:
   The application uses "Grace" instead of traditional "likes" to match Elden Ring's lore, where Grace guides and blesses players on their journey.

   ### Smart Autocomplete:
   Powered by the Elden Ring Fan API, the build forms provide intelligent suggestions as you type weapon names, making build creation fast and accurate.

   ### Responsive Design:
   The interface adapts seamlessly from desktop to mobile, ensuring a great experience for users on any device.

## User Stories -


### Authentication & User Management:
- **As a new visitor**, I want to register for an account so that I can create and share my own builds
- **As a registered user**, I want to log in securely so that I can access my builds and community features
- **As a user**, I want to update my profile information so that other community members can learn about me

### Build Creation & Management:
- **As a Tarnished**, I want to create detailed builds with weapons, armor, talismans, and spells so that I can share my character        strategies
- **As a build creator**, I want autocomplete suggestions for equipment names so that I can quickly and accurately input my gear
- **As a user**, I want to upload screenshots of my character so that others can see how my build looks in-game
- **As a build author**, I want to categorize my builds (PvP, PvE, Boss Slaying) so that others can find builds for their playstyle
- **As a build creator**, I want to edit my published builds so that I can update them with improvements or corrections
- **As a build author**, I want to delete my builds so that I can remove outdated or unwanted content

### Build Discovery & Browsing:
- **As a player**, I want to browse all community builds so that I can discover new character strategies
- **As a user**, I want to filter builds by category so that I can find builds suited for my preferred playstyle
- **As a Tarnished**, I want to search for builds by weapon or equipment name so that I can find builds using specific gear
- **As a user**, I want to view detailed build information including stats, equipment, and strategies so that I can understand how to recreate the build
- **As a mobile user**, I want the site to work well on my phone so that I can browse builds anywhere

### Community Interaction:
- **As a community member**, I want to grace (like) builds that I find helpful so that I can show appreciation and bookmark favorites
- **As a user**, I want to comment on builds so that I can ask questions, provide feedback, or share experiences
- **As a build creator**, I want to receive notifications when someone comments on my builds so that I can engage with the community
- **As a commenter**, I want to edit or delete my comments so that I can correct mistakes or remove unwanted content
- **As a user**, I want to see my graced builds in my profile so that I can easily return to my favorites

### User Profile & Statistics:
- **As a user**, I want to view my profile page so that I can see all my builds and activity in one place
- **As a community member**, I want to view other users' profiles so that I can see their builds and community contributions
- **As a build creator**, I want to see statistics about my builds (views, graces, comments) so that I can understand which content resonates with the community
- **As a user**, I want to see my total graces received so that I can track my contribution to the community

### Content Moderation & Quality:
- **As a build creator**, I want to preview my build before publishing so that I can ensure it displays correctly
- **As a user**, I want build images to load quickly and display properly so that I have a smooth browsing experience

### Technical User Stories:
- **As a user**, I want the site to load quickly so that I can browse builds efficiently
- **As a mobile user**, I want all features to work on my device so that I'm not limited by my platform
- **As a user**, I want my data to be secure so that my account and personal information are protected
- **As a user**, I want the site to work reliably so that I can depend on it for my Elden Ring needs

### Build Creation & Management:
- **Detailed Build Forms**: Create comprehensive builds with weapons, armor, talismans, and spells
- **Auto-Complete Integration**: Smart suggestions powered by the Elden Ring Fan API
- **Image Uploads**: Upload multiple build screenshots via Cloudinary
- **Category System**: Organize builds by type (PvP, PvE, etc.)

### Community Features:
- **Grace System**: Like and bookmark favorite builds (themed as "Grace")
- **Comments & Discussions**: Engage with the community through build comments
- **User Profiles**: Personalized profiles with build collections and statistics
- **Build Discovery**: Browse, filter, and search through community builds

### Elden Ring Theming:
- **Authentic Design**: Dark theme with golden accents matching the game's aesthetic
- **Grace-Blessed Terminology**: Custom "Grace" system instead of generic likes
- **Responsive UI**: Mobile-friendly Bootstrap design with custom styling

### Agile 

![Project Board](https://github.com/users/xGodai/projects/8)

## UX Design -

### WireFrames:

[Desktop and Mobile WireFrames](/readme/wireframes/wireframes.PNG)

### Color Scheme:

The Elden Ring Builds Community uses a **dark fantasy color palette** that mirrors the atmospheric and mystical aesthetic of the game itself:

#### Primary Colors:
- **Deep Charcoal (#1a1a1a)**: Main background color that provides the dark, mysterious foundation
- **Rich Black (#0d0d0d)**: Used for navigation bars and card backgrounds to create depth
- **Golden Grace (#d4af37)**: Primary accent color representing the game's iconic Grace guidance system
- **Warm Gold (#ffd700)**: Used for highlights, active states, and important CTAs

#### Secondary Colors:
- **Muted Silver (#c0c0c0)**: Secondary text and subtle UI elements
- **Soft Gray (#6c757d)**: Body text and form labels for readability
- **Dark Gray (#343a40)**: Card borders and subtle separators

#### Accent Colors:
- **Grace Glow (#ffeb3b)**: Hover states and active Grace (like) buttons
- **Erdtree Amber (#ff8f00)**: Warning states and special notifications
- **Maiden Blue (#4a90e2)**: Links and informational elements
- **Crimson Red (#dc3545)**: Error states and delete actions

#### Usage Philosophy:
The color scheme creates a **sacred and mystical atmosphere** while maintaining excellent readability and accessibility. The golden accents against the dark background evoke the feeling of Grace sites in the game - beacons of light in a dark world, guiding players on their journey.

The palette ensures:
- **High contrast** for accessibility compliance
- **Thematic consistency** with Elden Ring's visual identity
- **Intuitive color coding** for different UI states and actions
- **Eye comfort** during extended browsing sessions

### Fonts:

The Elden Ring Builds Community employs a **typographic hierarchy** that balances readability with thematic authenticity, creating an immersive experience that echoes the game's medieval fantasy setting:

#### Primary Typography:
- **Headers (H1-H3)**: **"Cinzel"** - A classical serif font that evokes ancient inscriptions and medieval manuscripts, perfect for build titles and major headings
- **Body Text**: **"Roboto"** or **"Inter"** - Clean, modern sans-serif fonts ensuring excellent readability across all devices and screen sizes
- **Navigation**: **"Roboto Condensed"** - A condensed variant that maximizes space efficiency in navigation bars

#### Accent Typography:
- **Grace Counters & Stats**: **"Orbitron"** - A futuristic font that adds mystical tech elements, used for numeric displays and counters
- **Form Labels**: **"Source Sans Pro"** - Professional and accessible font for form elements and UI labels
- **Code Elements**: **"Fira Code"** - Monospace font with programming ligatures for any code snippets or technical content

#### Font Weight Hierarchy:
- **Extra Bold (800)**: Main page titles and hero headings
- **Bold (700)**: Section headers and build names
- **Semi-Bold (600)**: Navigation items and CTAs
- **Regular (400)**: Body text and descriptions
- **Light (300)**: Secondary information and metadata

#### Typography Philosophy:
The font selection creates a **bridge between ancient and modern** - reflecting Elden Ring's blend of medieval fantasy and otherworldly elements. The serif headers provide gravitas and thematic weight, while the clean sans-serif body text ensures accessibility and ease of reading during extended browsing sessions.

#### Implementation:
```css
/* Google Fonts Import */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Roboto:wght@300;400;500;700&family=Orbitron:wght@400;700&display=swap');

/* Font Stack Definitions */
--font-heading: 'Cinzel', 'Times New Roman', serif;
--font-body: 'Roboto', 'Segoe UI', 'Arial', sans-serif;
--font-accent: 'Orbitron', 'Courier New', monospace;
```

#### Accessibility Considerations:
- **Minimum 16px** font size for body text
- **High contrast ratios** against dark backgrounds
- **Fallback fonts** for users who can't load web fonts
- **Responsive scaling** for mobile devices
- **Clear visual hierarchy** for screen readers

## Tech Stack -

- **Backend**: Django 5.2.4 (Python)
- **Database**: PostgreSQL with SQLite for development
- **Frontend**: Bootstrap 5 with custom CSS and JavaScript
- **File Storage**: Cloudinary for image management
- **API Integration**: Elden Ring Fan API for autocomplete
- **Deployment**: Configured for Heroku with Gunicorn and WhiteNoise

### Project Structure -

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
### API Integration:
The application integrates with the [Elden Ring Fan API](https://eldenring.fanapis.com/api) for:
- Weapon autocomplete suggestions
- Armor and equipment data
- Talisman information
- Spell and incantation data

## Datebase -

![Database Diagram](/readme/database/Database.png)

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
   - Tracks number of views
   - Many-to-Many relationship with User through "liked_by"

4. **BuildImage** (Many-to-One with Build)
   - Stores multiple images per build (max 3)
   - Cloudinary integration for image storage
   - Primary image designation system

5. **Comment** (Many-to-One with Build and User)
   - User comments on builds
   - Supports threaded discussions (self-referential parent_id for replies)
   - Voting system through CommentVote

6. **CommentVote** (Many-to-One with Comment and User)
   - Upvote/downvote system for comments
   - Unique constraint: one vote per user per comment

7. **Notification** (Many-to-One with User)
   - Real-time notification system
   - Links to builds and comments
   - Read/unread status tracking

## Testing and Validation -

### Lighthouse

![Lighthouse Score](/readme/validation/lighthouse%20score.PNG)

### HTML

![HTML Validation](/readme/validation/html%20validator.PNG)

### CSS

![CSS Validation](/readme/validation/css%20validator.PNG)

### PEP8

![PEP8](/readme/validation/pep8%20python.PNG)

## AI -

The Elden Ring Builds Community incorporates **AI-powered features** to enhance user experience and streamline content creation while maintaining authentic community-driven content:

### Development & Code Generation:
- **GitHub Copilot**: Used throughout development for:
  - **Code completion** and intelligent suggestions for Django models, views, and templates
  - **Bug detection** and code optimization recommendations
  - **Documentation generation** for inline comments and docstrings
  - **Test case creation** for comprehensive application testing

### Content Enhancement:
- **AI-Assisted Documentation**: 
  - Created detailed code comments
  - Automated generation of consistent naming conventions across the codebase

### Smart Autocomplete System:
While the primary autocomplete is powered by the **Elden Ring Fan API**, AI enhances the experience through:
- **Intelligent filtering** of API responses based on user input patterns
- **Contextual suggestions** that prioritize commonly used equipment
- **Typo correction** and fuzzy matching for equipment names
- **Learning algorithms** that adapt to community preferences over time

### Code Quality & Optimization:
- **Security vulnerability detection** in Django models and views
- **Database query optimization** recommendations
- **Accessibility improvements** for better user experience

### Future AI Integrations:
Planned AI features for upcoming releases:
- **Build recommendation engine** based on user preferences and playstyle
- **Automated build categorization** using machine learning classification
- **Content moderation** for inappropriate comments and build descriptions
- **Smart image tagging** for uploaded build screenshots
- **Performance analytics** to suggest optimal build configurations

### Ethical AI Usage:
- **Transparency**: All AI-generated code is reviewed and tested by human developer
- **Community-First**: AI enhances but never replaces community-driven content
- **Privacy Protection**: User data is never shared with external AI services

### AI Tools & Technologies:
- **GitHub Copilot**: Primary development assistant
- **Django Debug Toolbar**: AI-enhanced performance analysis
- **Natural Language Processing**: For search and content categorization

### Benefits Achieved:
- **faster development** cycle with AI-assisted coding
- **Improved code quality** through automated suggestions
- **Enhanced user experience** via intelligent autocomplete
- **Reduced bugs** through AI-powered code review
- **Better documentation** with consistent AI-generated comments

## License -

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments -

- **FromSoftware** for creating Elden Ring
- **Elden Ring Fan API** for providing Game Data
- **Django Community** for the excellent Web Framework
- **Bootstrap Team** for the responsive CSS Framework

---

*May the Grace guide your builds*