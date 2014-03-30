import datetime
import subprocess
import urlparse
import urllib2
import json


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
    return line_from_command("git for-each-ref --format=%(upstream:short) " + ref)

def git_remote_url(remote):
    r = remote.split("/")[0]
    return line_from_command("git config remote.%s.url" % r)


def repo_path(url):
    # TODO: Fix removing url parts
    return urlparse.urlparse(url).path[:-4]


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
        datetime.datetime.now(time.localtime())
        return d.strftime("%b %d %Y")

def main(branch, remote):
    if not branch:
        branch = git_current_branch()
    if not remote:
        remote = git_remote()
    print branch
    print remote
    print git_remote_url(remote)
    print repo_path(git_remote_url(remote))
    url = "https://api.travis-ci.org/repos/CocoaPods/Core"
    res = urllib2.urlopen(url)
    j = json.loads(res.read())
    print j
    time = datetime.datetime.strptime(j["last_build_finished_at"],
                                     "%Y-%m-%dT%H:%M:%SZ")
    print time
    print pretty_date(time)
    # print "Foobar"

if __name__ == "__main__":
    main(None, None)
