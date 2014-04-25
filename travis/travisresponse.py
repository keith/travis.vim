import datetime


class TravisResponse(object):
    _build_id = 0
    _start_time = ""
    _end_time = ""
    _state = ""

    def __init__(self, json, root, repo):
        if not root:
            root = "branch"
        branch = json[root]
        self.build_id = branch["id"]
        self._start_time = branch["started_at"]
        self._end_time = branch["finished_at"]
        self._state = branch["state"]
        self.repo = repo

    def html_url(self, repo_url):
        if not repo_url:
            repo_url = self.repo.repo_path(None)
        return "https://travis-ci.org/%s/builds/%s" % (repo_url, self.build_id)

    def message(self):
        if self._end_time:
            message = (self.state +
                       " (Updated %s)" % self.end_time +
                       " |%s|" % self.html_url(None))
        else:
            message = "Pending... (Started %s)" % self.start_time
        return message

    @property
    def start_time(self):
        try:
            time = self.iso_date(self._start_time)
            return TravisResponse.pretty_date(time)
        except ValueError as e:
            return e

    @property
    def end_time(self):
        try:
            time = self.iso_date(self._end_time)
            return TravisResponse.pretty_date(time)
        except ValueError:
            return self.start_time

    @property
    def state(self):
        return self._state.title()

    @staticmethod
    def iso_date(dt):
        if not dt:
            return None
        return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def pretty_date(d):
        if not d:
            raise ValueError("Invalid Date")

        diff = datetime.datetime.utcnow() - d
        s = diff.seconds
        if diff.days > 1:
            return "{} days ago".format(diff.days)
        elif diff.days == 1:
            return "Yesterday"
        elif s < 60:
            return "{} seconds ago".format(s)
        elif s < 120:
            return "One minute ago"
        elif s < 3600:
            return "{} minutes ago".format(s / 60)
        elif s < 7200:
            return "One hour ago"
        else:
            return "{} hours ago".format(s / 60 / 60)
