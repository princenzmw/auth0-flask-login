import os
from urllib.parse import urlencode

from flask import Flask, redirect, render_template, session, url_for
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Copy .env.example to .env and fill in your Auth0 credentials."
        )
    return value


AUTH0_DOMAIN = _require_env("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = _require_env("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = _require_env("AUTH0_CLIENT_SECRET")

app = Flask(__name__)
app.config.update(
    SECRET_KEY=_require_env("SECRET_KEY"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

oauth = OAuth(app)
auth0 = oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)


@app.route("/")
def home():
    return render_template("home.html", user=session.get("user"))


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback")
def callback():
    try:
        token = oauth.auth0.authorize_access_token()
    except Exception:
        app.logger.exception("Auth0 authorization callback failed")
        return redirect(url_for("home"))
    session["user"] = token.get("userinfo")
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    params = {
        "returnTo": url_for("home", _external=True),
        "client_id": AUTH0_CLIENT_ID,
    }
    return redirect(f"https://{AUTH0_DOMAIN}/v2/logout?{urlencode(params)}")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 3000)),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )
