""" Sermos' Flask Implementation and Tooling. Convenience imports here.
"""
import logging

logger = logging.getLogger(__name__)

try:
    from sermos.utils.smorest import Blueprint, Api, abort

except Exception as e:
    logger.error("Unable to import Web services (Blueprint, API, abort)"
                 f" ... {e}")

try:
    from sermos.flask.flask_sermos import FlaskSermos
except Exception as e:
    logger.exception("Unable to import Sermos services (FlaskSermos)"
                     f" ... {e}")
