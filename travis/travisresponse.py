import datetime
from dateexception import DateException


class TravisResponse(object):
    _build_id = 0
    _start_time = ""
    _end_time = ""
    _state = ""

    def __init__(self, json):
        branch = json["branch"]
        self._build_id = branch["id"]
        self._start_time = branch["started_at"]
        self._end_time = branch["finished_at"]
        self._state = branch["state"]

    @property
    def build_id(self):
        return self._build_id

    @property
    def start_time(self):
        # TODO: Pretty this
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def state(self):
        # TODO: Make this a enum type thingy
        return self._state

    @staticmethod
    def html_url(self, repo_url):
        return "https://travis-ci.org/%s/builds/%s" % (repo_url, self.build_id)

    @staticmethod
    def iso_date(self, dt):
        if not dt:
            return None
        return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def pretty_date(d):
        if not d:
            raise DateException("Invalid Date")

        # TODO: Times are lying
        diff = datetime.datetime.utcnow() - d
        s = diff.seconds
        if s < 10:
            return "Just now"
        elif s < 60:
            return "{} seconds ago".format(s)
        elif s < 120:
            return "One minute ago"
        elif s < 3600:
            return "{} minutes ago".format(s / 60)
        elif s < 7200:
            return "One hour ago"
        elif diff.days < 1:
            return "{} hours ago".format(s / 60 / 60)
        elif diff.days == 1:
            return "Yesterday"
        else:
            return "{} days ago".format(diff.days)
