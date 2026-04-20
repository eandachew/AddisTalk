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
- <p float="left"><img src="readme-images/site-images/paginated_code.png" alt="Paginator template code showing Django pagination implementation" height="200px" width="400px"/></p>

- <p float="left"><img src="readme-images/site-images/paginaged_pic.png" alt="Paginated posts screenshot showing multiple posts across pages" height="200px" width="400px"/></p>

 
### View Individual Post 
As a Generic User, I can view a single post so that I can read its full content. 
 
**Acceptance Criteria** 
-Acceptance criteria 1: Clicking a post title opens the full post. 
-Acceptance criteria 2: The post displays title, author, date, and content.  

**Status: COMPLETE**
- Implementation: DetailView with URL slug, template with full post details
- <p float="left"><img src="readme-images/site-images/post_detail.png" alt="Post detail view code showing DetailView implementation" height="200px" width="400px"/></p>
 
 - <p float="left"><img src="readme-images/site-images/viewpost.png" alt="View post screenshot showing full post content with title, author, date" height="200px" width="400px"/></p>

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
 - <p float="left"><img src="readme-images/site-images/signup.png" alt="Signup form code showing UserCreationForm implementation" height="200px" width="400px"/></p>
  - <p float="left"><img src="readme-images/site-images/signup_pic.png" alt="Signup page screenshot showing registration form" height="200px" width="400px"/></p>
 
 - if you are not a user you are not able to comment on posts. 
 - <p float="left"><img src="readme-images/site-images/login_comment.png" alt="Login required message screenshot showing comment form requires authentication" height="200px" width="400px"/></p>

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
- <p float="left"><img src="readme-images/site-images/approvalneeded.png" alt="Comment approval needed screenshot showing pending approval message" height="200px" width="400px"/></p>
- once it is approved it will be displayed 
- <p float="left"><img src="readme-images/site-images/commentapproved.png" alt="Comment approved code showing approval workflow implementation" height="200px" width="400px"/></p>
 - it will be visible in the page and says comment approved
 - <p float="left"><img src="readme-images/site-images/comment_approved.png" alt="Comment approved screenshot showing approved comment visible on post" height="200px" width="400px"/></p>

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
 
 - <p float="left"><img src="readme-images/site-images/admin.png" alt="Admin panel screenshot showing post and comment management interface" height="200px" width="400px"/></p>

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

- <p float="left"><img src="readme-images/site-images/edit_and_delete.png" alt="Edit and delete buttons screenshot showing comment management options" height="200px" width="400px"/></p>

- user are able to edit there pos 
 - <p float="left"><img src="readme-images/site-images/edit_comment_posted.png" alt="Edit comment posted screenshot showing updated comment after editing" height="200px" width="400px"/></p>
 
 - able to delete
 - <p float="left"><img src="readme-images/site-images/confirmation_delete.png" alt="Delete confirmation screenshot showing confirmation dialog before deletion" height="200px" width="400px"/></p>
 
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
- <p float="left"><img src="readme-images/site-images/contact_page.png" alt="Contact page screenshot showing contact form with name, email, message fields" height="200px" width="400px"/></p>

- contact sucess message
- <p float="left"><img src="readme-images/site-images/contact succes.png" alt="Contact success message screenshot showing confirmation after form submission" height="200px" width="400px"/></p>


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
 - <p float="left"><img src="readme-images/site-images/like_option.png" alt="Like option screenshot showing like button on post" height="200px" width="400px"/></p>

 - liked

 - <p float="left"><img src="readme-images/site-images/like_woking.png" alt="Like working screenshot showing successful like with updated count" height="200px" width="400px"/></p>

 - unlike send you notification
 - <p float="left"><img src="readme-images/site-images/unlike.png" alt="Unlike notification screenshot showing message after removing like" height="200px" width="400px"/></p>


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

- <p float="left"><img src="readme-images/site-images/about.png" alt="About page screenshot showing platform information and description" height="200px" width="400px"/></p>
--- 


## Unit Testing

- ### Django Unit Testing   

    - Each app was tested using Django unit testing.
    - Tests were written to test the URLs, Models, Forms, and the Views.
    - To run the tests in the terminal you can type the following command
    -