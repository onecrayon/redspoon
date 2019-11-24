import datetime

import falcon
from falcon.asgi import Request, Response

from application.firebase import auth, exceptions
from application.models import User

__all__ = (
    'FirebaseAuth',
)


class FirebaseAuth:
    """Validates user tokens, creating local accounts for them if needed"""
    async def on_post(self, req: Request, resp: Response):
        id_token = req.media.get('id_token')
        if not id_token:
            raise falcon.HTTPForbidden('Missing Token')
        # Download the cert and verify the token
        try:
            decoded_token = await auth.verify_id_token(id_token)
            uid = decoded_token['uid']
        except (ValueError, exceptions.InvalidIdTokenError):
            raise falcon.HTTPForbidden('Invalid Token')
        except exceptions.RevokedIdTokenError:
            raise falcon.HTTPForbidden('Token Revoked')
        except exceptions.CertificateFetchError:
            raise falcon.HTTPForbidden('Missing Certificate')

        # Create our session cookie
        try:
            expires_in = datetime.timedelta(days=7)
            session_cookie = await auth.create_session_cookie(id_token, expires_in=expires_in)
            resp.set_cookie(
                'session', session_cookie,
                expires=datetime.datetime.now() + expires_in
            )
        except exceptions.FirebaseError:
            raise falcon.HTTPForbidden('Session Cookie Failure')
        # Grab our local user object
        session = req.context.session
        user = session.query(User).filter(User.firebase_uid==uid).first()
        # Create our user, if this is their first sign-in
        if not user:
            user = User(firebase_uid=uid)
            session.add(user)
            session.commit()
        resp.status = falcon.HTTP_CREATED
    
    async def on_delete(self, req: Request, resp: Response):
        resp.unset_cookie('session')

