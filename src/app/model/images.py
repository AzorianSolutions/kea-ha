

class ImageRepo(object):
    repo_url: str
    repo_name: str
    repo_tag: str

    @property
    def repo_path(self) -> str:
        """Returns the repo path."""

        repo_path: str = ''

        if self.repo_url is not None:
            repo_path += self.repo_url

        if self.repo_name is not None:
            if repo_path:
                repo_path += '/'
            repo_path += f'{self.repo_name}'

        if self.repo_tag is not None:
            repo_path += f':{self.repo_tag}'

        return repo_path

    def __init__(self, repo_url: str, repo_name: str, repo_tag: str):
        """Constructor."""
        self.repo_url = repo_url
        self.repo_name = repo_name
        self.repo_tag = repo_tag

    def __str__(self) -> str:
        """String representation."""
        return self.repo_path

    def __repr__(self) -> str:
        """Representation."""
        return "ImageRepo(repo_url=%s, repo_name=%s, repo_tag=%s)" % (self.repo_url, self.repo_name, self.repo_tag)

    @staticmethod
    def from_tag(tag: str) -> 'ImageRepo':
        """Extracts the repo URL, name, and tag from the tag argument."""
        repo_url: str = ''
        repo_name: str = ''
        repo_tag: str = ''

        if tag:
            if '/' in tag:
                if tag.count('/') == 1:
                    repo_name = tag
                else:
                    parts = tag.split('/', 1)
                    repo_url = parts[0]
                    repo_name = parts[1]
            else:
                repo_name = tag

            if repo_name.endswith(':'):
                repo_name = repo_name[:-1]

            if ':' in repo_name:
                parts = repo_name.split(':', 1)
                repo_name = parts[0]
                repo_tag = parts[1]

        return ImageRepo(repo_url, repo_name, repo_tag)
