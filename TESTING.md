# Testing 
## Table of Contents

- [User Stories](#user-stories)
  - [View Paginated List of Posts](#view-paginated-list-of-posts)
  - [View Individual Post](#view-individual-post)
  - [User Registration](#user-registration)
  - [Comment on Posts](#comment-on-posts)
  - [Admin Post Management](#admin-post-management)
  - [Edit/Delete Own Comments](#editdelete-own-comments)
  - [Contact Form](#contact-form)
  - [Like Posts](#like-posts)
  - [About Page](#about-page)

- [Unit Testing](#unit-testing)
  - [Django Unit Testing](#django-unit-testing)

- [Test and Bugs During Development](#test-and-bugs-during-development)
  - [Cloudinary Image Field Integration](#1-cloudinary-image-field-integration)
  - [Comment Approval Workflow](#comment-approval-workflow)
  - [Performance Optimization for Like Counts](#performance-optimization-for-like-counts)

- [Defensive Programming and Security](#defensive-programming-and-security)
  - [Security](#security)
  - [Environment Variables](#environment-variables)
  - [User Authentication & Password Security](#user-authentication--password-security)

- [Manual Testing](#manual-testing)
  - [User Authentication](#user-authentication)
  - [Blog Posts](#blog-posts)
  - [Comments](#comments)
  - [Likes](#likes)
  - [Navigation]()

## User Stories 
 
### View Paginated List of Posts 
   
As a View paginated list of posts I can choose what content to read so that I can choose what content to read 
 
**Acceptance Criteria** 
- Acceptance criteria 1: Given more than one post in the database, multiple posts are displayed. 
- Acceptance criteria 2: When a user visits the homepage, a list of posts is shown. 
- Acceptance criteria 3: Posts are split across pages using pagination. 

**Status: COMPLETE**

- Implementation: Django ListView with Paginator, template rendering with Bootstrap
- <p float="left"><img src="static/images/paginated_code.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

- <p float="left"><img src="static/images/paginaged_pic.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

 
### View Individual Post 
As a Generic User, I can view a single post so that I can read its full content. 
 
**Acceptance Criteria** 
-Acceptance criteria 1: Clicking a post title opens the full post. 
-Acceptance criteria 2: The post displays title, author, date, and content.  

**Status: COMPLETE**
- Implementation: DetailView with URL slug, template with full post details
- <p float="left"><img src="static/images/post_detail.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
 
 - <p float="left"><img src="static/images/viewpost.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

### User Registration 
**User Story**   
As a generic user,   
I want to register an account,   
So that I can comment on posts. 
 
**Acceptance Criteria** 
- Sign-up form is available. 
- Valid details create a new user account. 
- User is redirected after successful registration. 

**Status: COMPLETE**

- Implementation: Django UserCreationForm, crispy-forms, success redirect
 - <p float="left"><img src="static/images/signup.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
  - <p float="left"><img src="static/images/signup_pic.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
 
 - if you are not a user you are not able to comment on posts. 
 - <p float="left"><img src="static/images/login_comment.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

### Comment on Posts 
**User Story**   
As a registered user,   
I want to comment on posts,   
So that I can participate in discussions. 
 
**Acceptance Criteria** 
- Only logged-in users can comment. 
- Comments are saved to the database. 
- Comments require admin approval before appearing. 

**Status: COMPLETE**

- Implementation: Comment model with approval flag, form validation, permissions
- <p float="left"><img src="static/images/approvalneeded.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
- once it is approved it will be displayed 
- <p float="left"><img src="static/images/commentapproved.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
 - it will be visible in the page and says comment approved
 - <p float="left"><img src="static/images/comment_approved.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

### Admin Post Management 
As an admin,   
I want to create, edit, and delete posts,   
So that I can manage site content. 
 
**Acceptance Criteria** 
- Admin can create posts via the admin panel. 
- Admin can edit and delete posts. 
- Admin can approve comments in the admin panel. 

**Status: COMPLETE**
- Implementation: Django Admin customization, inline comments, approval actions
 
 - <p float="left"><img src="static/images/admin.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

### Edit/Delete Own Comments  
As a registered user,   
I want to edit or delete my comments,   
So that I can fix mistakes. 
 
**Acceptance Criteria** 
- Users can edit/delete only their own comments. 
- Changes update immediately. 

**Status: COMPLETE**
- Implementation: User permission checks, UpdateView, DeleteView
- users are able to edit and delete there comment 

- <p float="left"><img src="static/images/edit_and_delete.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

- user are able to edit there pos 
 - <p float="left"><img src="static/images/edit_comment_posted.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
 
 - able to delete
 - <p float="left"><img src="static/images/confirmation_delete.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
 
### Contact Form   
As a user,   
I want to contact the site owner,   
So that I can report issues or provide feedback. 
 
**Acceptance Criteria** 
- Contact form is accessible. 
- Form sends messages successfully. 

 **Status: COMPLETE**
 - Implementation: Email backend, form validation, success messages
- contact page
- <p float="left"><img src="static/images/contact_page.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

- contact sucess message
- <p float="left"><img src="static/images/contact succes.png" alt="Image of hero buttons" height="200px" width="400px"/></p>


### Like Posts 
As a registered user,   
I want to like/unlike posts,   
So that I can show appreciation. 
 
**Acceptance Criteria** 
- Users can like and unlike posts. 
- Like count updates dynamically. 

 **Status: COMPLETE**
 - Implementation: AJAX likes, ManyToMany relationship, dynamic updates
 - like choice 
 - <p float="left"><img src="static/images/like_option.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

 - liked

 - <p float="left"><img src="static/images/like_woking.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

 - unlike send you notification
 - <p float="left"><img src="static/images/unlike.png" alt="Image of hero buttons" height="200px" width="400px"/></p>


### About Page   
As a visitor,   
I want to view information about the platform,   
So that I can understand what the site offers. 
 
**Acceptance Criteria** 
- Accessible from the navigation menu. 
- Contains descriptive text about the platform. 
- Uses the site’s base template. 
- Responsive and readable on all devices. 
 
 **Status: COMPLETE**
 - Implementation: Static page, extends base template, responsive design
 - it is in the nav-bar and give info 

- <p float="left"><img src="static/images/about.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
--- 


## Unit Testing

- ### Django Unit Testing   

    - Each app was tested using Django unit testing.
    - Tests were written to test the URLs, Models, Forms, and the Views.
    - To run the tests in the terminal you can type the following command
    -
        ```
            python3 manage.py test
        ```
    - To show how much of the app has been covered by the testing I used coverage.
    - To use coverage first run
    - ```
        pip install coverage
      ```
    - The run to test the whole app.
    - ```
        coverage run --source=. manage.py test
      ```
    - Or to test individual apps.
    - ```
        coverage run --source=abode manage.py test <app name>
      ```
    - Coverage generates a report to show how much of the code has been tested and how much is yet to be tested.
    - ```
        coverage report
      ```
    - You can then run coverage HTML to show the report on the screen.
    - ```
        coverage html
      ```    
    - To open the report you can run 
    - ```
            python3 -m http.server
      ```


    

## Test and Bugs During Development


### **1. Cloudinary Image Field Integration**

-   **Issue**: During development, I had issues integrating Cloudinary for image uploads in the Post model. Images uploaded through forms weren't displaying, and the admin panel showed raw Cloudinary URLs instead of images.
    
-   **Solution**: After extensive research, I found that Cloudinary requires both `cloudinary` and `cloudinary_storage` in INSTALLED_APPS.

### **Comment Approval Workflow**

-   **Issue**: The comment approval system wasn't displaying properly in the admin panel, and approved/unapproved comments weren't being filtered correctly in views.
    
-   **Solution**: Implemented a manager and view logic:
- 
### **Performance Optimization for Like Counts**

-   **Issue**: `post.likes.count()` was causing N+1 queries when displaying multiple posts.
    
-   **Solution**: Used annotations in queryset:
    
    python
    
    posts = Post.objects.filter(status=1).annotate(
        like_count=Count('likes'),
        comment_count=Count('comments')
    ).order_by('-created_on')

## Defensive Programming and Security


### **Security**

#### **Environment Variables**

-   For security reasons, I have followed Django best practices and used `os.environ` to manage sensitive information throughout the project.
    
-   All sensitive configuration including secret keys, database credentials, and API keys are stored as environment variables.
    
-   **For Development**: These variables are declared in the `.env` file which is excluded from version control via `.gitignore`.
    
-   **For Production**: These environment variables are configured in Heroku's Config Vars settings panel.
    
-   This approach ensures that sensitive information such as database passwords, Cloudinary API secrets, and Django secret keys are never exposed in public code repositories.
    

#### **User Authentication & Password Security**

-   I have implemented Django's built-in authentication system which provides robust security features out of the box.
    
-   **Password Storage**: User passwords are never stored in plain text. Django automatically hashes

    
## Manual Testing


### **User Authentication**

-   Users can register with valid credentials
    
-   Users can login/logout successfully
    
-   Password reset works (if implemented)
    
-   Protected pages block unauthorized access
    _login 
- <p float="left"><img src="static/images/login.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
 - logout 
- <p float="left"><img src="static/images/logout.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
### **Blog Posts**

-   Published posts display on blog page
    
-   Draft posts hidden from regular users
    
-   Post detail page loads with all content
    
-   Featured images display from Cloudinary
    
-   Admin can create/edit/delete posts
- <p float="left"><img src="static/images/viewpost.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

### **Comments**

-   Logged-in users can submit comments
    
-   Comments require admin approval
    
-   Approved comments display on posts
    
-   Users can edit their own comments
    
    - <p float="left"><img src="static/images/edit_and_delete.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
### **Likes**

-   Logged-in users can like/unlike posts
    
-   Like count updates correctly
    
-   Non-logged-in users cannot like posts
- <p float="left"><img src="static/images/like_woking.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

### **Navigation**

-   All navigation links work
    
-   Mobile menu works on small screens
    
-   Active page highlighted in nav
    - <p float="left"><img src="static/images/navigation.png" alt="Image of hero buttons" height="200px" width="400px"/></p>

### **Forms**

-   Contact form submits successfully
    
-   Form validation shows errors
    
-   CSRF protection works on all forms

- <p float="left"><img src="static/images/contact_page.png" alt="Image of hero buttons" height="200px" width="400px"/></p>
### **Admin Panel**

-   Admin can access /admin
    
-   Can manage posts, comments, users
    
-   Contact messages appear in admin

- <p float="left"><img src="static/images/admin.png" alt="Image of hero buttons" height="200px" width="400px"/></p>


## Validators

- #### CSS
    - I passed my CSS through the CSS code validator and it has passesd.

        - <div float="left">
            <img src="static/images/CSS CHECKER.png" alt="Image of css report" width="500px" height="380px" />
        </div>

- #### Javascript

     - My javascript was passed thorough jshint.

     - <div float="left">
        <img src="static/images/js.png" alt="Image of jshint" width="500px" height="180px" />
        </div>

- #### Python

     - My python was passed through a pep8 validating tool to validate it and it all passed.

     - <div float="left">
        <img src="static/images/python.png" alt="Image of pep8 results" width="500px" height="280px" />
        </div>

- #### Html

     - My Html code was passed through the W3C Markup Validation Service and there are no errors showing.

     - <div float="left">
        <img src="static/images/HTML CHECKER.png" alt="Image of pep8 results" width="500px" height="280px" />
        </div>

## Responsiveness and Browsers

- I have tested the site Responsivenessacross Google chrome dev tools. 
- I have also used the application across different screen sizes.
- The app has also been used on different browsers to check its compatibility
    - Google chrome.
    - Safari
    - Opera
    - Microsoft edge
    - Firefox.
