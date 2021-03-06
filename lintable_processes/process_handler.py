"""Handles the linting process, between the GitHandler and Lintball."""

# Copyright 2015-2016 Capstone Team G
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List
from uuid import UUID

from git import Commit, Repo

from lintable_lintball.lint_report import LintReport
from lintable_processes.do_nothing_handler import DoNothingHandler
from lintable_processes.process_state import ProcessState


class ProcessHandler(object):
    """Handles the linting process, between the GitHandler and Lintball.

    It tracks the state of the process and delegates to side-effecting code
    for logging, db persistence, and GitHub status updates.
    """

    def __init__(self, uuid: UUID, repo: Repo, handlers: List[DoNothingHandler]):
        self.state = ProcessState.STARTED
        self.uuid = uuid
        self.repo = repo
        self.handlers = handlers
        self.a_commit = None
        self.b_commit = None
        self.local_path = None
        self.repo_path = None
        self.a_path = None
        self.b_path = None
        self.files = []

    def started(self):
        """Kicks off the process.

        :return:
        """
        for h in self.handlers:
            h.started(uuid=self.uuid)

    def clone_repo(self, local_path: str, repo_path: str, a_path: str, b_path: str):
        """Indicates a repo has been cloned and where that clone is located.

        :param local_path: The path of the cloned repo.
        :param repo_path:
        :param a_path:
        :param b_path:
        :return:
        """

        self.state = ProcessState.CLONE_REPO
        self.local_path = local_path
        self.repo_path = repo_path
        self.a_path = a_path
        self.b_path = b_path

        for h in self.handlers:
            h.clone_repo(self.uuid, self.repo, local_path)

        return

    def retrieve_changed_file_set(self, a_commit: Commit, b_commit: Commit):
        """Indicates what files are going to be retrieved for the 2 commits.

        :param a_commit: The commit we are checking for changed files
        :param b_commit: The commit we are comparing against
        :return:
        """

        self.state = ProcessState.RETRIEVE_FILES
        self.a_commit = a_commit
        self.b_commit = b_commit

        for h in self.handlers:
            h.retrieve_changed_file_set(self.uuid, a_commit, b_commit)

        return

    def retrieve_file_from_commit(self, file: str, commit: Commit):
        """Called for each file being retrieved.

        :param file: The filename being retrieved
        :param commit: The commit it is being retrieved from.
        :return:
        """

        # track which files we have retrieved
        self.files.append(file)

        for h in self.handlers:
            h.retrieve_file_from_commit(self.uuid, file, commit)

        return

    def lint_file(self, linter: str, file: str):
        """Called when each file is linted.

        :param linter: The name of the linter being used
        :param file: The filename being linted.
        :return:
        """

        self.state = ProcessState.LINT_FILES

        for h in self.handlers:
            h.lint_file(self.uuid, linter, file)

        return

    def report(self, report: LintReport):
        """Called when the linting process has produced a LintReport.

        :param report: The lint report being produced.
        :return:
        """

        self.state = ProcessState.REPORT

        for h in self.handlers:
            h.report(self.uuid, report)

        return

    def finish(self):
        """Called as a last step to clean up the linting process.

        :return:
        """

        self.state = ProcessState.FINISHED

        for h in self.handlers:
            h.finish(self.uuid)

        return
