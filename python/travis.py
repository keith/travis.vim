import subprocess


def git_is_repo():
    return subprocess.call(["git", "rev-parse"]) == 0


def git_remote():
    # TODO: Get default remote name
    pass


def git_current_branch():
    # TODO: Use current branch?
    # TODO: Branch to use
    pass


def main(branch, remote):
    if not branch:
        branch = git_current_branch()
    if not remote:
        remote = git_remote()
    print "Foobar"

# if __name__ == "__main__":
