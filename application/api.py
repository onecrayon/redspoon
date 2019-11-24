"""Configures the main Falcon app and routes

`app` is hoisted to the main application; e.g.:

    from application import app
"""
from falcon.asgi import App

from . import views
from .environment import settings
from .middleware.sqlalchemy import SQLAlchemySessionManager
from .middleware.firebase import FirebaseSessionManager


# Create our main application
app = App(middleware=[
    SQLAlchemySessionManager(),
    FirebaseSessionManager(),
])
# Allow HTTP cookies for local development
app.resp_options.secure_cookies_by_default = settings.debug

# Define our application routes
app.add_route('/health-check', views.HealthCheck())
app.add_route('/session', views.FirebaseAuth())
