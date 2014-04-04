import datetime
import subprocess
import urlparse
import urllib2
import json
import re

try:
    import vim
except ImportError:
    in_vim = False
else:
    in_vim = True


def git_is_repo():
    return subprocess.call(["git", "rev-parse"]) == 0


def line_from_command(command):
    out = subprocess.Popen(command.split(" "),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    return out.stdout.readline().replace("\n", "")


def git_remote():
    # TODO: Get default remote name
    # TODO: get remote name off branch name
    # git rev-parse --abbref-ref branch@{u}
    # git for-each-ref --format='%(upstream:short)' $(git symbolic-ref -q HEAD)
    ref = line_from_command("git symbolic-ref -q HEAD")
    return line_from_command("git for-each-ref --format=%(upstream:short) "
                             + ref)


def git_remote_url(remote):
    r = remote.split("/")[0]
    return re.sub(r"\.git$", "",
                  line_from_command("git config remote.%s.url" % r))


def repo_path(url):
    # TODO: Fix removing url parts
    return re.sub(r"^/", "", urlparse.urlparse(url).path)


def git_current_branch():
    # TODO: Use current branch?
    # TODO: Branch to use
    # git name-rev --name-only HEAD
    # git rev-parse --abbrev-ref HEAD
    return line_from_command("git rev-parse --abbrev-ref HEAD")


def pretty_date(d):
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


def iso_date(dt):
    return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")


# def main(branch, remote):
def main():
    # if not branch:
    branch = git_current_branch()
    # if not remote:
    remote = git_remote()
    repo_url = repo_path(git_remote_url(remote))
    url = "https://api.travis-ci.org/repos/%s/branches/%s" % (repo_url, branch)
    if in_vim:
        vim.vars["travis_last_url"] = url
    # print url
    # url = "https://api.travis-ci.org/repos/CocoaPods/Specs"
    req = urllib2.Request(url,
                          headers={"Accept":
                                   "application/vnd.travis-ci.2+json"})
    try:
        res = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print("%d: %s" % (e.getcode(), e.reason))
        return
    # print res.getcode()
    j = json.loads(res.read())
    # print j
    j = j["branch"]
    started = j["started_at"]
    finished = j["finished_at"]
    message = "Pending... (Started %s)" % pretty_date(iso_date(started))
    if finished:
        time = iso_date(finished)
        message = pretty_date(time)
    message = (j["state"].title() +
               " (Updated %s)" % pretty_date(iso_date(finished)))
    print message

if not in_vim:
    if __name__ == "__main__":
        # main(None, None)
        main()
