"""Configures Firebase support

Importing through this file ensures that the application is instantiated prior to any calls.
"""
import firebase_admin
from firebase_admin import auth, exceptions

# Initialize our Firebase app for managing user credentials
firebase_app = firebase_admin.initialize_app()
