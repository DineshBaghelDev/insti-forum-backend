# insti-forum-backend
Backend for our Insti Forum

## Dependencies - You need to install these via pip:

a. flask  
b. flask-sqlalchemy  
c. flask-bcrypt  
d. flask-jwt-extended  
(email-validator  
password-validator)

## Database setup
Requirements: Install SQLite DB Browser for viewing the database.  
When **backend/run.py** is executed, the **insti_forum.db** file is created in backend/instance.  
The database and tables are created automatically once the backend server is run for the first time.  
To reset the database, stop the backend server, delete the insti_forum.db file and restart the backend again, to delete all old data.

**For JWT_SECRET_KEY**,

Add the user environment variable **JWT_SECRET_KEY = dev-secret-key**.


## 1. Auth Routes (routes/auth.py) - Base Path: /auth

**a. Signup (POST /auth/signup)**
  
Send: 
  - username
  - email
  - password
  
Expect:
201 (Success) or 400/409 (Error).

**b. Login (POST /auth/login)** 

Send:
  - identifier (can be username or email)
  - password
      
Expect: 200 with an access_token or 401/400 (Fail).

**c. View Profile (GET /auth/me)**  

Required: JWT Token in Header.   
Expect: 200 with 
  - user id
  - username
  - email
  - created_at 

## 2. Community Routes (routes/community.py)

**a. Create Community (POST /communities)**  

Required: JWT Token in Header.  
Send: 
  - name
  - description (optional)
    
Expect: 201 with community_id
    
**b. View all communities (GET /communities)**

Expect: 200 with a list of all communities containing the following info of each community
  - id
  - name
  - description
  - creator_id
  - created_at

**c. View a single community (GET /communities/`<int:community_id>`)**  

Expect: 200 with all details of the community (same as before).

**d. Join a community (POST /communities/`<int:community_id>`/join)**  

Required: JWT Token in Header.  
Expect: 201 with membership_id.

**d. Leave a community (POST /communities/`<int:community_id>`/join)**  

Required: JWT Token in Header.  
Expect: 204

**e. Delete a community (DELETE /communities/`<int:community_id>`/delete)**  

Required: Only creator can delete a community.  
Expect: 200

## 3. Post Routes (routes/post.py) - Base Path: /

**a. Create Post (POST communitites/`<int:community_id>`/posts)**  

Required: JWT Token in Header.   
Send: 
  - title
  - content (optional)
    
Note: Backend checks if you are a member of that community first.  
Expect: 201 with post_id.

**b. Get Single Post (GET /posts/`<int:post_id>`)**  

Expect: 200 with 
  - id
  - user_id
  - community_id
  - title
  - content
  - created_at
      
    in JSON or 404 if it doesn't exist.

**c. Get Community Feed (GET /communities/`<int:community_id>`/posts)**    

Expect: 200 with an array of post objects (same as before) or 404 if the community is empty.

**d. Delete a post (DELETE /posts/`<int:post_id>`/delete)**  

Required: Only post creator can delete it.  
Expect: 200

## 4. Comment Routes (routes/comment.py)

**a. Create comment (POST /posts/`<int:post_id>`/comments)**  

Required: JWT Token in Header.  
Send: 
 - content
     
Expect: 201 with comment_id.

**b. View comments (POST /posts/`<int:post_id>`/comments)**  

Expect: 200 with list of all comments and their details
  - id
  - post_id
  - content
  - author_id
  - created_at

**c. Delete a comment (DELETE /comments/`<int:comment_id>`/delete)**  

Required: Only comment author can delete a comment.  
Expect: 200

## Critical Implementation Notes

a. JWT Header: For all protected routes (/auth/me and /posts), the frontend must send the token like this: Authorization: Bearer <your_token>.

b. Identifiers: The login uses the key identifier to handle both username and email logins simultaneously.

c. Date Formats: All timestamps (like created_at) are returned in ISO 8601 string format (YYYY-MM-DDTHH:MM:SS).

d. Error Response Body: All error responses return a msg or error key. Example: {"msg": "User already exists"}.

e. Member Check: For POST /posts, if the user is not a member of the community, the API returns a 403 Forbidden.

f. Data Types: community_id and post_id must be sent as Integers, not Strings.

g. All requests and responses are in JSON format
