import os
import re
import subprocess
import urlparse


class GitRepo(object):
    def __init__(self):
        if not self.is_repo():
            raise ValueError("Not a git repo")

    def is_repo(self):
        with open(os.devnull, "w") as f:
            return subprocess.call("git rev-parse".split(), stderr=f) == 0

    def remote_name(self):
        # TODO: Get default remote name
        # TODO: get remote name off branch name
        # git rev-parse --abbref-ref branch@{u}
        # git for-each-ref --format='%(upstream:short)'
        #        $(git symbolic-ref -q HEAD)
        ref = self.__line_from_command("git symbolic-ref -q HEAD")
        return self.__line_from_command(
            "git for-each-ref --format=%(upstream:short) " + ref)

    def remote_url(self, remote=None):
        if not remote:
            remote = self.remote_name()
        r = remote.split("/")[0]
        return re.sub(r"\.git$",
                      "",
                      self.__line_from_command("git config remote.%s.url" % r))

    def repo_path(self, url):
        # TODO: Fix removing url parts
        if not url:
            url = self.remote_url()
        return re.sub(r"^/", "", urlparse.urlparse(url).path)

    def path_url(self, remote):
        return self.repo_path(self.remote_url(remote))

    def current_branch(self):
        # TODO: Use current branch?
        # TODO: Branch to use
        # git name-rev --name-only HEAD
        # git rev-parse --abbrev-ref HEAD
        return self.__line_from_command("git rev-parse --abbrev-ref HEAD")

    def travis_branch_url(self, remote, branch):
        if not remote:
            remote = self.remote_name()
        if not branch:
            branch = self.current_branch()
        path = self.path_url(remote)
        return ("https://api.travis-ci.org/repos/%s/branches/%s" %
                (path, branch))

    def travis_build_url(self, remote, build):
        if not remote:
            remote = self.remote_name()
        if not build:
            build = "23396887"
        path = self.path_url(remote)
        return ("https://api.travis-ci.org/repos/%s/builds/%s" %
                (path, build))

    @staticmethod
    def __line_from_command(command):
        out = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        return out.stdout.readline().replace("\n", "")
