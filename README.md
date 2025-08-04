# 📰 Star Wars API

A RESTful API built with Django Rest Framework that allows authenticated users to manage the data loaded for the Star Wars API.

## 🛠️ Local Setup Instructions

To run the API locally, make sure you have Docker and Docker Compose installed.

### 1. Clone the Repository

### 2. Use the environment variables file.
An environment variables file will be provided containing some variables that are needed for the execution of the API. This file will just need to be copy-pasted into the root of the project.

### 3. Build and Run the Containers
Inside the root folder of the project, run:
```bash
docker compose up --build
```

### 4. Access the API

- Open Swagger UI at:
[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)

- Or use Postman to test the endpoints at:
[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

## 🔐 Authentication

This API uses JWT (JSON Web Token) for authentication.

### 🔸 Get Access Token

Send a POST request to:
```bash
POST /api/user/token/
```

With the following JSON body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

You'll receive a response with access and refresh tokens:
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

### 🔸 Use the Token in Swagger

1. Click on the top-right Authorize button.
2. Enter the access token inside the text field.
3. Click Authorize.
4. User is now allowed to make API calls.

### 🔸 Use the Token in Postman

1. Go to the Auth tab of the request.
2. From the Dropdown 'Type', Select Bearer Token.
3. Enter the access token in the 'Token' field.
4. User can now make the API call.

---
## 🎯 Users & Seed Data

When loading for the 1st time, the project preloads  dummy users to help you explore the API functionality right away.


The following users are available for testing:

| Role        | Username | Password   |
|-------------|----------|------------|
| Superuser   | `admin`  | `adminpass`|
| Regular User | `user`  | `userpass` |

⚙️ **Admin Panel**
You can view, add, or edit data through the Django Admin interface at:
🔗 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---
## 📦 Available API Endpoints

All available endpoints can be found in the Swagger interface.
One important note is that after the authentication, the /sync/ API must be run, which is the one that calls the Star Wars API and populates the database.

---

## 🛡️ Testing

Tests are also included. You can run them by being in the root folder of the project and running the following command in the bash or cmd:
```bash
python manage.py test
```

