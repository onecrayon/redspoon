from falcon.asgi import Request, Response

from application.firebase import auth
from application.models.users import User, AnonymousUser

class FirebaseSessionManager:
    def process_resource(self, req: Request, resp: Response, resource, params):
        if req.method == 'OPTIONS':
            return
        # Fetch the user from the session
        session_cookie = req.cookies.get('session')
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
            uid = decoded_claims.get('uid')
            user = req.context.session.query(User).filter(User.firebase_uid==uid).first()
            if user:
                req.context.user = user
        except (ValueError, auth.InvalidSessionCookieError):
            resp.unset_cookie('session')
            req.context.user = AnonymousUser()
