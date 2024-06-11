"""Module for handling templates."""

import atexit
import glob
import ntpath
import os
import shutil
import tempfile

from git import GitCommandError, Repo

import ansibledoctor.exception
from ansibledoctor.utils import SingleLog


class Template:
    """
    Represents a template that can be used to generate content.

    Templates can besourced from a local file or a Git repository. The `Template` class handles
    the initialization and setup of a template, including cloning a Git repository if necessary.

    Args:
    ----
        name (str): The name of the template.
        src (str): The source of the template, in the format `<provider>><path>`.
        Supported providers are `local` and `git`.

    Raises:
    ------
        ansibledoctor.exception.TemplateError

    """

    def __init__(self, name, src):
        self.log = SingleLog()
        self.logger = self.log.logger

        try:
            provider, path = src.split(">", 1)
        except ValueError as e:
            raise ansibledoctor.exception.TemplateError(
                "Error reading template src", str(e)
            ) from e

        self.provider = provider.strip().lower()
        self.path = path.strip()

        if self.provider == "local":
            self.path = os.path.realpath(os.path.join(path, name))
        elif self.provider == "git":
            repo_url, branch_or_tag = path.split("#", 1) if "#" in path else (path, None)
            temp_dir = self._clone_repo(repo_url, branch_or_tag)
            self.path = os.path.join(temp_dir, name)
        else:
            raise ansibledoctor.exception.TemplateError(
                f"Unsupported template provider: {provider}"
            )

        self.files = self._scan_files()

    def _clone_repo(self, repo_url, branch_or_tag=None):
        temp_dir = tempfile.mkdtemp(prefix="ansibledoctor-")
        atexit.register(self._cleanup_temp_dir, temp_dir)

        try:
            self.logger.debug(f"Cloning template repo '{repo_url}'")
            repo = Repo.clone_from(repo_url, temp_dir)
            if branch_or_tag:
                self.logger.debug(f"Checking out branch or tag '{branch_or_tag}'")
                try:
                    repo.git.checkout(branch_or_tag)
                except GitCommandError as e:
                    raise ansibledoctor.exception.TemplateError(
                        f"Error checking out branch or tag '{branch_or_tag}': {e}"
                    ) from e

            return temp_dir
        except GitCommandError as e:
            msg = e.stderr.strip("'").strip()
            msg = msg.removeprefix("stderr: ")

            raise ansibledoctor.exception.TemplateError(
                f"Error cloning Git repository: {msg}"
            ) from e

    def _scan_files(self):
        """Search for Jinja2 (.j2) files to apply to the destination."""
        template_files = []

        if os.path.isdir(self.path):
            self.logger.info(f"Using template: {os.path.relpath(self.path, self.log.ctx)}")
        else:
            self.log.sysexit_with_message(f"Can not open template directory {self.path}")

        for file in glob.iglob(self.path + "/**/*.j2", recursive=True):
            relative_file = file[len(self.path) + 1 :]
            if ntpath.basename(file)[:1] != "_":
                self.logger.debug(f"Found template file: {relative_file}")
                template_files.append(relative_file)
            else:
                self.logger.debug(f"Ignoring template file: {relative_file}")

        return template_files

    @staticmethod
    def _cleanup_temp_dir(temp_dir):
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
