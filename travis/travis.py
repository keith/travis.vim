import json
import urllib2

# Fuck you python.
# If someone can explain to me why python makes this such a
# pain In the ass I would love that
try:
    from travis.gitrepo import GitRepo
    from travis.travisresponse import TravisResponse
except ImportError:
    from gitrepo import GitRepo
    from travisresponse import TravisResponse


try:
    import vim
except ImportError:
    # Hack to ignore Vim code when running outside of vim
    class vim(object):
        vars = {}


# def main(branch, remote):
def main():
    # if not branch:
    # if in_vim:
    try:
        repo = GitRepo()
    except ValueError as e:
        print(e)
        return

    return
    # vim.vars["travis_last_url"] = url
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
    message = (travis.state +
               " (Updated %s)" % travis.end_time + " |%s|" % html_url)
    print(message)


# if not in_vim:
if __name__ == "__main__":
    # main(None, None)
    main()
