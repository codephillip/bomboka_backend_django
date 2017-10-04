"""
PLEASE UPDATE CURL TESTS

########## NOTE ###########
first access the token before accessing any endpoint
http://localhost:8000/api-token-auth
or
http://localhost:8000/auth/login/
###########################


# GENERATE TOKEN
# pass the username and password. returns a token
curl -X POST -d "username=codephillip&password=password123" http://localhost:8000/api-token-auth
# token example
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNmZSIsInVzZXJfaWQiOjEsImVtYWlsIjoiIiwiZXhwIjoxNDYxOTY1ODI5fQ.OTX7CZFZqxhaUnU9Da13Ebh9FY_bHMeCF1ypr9hXjWw


# USER LOGIN(user can login with either phone number, email, or username
# login with phone number
curl -X POST
-d 'phone=254759994444&password=nopassword@#()'
http://127.0.0.1:8000/api/v1/users/login

# login with email
curl -X POST
-d 'email=codephillip@gmail.com&password=nop@s&&ord'
http://127.0.0.1:8000/api/v1/users/login

# login with username
curl -X POST
-d 'username=codephillip&password=nopas@(*sword'
http://127.0.0.1:8000/api/v1/users/login


# REFRESH TOKEN
curl -X POST -H "Content-Type: application/json"
-d '{"token":"<EXISTING_TOKEN>"}'
http://localhost:8000/api-token-refresh

# VERIFY TOKEN
curl -X POST -H "Content-Type: application/json"
-d '{"token":"<EXISTING_TOKEN>"}'
http://localhost:8000/api-token-verify



# REQUESTS #
# use header "Authorization: JWT <token>" in curl or client

# POST example where user creating account
curl -X POST -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNmZSIsInVzZXJfaWQiOjEsImVtYWlsIjoiIiwiZXhwIjoxNDYxOTY2MTc4fQ._i5wEqJ_OO8wNiVVNAWNPGjGaO7OzChY0UzONgw06D0"
 -H "Content-Type: application/json"
 -d 'first_name=Krukov7&phone=254759994444&password=123paKrukov&last_name=Krukov7&email=Krukov7@example.com&dob=1989-08-13&email2=Krukov7@example.com'
 'http://127.0.0.1:8000/api/v1/users/register'

# GET example which lists all products
curl -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNmZSIsInVzZXJfaWQiOjEsImVtYWlsIjoiIiwiZXhwIjoxNDYxOTY1ODI5fQ.OTX7CZFZqxhaUnU9Da13Ebh9FY_bHMeCF1ypr9hXjWw"
http://127.0.0.1:8000/api/v1/products

# GET example which lists all users
curl -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNmZSIsInVzZXJfaWQiOjEsImVtYWlsIjoiIiwiZXhwIjoxNDYxOTY1ODI5fQ.OTX7CZFZqxhaUnU9Da13Ebh9FY_bHMeCF1ypr9hXjWw"
http://127.0.0.1:8000/api/v1/users

####################
CURL BUGS
you may need to use quotes around urls
'http://127.0.0.1:8000/api/v1/users/login'
####################

####################
PASSWORD RESET USING EMAIL LINK
User is redirected to this page when they click the reset password in their email
the <uid> and <token> is picked from
http://127.0.0.1:8000/password/insert_new_password/{uid}/{token}
and sent to
http://127.0.0.1:8000/password/reset/confirm
with post data
data = {
  "new_password": "string",
  "token": "string",
  "uid": "string"
}

###################

###################
ACCESSING IMAGES
Use this base url
http://127.0.0.1:8000/photos/
plus products/123.png, vendors/234.png, users/456.png
###################

# END



Random tokens for debugging only. Most will be expired.
however, tokens can be refresh if less than 7 days old
# Note refresh the token to prevent user inserting credentials(auto sign_in)
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNDhlOGZlNWQtM2NlYi00N2U3LThjYjItOGZjOWYzNjE4OGZmIiwiZXhwIjoxNTAzMzg0NDMwLCJlbWFpbCI6ImNvZGVwaGlsbGlwQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiY29kZXBoaWxsaXAifQ.3gub3cEmftftX7G3F6206r-pHxUu1FJEpF7lI9ERekg

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmlnX2lhdCI6MTUwMzM4NTM3MCwiZW1haWwiOiJjb2RlcGhpbGxpcEBnbWFpbC5jb20iLCJleHAiOjE1MDMzODg5NzAsInVzZXJuYW1lIjoiY29kZXBoaWxsaXAiLCJ1c2VyX2lkIjoiNDhlOGZlNWQtM2NlYi00N2U3LThjYjItOGZjOWYzNjE4OGZmIn0.g48vmXNKNrZkif0mvA_Vchmp-q1HS9YmYg0QMlHFVcM

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmlnX2lhdCI6MTUwMzM4NTM5MSwiZW1haWwiOiJjb2RlcGhpbGxpcEBnbWFpbC5jb20iLCJleHAiOjE1MDMzODg5OTEsInVzZXJuYW1lIjoiY29kZXBoaWxsaXAiLCJ1c2VyX2lkIjoiNDhlOGZlNWQtM2NlYi00N2U3LThjYjItOGZjOWYzNjE4OGZmIn0.m4bG0zd3nEVxjmn4Td1mar9KI7Csw3xH66w0nLwmsgk
"""