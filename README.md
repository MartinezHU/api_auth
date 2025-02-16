# API Authentication Service

A Django REST Framework-based authentication service that provides multiple authentication methods including OAuth2 and JWT.

## Features

- User registration and management
- Multiple authentication methods:
  - OAuth2 (password, authorization_code, refresh_token)
  - JWT (access and refresh tokens)
- Token introspection
- Application-based user registration
- Detailed API logging

## Technical Stack

- Python
- Django
- Django REST Framework
- Django OAuth Toolkit
- Simple JWT
- drf-spectacular (for OpenAPI documentation)

## API Endpoints

### Authentication

#### SignUp
- `POST /signup/`
  - Register new users
  - Requires `X-App-Name` header

#### OAuth2
- `POST /oauth/token/`
  - Obtain OAuth2 access tokens
  - Supports multiple grant types
- `POST /oauth/revoke/`
  - Revoke OAuth2 tokens
- `POST /oauth/introspect/`
  - Introspect OAuth2 tokens

#### JWT
- `POST /jwt/token/`
  - Obtain JWT access and refresh tokens
- `POST /jwt/refresh/`
  - Refresh JWT tokens

### User Management
- `GET /users/`
  - List users (authenticated)
- `GET /users/{id}/`
  - Retrieve user details
- `PUT /users/{id}/`
  - Update user information
- `DELETE /users/{id}/`
  - Delete user

## Security

- Authentication required for user management endpoints
- Scope-based permission system
- Request logging and monitoring

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt