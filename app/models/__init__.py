from .results import get_result_model
from .polls import Poll
from sqlalchemy.exc import OperationalError

try:
    results = {
        p.name: get_result_model(p) for p in Poll.query.all()
    }
except OperationalError:
    results = {}
