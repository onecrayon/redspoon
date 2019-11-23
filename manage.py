#!/usr/bin/env python3
"""Easy server running for debugging"""
import argparse
import os.path
import sys
from typing import Tuple

from alembic.config import main as alembic_cli
import pytest
import uvicorn
from dotenv import load_dotenv


def log_error_and_exit(error: str):
    """Logs an error to STDERR and exits with a generic error code"""
    print(error, file=sys.stderr)
    sys.exit(1)


def get_action_and_args() -> Tuple[str, list]:
    """Parse command line arguments, optionally load .env file, and return selected action and any extra arguments"""
    parser = argparse.ArgumentParser(description='Run gunicorn API server, execute tests, or manage migrations')
    parser.add_argument('-e', '--env', '--environment', dest='environment', metavar='ENV', nargs='?', type=str,
                        default=None, help='optionally load in environment settings for `ENV`')
    parser.add_argument('action', nargs='?', type=str, default='run', choices=('run', 'test', 'db'),
                        help='specify your action (defaults to `run`); `test` is an alias for pytest and '
                             '`db` is an alias for alembic')
    # Parse in our command-line arguments
    main_args = []
    action_args = []
    # Check if a "help" arg comes after the action (need to pass it through, if that's the case)
    hit_action = False
    env_variable = False
    for arg in sys.argv[1:]:
        if hit_action:
            action_args.append(arg)
        elif env_variable:
            main_args.append(arg)
            env_variable = False
        else:
            if arg in ('-e', '--env', '--environment'):
                env_variable = True
            elif arg in ('test', 'db'):
                hit_action = True
            main_args.append(arg)

    args = parser.parse_args(args=main_args)

    # Load up our environment, if necessary
    if args.environment:
        env_path = f'environments/.env.{args.environment}'
        if not os.path.exists(env_path):
            log_error_and_exit(f'No environment defined at `{env_path}`')
        load_dotenv(dotenv_path=env_path)
        print(f'Successfully loaded settings from `{env_path}`!')

    return args.action, action_args


# "Zhu Li! Do the thing!"
if __name__ == "__main__":
    action, extra_args = get_action_and_args()
    # Now that environment is setup, load in our settings
    from application import settings

    if action == 'run':
        uvicorn.run('application:app', host="localhost", port=8080, reload=settings.debug)
    elif action == 'test':
        pytest.main(extra_args)
    elif action == 'db':
        alembic_cli(argv=extra_args, prog='./manage.py db')
    else:
        log_error_and_exit(f'Unrecognized command: `{action}`')
