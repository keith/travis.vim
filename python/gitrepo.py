import re
import subprocess
import urlparse


class GitRepo(object):
    def is_repo(self):
        return subprocess.call(["git", "rev-parse"]) == 0

    def remote_name(self):
        # TODO: Get default remote name
        # TODO: get remote name off branch name
        # git rev-parse --abbref-ref branch@{u}
        # git for-each-ref --format='%(upstream:short)'
        #        $(git symbolic-ref -q HEAD)
        ref = self.line_from_command("git symbolic-ref -q HEAD")
        return self.line_from_command(
            "git for-each-ref --format=%(upstream:short) " + ref)

    def remote_url(self, remote):
        r = remote.split("/")[0]
        return re.sub(r"\.git$",
                      "",
                      self.line_from_command("git config remote.%s.url" % r))

    def repo_path(self, url):
        # TODO: Fix removing url parts
        return re.sub(r"^/", "", urlparse.urlparse(url).path)

    def current_branch(self):
        # TODO: Use current branch?
        # TODO: Branch to use
        # git name-rev --name-only HEAD
        # git rev-parse --abbrev-ref HEAD
        return self.line_from_command("git rev-parse --abbrev-ref HEAD")

    def __line_from_command(self, command):
        out = subprocess.Popen(command.split(" "),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        return out.stdout.readline().replace("\n", "")
