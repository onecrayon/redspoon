"""Configures the main Falcon app and routes

`app` is hoisted to the main application; e.g.:

    from application import app
"""
from falcon.asgi import App

from . import views
from .middleware.sqlalchemy import SQLAlchemySessionManager


# Create our main application
app = App(middleware=[
    SQLAlchemySessionManager()
])

# Define our application routes
app.add_route('/health-check', views.HealthCheck())
