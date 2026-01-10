# AddisTalk2 
## Table of Contents

- [Project Goals](#project-goals)
- [Live Project](#live-project)
- [Screenshot](#screenshot)
- [User Stories](#user-stories)
- [Database Models and Schema](#database-models-and-schema)
- [Design](#design)
- [Features](#features)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)
- [Conclusion](#conclusion)

 

## Project Goals 
This project aims to build a full-featured, interactive blogging platform using Django, PostgreSQL, and modern front-end technologies (HTML, CSS, JavaScript, Bootstrap 5). AddisTalk is a Reddit-style discussion forum that allows users to share Ethiopian perspectives and engage in meaningful conversations. The platform is designed to be responsive, secure, and fully functional, following best practices and good UX principles. 
 
--- 
## Live Project  
- [View the live project here.](https://addistalk-22f34f7eacaf.herokuapp.com/) 

## Screenshot  
### Home page screenshot. 

 <div align="center">
    <img src="static/images/home_screen.png" alt="image of the homepage hero section">
</div>

 
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
 
## Database models and schema

### Models


-   **User**
    
    -   From Django's built-in `django.contrib.auth.models.User`
        
    -   Contains: `username`, `email`, `password`, `is_active`, `is_staff`, `date_joined`
        
    -   **Role in blog**: Post author, commenter, and liker
        
    -   **Relationships**:
        
        -   Can create multiple blog posts (1:N)
            
        -   Can write multiple comments (1:N)
            
        -   Can like multiple posts (M:N via join table)
            
 **Blog**

-   **Post**
    
    -   Core content model for blog articles
        
    -   **Fields**: `title`, `slug`, `author`, `content`, `created_on`, `status`, `featured_image`
        
    -   **Special features**:
        
        -   `status`: Draft (0) or Published (1) for content workflow
            
        -   `slug`: URL-friendly version of title for clean URLs
            
        -   `featured_image`: Cloudinary integration for image hosting
            
    -   **Relationships**:
        
        -   Belongs to one User (author)
            
        -   Has many Comments (1:N)
            
        -   Liked by many Users (M:N)
            
-   **Comment**
    
    -   User-generated responses to posts
        
    -   **Fields**: `post`, `author`, `body`, `approved`, `created_on`
        
    -   **Moderation**: `approved` flag for comment moderation system
        
    -   **Relationships**:
        
        -   Belongs to one Post
            
        -   Belongs to one User (author)
            
-   **Like System**
    
    -   Many-to-Many relationship between Users and Posts
        
    -   **Implementation**: Automatic join table `blog_post_likes`
        
    -   **Functionality**:
        
        -   Users can like/unlike posts
            
        -   Unique constraint prevents duplicate likes
            
        -   `post.number_of_likes()` method returns count
            
    -   **Join table fields**: `id`, `post_id`, `user_id`
        

-   **About**
    
    -   Static content model for "About Us" page
        
    -   **Fields**: `title`, `updated_on`, `content`
        
    -   **Characteristics**:
        
        -   Typically single instance (but can have multiple)
            
        -   `updated_on` auto-updates on save
            
        -   No relationships with other models
            
 **Contact**

-   **ContactMessage**
    
    -   Stores visitor contact form submissions
        
    -   **Fields**: `name`, `email`, `subject`, `message`, `created_on`, `is_read`, `resolved`
        
    -   **Workflow tracking**:
        
        -   `is_read`: Marks messages as read/unread
            
        -   `resolved`: Tracks issue resolution status
            
        -   `created_on`: Auto-timestamp for sorting

- Database Diagram

  - The database diagram shows a list of items in each object and relationships between each object.    

   <div align="center"><img src="static/images/database_diagram.png" alt="image of the database diagram"></div>
## Design



### **🎨 Colour Scheme**

#### **Primary Colours:**

-   **Navy Gradient**: `#343a40` → `#495057` (Navigation, headers)
    
-   **Primary Blue**: `#0d6efd` → `#0b5ed7` (Buttons, links)
    
-   **Accent Yellow**: `#ffc107` (Highlights, active states)
    
-   **Danger Red**: `#dc3545` (Delete actions, warnings)
    

#### **Background & Text:**

-   **Light Grey**: `#f8f9fa` (Page background)
    
-   **Text Dark**: `#212529` (Main text)
    
-   **Text Muted**: `#6c757d` (Meta info, timestamps)
    

#### **Cultural Inspiration:**

-   Ethiopian flag yellow (`#ffc107`) for cultural accent
    
-   Clean, professional gradients for modern look
    

### **🔤 Typography**

#### **Font Stack:**

text

-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif

-   **Why**: Fast loading, system-native, excellent readability
    
-   **Fallback**: `sans-serif`
    

#### **Font Usage:**

-   **Headings**: Bold (700-800 weight) for hierarchy
    
-   **Body Text**: Regular (400 weight) for comfortable reading
    
-   **Buttons/Meta**: Medium/Semi-bold (500-600 weight)
    
-   **Size Scaling**: Responsive across devices
    

### **🖼️ Images & Icons**

#### **Images:**

-   **Hero Image**: `header.png` - Ethiopian cultural theme
    
-   **Treatment**: Rounded corners (`border-radius: 8px`)
    
-   **Style**: Professional quality, optimized for web
    
-   **Responsive**: Scales with `object-fit: cover`
    

#### **Icons (Bootstrap Icons):**

-   **Navigation**: `bi-house-door`, `bi-info-circle`, `bi-envelope`
    
-   **User Actions**: `bi-person-circle`, `bi-gear`, `bi-heart`
    
-   **Status**: `bi-check-circle`, `bi-clock`, `bi-calendar`
    
-   **Purpose**: Visual cues, accessibility support
    

**Design Philosophy**: Clean, modern, culturally-aware platform for meaningful discussion.


## Features


### **Homepage Blog Section**

-   **Latest Posts Display**: Shows recent blog posts with titles, excerpts, and author information
    
-   **Read Full Posts**: Users can click "Read More" to access complete post content
    
-   **Post Metadata**: Each post shows author, publication date, and number of comments
    
-   **Visual Cards**: Posts are displayed in responsive cards with hover effects
    
-   **Staff Access**: Admin users see direct links to create new posts
    

### **Post Detail Features**

-   **Complete Content**: Full post display with proper formatting
    
-   **Like System**: Authenticated users can like/unlike posts (AJAX-powered)
    
-   **Comment Section**: Users can read and submit comments (requires approval)
    
### **Comment Features**

-   **Authenticated Commenting**: Only registered users can comment
    
-   **Admin Approval**: Comments require admin approval before public display
    
-   **Edit & Delete**: Users can edit or delete their own comments
    
-   **Comment Moderation**: Admin dashboard for comment management
    
-   **Real-time Updates**: AJAX-powered comment submission (optional)
    

### **Comment Display**

-   **Approved Comments**: Only admin-approved comments are publicly visible
    
-   **User Badges**: Visual indicators for comment authors
    
-   **Timestamps**: Clear display of when comments were posted
    
### **Interactive Features**

-   **AJAX-powered**: Like/unlike without page refresh
    
-   **Visual Feedback**: Heart icon animation on like action
    
-   **Like Count**: Real-time update of total likes
    
-   **Authentication Required**: Only logged-in users can like posts
    
-   **User Tracking**: System remembers which posts each user has liked
    

### **Footer Display**

-   **Real-time Clocks**: Shows current time in Ireland and Ethiopia
    
-   **API Integration**: Fetches accurate times from [worldtimeapi.org](https://worldtimeapi.org/)
    
-   **Time Difference**: Calculates and displays time zone difference
    
-   **Fallback System**: Uses calculated times if API fails
    
-   **Cultural Connection**: Highlights the Ireland-Ethiopia bridge
    

### **Contact Page**

-   **Contact Form**: Users can send messages through a secure form
    
-   **Form Validation**: Client-side and server-side validation
    
-   **Success Feedback**: Confirmation message after successful submission
    
-   **Admin Notification**: Messages are logged for admin review
        

### **Message System**

-   **Database Storage**: All messages are saved in the database
    
-   **Admin Access**: Site administrators can view all messages
        

### **Authentication System**

-   **Registration**: New users can create accounts
    
-   **Login/Logout**: Secure session management
    
-   **Password Management**: Reset/change password functionality
    
-   **Email Settings**: Users can manage email preferences
    
-   **Profile Management**: Basic account information display
    

### **User Interaction**

-   **Comment History**: Users can view their comment history
    
-   **Liked Posts**: Track which posts users have liked
    
-   **Account Settings**: Update email and password
    
-   **Admin Privileges**: Staff users have additional content management options
    
### **Content Management**

-   **Post Creation**: Add new blog posts through admin interface
    
-   **Post Editing**: Modify existing posts
    
-   **Comment Moderation**: Approve/reject user comments
    
-   **User Management**: Admin control over user accounts
    
-   **Analytics**: Basic statistics on posts and engagement
    

### **Moderation Tools**

-   **Comment Approval Queue**: Review pending comments
    
-   **Post Status Control**: Publish/draft post management
    
-   **User Management**: Monitor and manage user accounts
    
-   **Content Removal**: Delete inappropriate posts or comments

- #### Testing.
  - The testing section for this site is located at the following link.
    - [Testing file](TESTING.md)
 
--- 
 
## Deployment 
 
### Deployment Process 
This Django application was developed on Windows using VS Code, with Git for version control and GitHub for remote repository hosting. Multiple branches were used for organized feature development and testing. 
 
### Deployment Procedure 
 
1. **Development Environment Setup** 
   -  with Python virtual environment in VS Code 
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
   - Application live at: [https://addistalk-22f34f7eacaf.herokuapp.com] 
 
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