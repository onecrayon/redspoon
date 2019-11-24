from sqlalchemy.exc import OperationalError

import falcon
from falcon.asgi import Request, Response

__all__ = (
    'HealthCheck',
)


class HealthCheck:
    """Check internal systems for faults"""
    async def on_get(self, req: Request, resp: Response):
        # Default okay response
        resp.media = {
            'status': 'okay',
            'services': {
                'database': 'okay',
            }
        }
        # Verify that the database is up and running
        try:
            meaning_of_life_the_universe_and_everything = req.context.session.execute(
                'SELECT 42'
            ).scalar()
            assert meaning_of_life_the_universe_and_everything == 42
        except (AssertionError, OperationalError):
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
            resp.media['status'] = 'error'
            resp.media['services']['database'] = 'error'
