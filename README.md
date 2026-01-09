# AddisTalk2 
 
# Table of Contents 
1. [Project Goals](#project-goals)   
2. [User Stories](#user-stories)   
   - [View Paginated List of Posts](#view-paginated-list-of-posts)    
   - [View Individual Post](#view-individual-post)   
   - [User Registration](#user-registration)   
   - [Comment on Posts](#comment-on-posts)   
   - [Admin Post Management](#admin-post-management)   
   - [Edit/Delete Own Comments](#editdelete-own-comments)   
   - [Contact Form](#contact-form)   
   - [Like Posts](#like-posts)   
   - [About Page](#about-page)   
3. [Project Requirements Fulfilled](#project-requirements-fulfilled)   
4. [Functionality of Project](#functionality-of-project)   
   - [Core Features](#core-features)   
   - [User Roles](#user-roles)   
5. [User Experience](#user-experience)   
   - [Visitor Journey](#visitor-journey)   
   - [UX Principles](#ux-principles)   
6. [Design](#design)   
   - [Font](#font)   
   - [Color Scheme](#color-scheme)   
   - [Layout](#layout)   
7. [Technology Used](#technology-used)   
   - [Backend](#backend)   
   - [Frontend](#frontend)   
   - [Development Tools](#development-tools)   
8. [Features](#features)   
   - [Current Features](#current-features)   
   - [Admin Features](#admin-features)   
9. [Future Features](#future-features)   
10. [Testing](#testing)   
11. [Security Measures](#security-measures)   
12. [Deployment](#deployment)   
13. [Credits](#credits)   
14. [Conclusion](#conclusion) 
 

## Project Goals 
This project aims to build a full-featured, interactive blogging platform using Django, PostgreSQL, and modern front-end technologies (HTML, CSS, JavaScript, Bootstrap 5). AddisTalk is a Reddit-style discussion forum that allows users to share Ethiopian perspectives and engage in meaningful conversations. The platform is designed to be responsive, secure, and fully functional, following best practices and good UX principles. 
 
--- 
## Live Project  
- [View the live project here.](https://addistalk-22f34f7eacaf.herokuapp.com/) 
## Screenshot  
### Home page screenshot. 
 

### Signup page screenshot. 
 
## User Stories 
 
### View Paginated List of Posts 
   
As a View paginated list of posts I can choose what content to read so that I can choose what content to read 
 
**Acceptance Criteria** 
- Acceptance criteria 1: Given more than one post in the database, multiple posts are displayed. 
- Acceptance criteria 2: When a user visits the homepage, a list of posts is shown. 
- Acceptance criteria 3: Posts are split across pages using pagination. 
 
### View Individual Post 
As a Generic User, I can view a single post so that I can read its full content. 
 
**Acceptance Criteria** 
-Acceptance criteria 1: Clicking a post title opens the full post. 
-Acceptance criteria 2: The post displays title, author, date, and content.  
 
### User Registration 
**User Story**   
As a generic user,   
I want to register an account,   
So that I can comment on posts. 
 
**Acceptance Criteria** 
- Sign-up form is available. 
- Valid details create a new user account. 
- User is redirected after successful registration. 
 
### Comment on Posts 
**User Story**   
As a registered user,   
I want to comment on posts,   
So that I can participate in discussions. 
 
**Acceptance Criteria** 
- Only logged-in users can comment. 
- Comments are saved to the database. 
- Comments require admin approval before appearing. 
 
### Admin Post Management 
As an admin,   
I want to create, edit, and delete posts,   
So that I can manage site content. 
 
**Acceptance Criteria** 
- Admin can create posts via the admin panel. 
- Admin can edit and delete posts. 
- Admin can approve comments in the admin panel. 
 
### Edit/Delete Own Comments  
As a registered user,   
I want to edit or delete my comments,   
So that I can fix mistakes. 
 
**Acceptance Criteria** 
- Users can edit/delete only their own comments. 
- Changes update immediately. 
 
### Contact Form   
As a user,   
I want to contact the site owner,   
So that I can report issues or provide feedback. 
 
**Acceptance Criteria** 
- Contact form is accessible. 
- Form sends messages successfully. 
 
### Like Posts 
As a registered user,   
I want to like/unlike posts,   
So that I can show appreciation. 
 
**Acceptance Criteria** 
- Users can like and unlike posts. 
- Like count updates dynamically. 
 
### About Page   
As a visitor,   
I want to view information about the platform,   
So that I can understand what the site offers. 
 
**Acceptance Criteria** 
- Accessible from the navigation menu. 
- Contains descriptive text about the platform. 
- Uses the site’s base template. 
- Responsive and readable on all devices. 
 
--- 
 
## Project Requirements Fulfilled 
- **Database Structure**: PostgreSQL with Post and Comment models   
- **CRUD Functionality**: Users can create, read, update, delete posts/comments   
- **Frontend Technologies**: HTML, CSS, Bootstrap 5, JavaScript   
- **User Authentication**: Django-allauth for signup/login   
- **Admin Management**: Django admin panel for content moderation   
- **Responsive Design**: Mobile-first implementation   
- **Deployment Ready**: Heroku configuration   
- **Version Control**: GitHub   
 
--- 
 
## Functionality of Project 
 
### Core Features 
1. User Registration & Authentication   
2. Blog Posts (CRUD with rich text)   
3. Comment System (with admin approval)   
4. Like System (AJAX-based)   
5. Contact Form   
6. About Page   
7. Responsive Design 
 
### User Roles 
- Anonymous Users: Browse posts, view comments   
- Registered Users: Comment, like, edit/delete own comments   
- Administrators: Manage posts, approve comments, manage users   
 
--- 
 
## User Experience 
 
### Visitor Journey 
1. Landing Page → Paginated post list   
2. Post Detail → Full post and comments   
3. Registration → Sign up to participate   
4. Authentication → Login to engage   
5. Interaction → Comment, like, edit, delete   
 
### UX Principles 
- Simplicity   
- Accessibility   
- Immediate Feedback   
- Consistency   
 
--- 
 
## Design 
 
### Font 
- Primary: Bootstrap default   
- Fallback: Segoe UI, Tahoma, Geneva, Verdana, sans-serif   
- Icons: Bootstrap Icons   
 
### Color Scheme 
- Primary: `#0d6efd`   
- Secondary: `#6c757d`   
- Success: `#198754`   
- Danger: `#dc3545`   
- Background: `#f8f9fa`   
- Text: `#212529` / `#6c757d`   
 
### Layout 
- Containers: Bootstrap `container-fluid`   
- Cards: Rounded corners, subtle shadows   
- Navigation: Fixed top navbar   
- Responsive wireframes: Mobile → tablet → desktop   
 
--- 
 
## Technology Used 
 
### Backend 
- Django 4.2.27   
- PostgreSQL   
- Django-allauth   
- Django-crispy-forms   
- Django-summernote   
- Gunicorn & Whitenoise   
 
### Frontend 
- Bootstrap 5.3.2   
- Bootstrap Icons   
- Vanilla JS with AJAX   
- Django Templates   
 
### Development Tools 
- Git & GitHub   
- Python virtual environment   
- Heroku deployment   
- Neon.tech PostgreSQL   
 
--- 
 
## Features 
 
### Current Features 
- User authentication & registration   
- Create, read, update, delete posts   
- Comment system with admin approval   
- Like/unlike posts (AJAX)   
- Contact form   
- About page   
- Responsive design   
 
### Admin Features 
- Full post management   
- Comment moderation   
- User management   
 
--- 
 
## Future Features 
- User profiles, avatars, bio   
- Post categories and tags   
- Search functionality   
- Notifications and social sharing   
- Dark mode   
- Email integration and advanced moderation   
- Analytics & REST API   
- Multilingual support   
 
--- 
 
## Testing 
- Manual testing: authentication, CRUD, comments, likes, forms, responsive design, browsers   
- Planned automated tests: unit, integration, Selenium, performance   
 
--- 
 
## Security Measures 
- Secure authentication & session handling   
- User permissions & ownership verification   
- Input validation & XSS/SQL prevention   
- CSRF protection   
- Environment variables for secrets   
 
--- 
 
## Deployment 
 
### Deployment Process 
This Django application was developed on Windows using VS Code, with Git for version control and GitHub for remote repository hosting. Multiple branches were used for organized feature development and testing. 
 
### Deployment Procedure 
 
1. **Development Environment Setup** 
   - Windows 11 with Python virtual environment in VS Code 
   - Environment variables managed via `.env` or configuration file 
   - Regular Git commits following semantic conventions 
 
2. **GitHub Repository** 
   - Remote repository created and connected to local project 
   - Code synchronized using: 
     ```bash 
     git add . 
     git commit -m "Feature implementation: User authentication" 
     git push origin main 
     ``` 
 
3. **Heroku Deployment** 
   - Created `Procfile` in project root: 
     ``` 
     web: gunicorn AddisTalk2.wsgi 
     ``` 
   - Specified Python version in `runtime.txt` 
   - Configured Heroku app and buildpacks (Python/Node.js) 
   - Set environment variables (SECRET_KEY, DATABASE_URL, etc.) 
   - Configured PostgreSQL database and ran migrations 
   - Managed static files with WhiteNoise and Cloudinary 
 
4. **Deployment Execution** 
   - Enabled automatic deployment from GitHub main branch 
   - Monitored logs using Heroku CLI 
   - Application live at: [https://addistalk2-555124552836.herokuapp.com/] 
 
5. **Windows-Specific Notes** 
   - Handle file paths and line endings correctly 
   - Activate virtual environment: 
     ```powershell 
     venv\Scripts\activate 
     ``` 
   - Install dependencies: 
     ```powershell 
     pip install -r requirements.txt 
     ``` 
   - Run migrations and create superuser: 
     ```powershell 
     python manage.py migrate 
     python manage.py createsuperuser 
     python manage.py runserver 
     ``` 
 
6. **Deployment Verification** 
   - Test endpoints, database connectivity, static/media files, authentication, and responsive design 
   - Continuous deployment ensures automatic updates on main branch pushes and rollback capability via Heroku 
 
  
 
--- 
 
## Credits 
- Django, Bootstrap, Django-allauth, Summernote   
- Code Institute tutorials   
- Open-source community   
 
--- 
 
## Conclusion 
AddisTalk is a fully functional Django blog platform that fulfills all core requirements. It is scalable, responsive, secure, and ready for production deployment, providing a strong foundation for a community-focused discussion forum. 