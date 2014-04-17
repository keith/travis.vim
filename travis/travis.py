import urllib2
import json
from travis.gitrepo import GitRepo
from travis.travisresponse import TravisResponse

try:
    import vim
except ImportError:
    # Hack to ignore Vim code when running outside of vim
    class vim(object):
        vars = {}


# def main(branch, remote):
def main():
    # if not branch:
    repo = GitRepo()
    branch = repo.current_branch()
    # if not remote:
    remote = repo.remote_name()
    repo_url = repo.repo_path(repo.remote_url(remote))
    url = "https://api.travis-ci.org/repos/%s/branches/%s" % (repo_url, branch)
    # if in_vim:
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

    travis = TravisResponse(json.loads(res.read()))
    message = "Pending... (Started %s)" % travis.start_time
    html_url = ("https://travis-ci.org/%s/builds/%s" %
                (repo_url, travis.build_id))
    message = (travis.state.title() +
               " (Updated %s)" % travis.end_time + " |%s|" % html_url)
    print message


# if not in_vim:
if __name__ == "__main__":
    # main(None, None)
    main()
