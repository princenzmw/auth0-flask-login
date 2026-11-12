# Auth0 Login Flow Demo (Flask)

A minimal Flask web application implementing a complete Auth0 OpenID Connect
login flow: hosted Universal Login, callback handling, session management,
and full OIDC single logout. Built for MLH Global Hack Week: Builders Week.

## What it demonstrates

- Redirect-based OIDC login (`/login` -> Auth0 Universal Login -> `/callback`)
- Session-backed user state with claims (sub, email, email_verified, iss)
- Protected route (`/dashboard`) with unauthenticated redirect
- Standard-compliant logout via Auth0's `/v2/logout` endpoint

## Setup

### 1. Auth0 dashboard

1. Sign in at <https://manage.auth0.com> (free plan is fine).
2. **Applications -> Create Application** -> name it (e.g. `mlh-ghw-flask`), type **Regular Web Application**.
3. In the app's **Settings** tab, set:
   - **Allowed Callback URLs**: `http://localhost:3000/callback`
   - **Allowed Logout URLs**: `http://localhost:3000`
4. Copy **Domain**, **Client ID**, and **Client Secret**.

### 2. Environment

```bash
cp .env.example .env
# paste your Domain / Client ID / Client Secret into .env
```

### 3. Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://localhost:3000>, click **Log in with Auth0**, sign in, and you
will be returned to the dashboard with your verified profile claims.

## Tech stack

Flask, Authlib (OIDC client), python-dotenv.
