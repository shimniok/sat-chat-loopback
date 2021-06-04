from flask.json import JSONEncoder
from datetime import datetime, timezone

dt_fmt = "%Y-%m-%dT%H:%M:%SZ"

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                #new = obj.replace(tzinfo=timezone.utc)
                #return new.isoformat()
                return datetime.strftime(obj, dt_fmt)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
