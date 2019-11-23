from falcon.asgi import Request
from application.db import SessionLocal


class SQLAlchemySessionManager:
    """Falcon middleware to create an SQLAlchemy session for every request, and close it when the request ends.

    Access to session is available through `req.context.session`.

    Automatically closes the session when the request is complete (but doesn't roll anything back, currently).

    Inspired by <https://eshlox.net/2019/05/28/integrate-sqlalchemy-with-falcon-framework-second-version>"""
    def process_resource(self, req: Request, resp, resource, params):
        if req.method == 'OPTIONS':
            return

        req.context.session = SessionLocal()

    def process_response(self, req: Request, resp, resource, req_succeeded: bool):
        if req.method == 'OPTIONS':
            return

        if 'session' in req.context:
            req.context.session.close()
