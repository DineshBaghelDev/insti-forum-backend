# insti-forum-backend
Backend for our Insti Forum

1. Dependencies - You need to install these via pip:

a. flask
b. flask-sqlalchemy
c. flask-bcrypt
d. flask-jwt-extended
(email-validator
password-validator)

2. Auth Routes (routes/auth.py) - Base Path: /auth
a. Signup (POST /auth/signup) - Send: username, email, password (JSON) - Expect: 201 (Success) or 400/ 409 (Error).

b. Login (POST /auth/login) - Send: identifier (can be email or username), password - Expect: 200 with an access_token or 401 (Fail).

c. View Profile (GET /auth/me) - Required: JWT Token in Header. - Expect: 200 with user id, username, email, and created_at.

3. Post Routes (routes/post.py) - Base Path: /

a. Create Post (POST /posts) - Required: JWT Token in Header. - Send: community_id, title, content.
Note: Backend checks if you are a member of that community first.
Expect: 201 with post_id.

b. Get Single Post (GET /posts/<int:post_id>)
Expect: 200 with full post details or 404 if it doesn't exist.

c. Get Community Feed (GET /communities/<int:community_id>/posts)
Expect: 200 with an array of post objects or 404 if the community is empty.

4. Critical Implementation Notes

a. JWT Header: For all protected routes (/auth/me and /posts), the frontend must send the token like this: Authorization: Bearer <your_token>.

b. Identifiers: The login uses the key identifier to handle both username and email logins simultaneously.

c. Date Formats: All timestamps (like created_at) are returned in ISO 8601 string format (YYYY-MM-DDTHH:MM:SS).

d. Error Response Body: All error responses return a msg or error key. Example: {"msg": "User already exists"}.

e. Member Check: For POST /posts, if the user is not a member of the community, the API returns a 403 Forbidden.

f. Data Types: community_id and post_id must be sent as Integers, not Strings.
