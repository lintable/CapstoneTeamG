from logging import Logger
from uuid import UUID

from git import Repo

from lintball.lint_report import LintReport
from process_handler.do_nothing_handler import DoNothingHandler


class LogHandler(DoNothingHandler):

    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def lint_file(self, linter: str, file: str):
        super().lint_file(linter, file)
        self.logger.info('Linting {file} with linter {linter}'.format(file=file, linter=linter))

    def retrieve_files(self, a_commit: str, b_commit: str):
        super().retrieve_files(a_commit, b_commit)
        self.logger.info('Retrieving files from {a_commit} and {b_commit}'.format(a_commit=a_commit, b_commit=b_commit))

    def report(self, report: LintReport):
        super().report(report)
        num_of_files = len(report.errors)
        files_with_errors = dict((filename, errors) for filename, errors in report.errors.items() if len(errors) > 0)

        self.logger.info('Total number of files processed: {nof}\t Files with errors: {fwe}'.format(nof=num_of_files,
                                                                                     fwe=len(files_with_errors)))
        for f, e in report.errors.items():
            if len(e) > 0:
                self.logger.info('File {file} contains $errors errors.'.format(file=f, e=len(e)))
                for l, c, m in e:
                    self.logger.info('[{line}, {column}] - {message}'.format(line=l, column=c, message=m))
            else:
                self.logger.info('{file} contained no errors.'.format(file=f))

    def started(self, uuid: UUID, comment_id: int = None[int]):
        super().started(uuid, comment_id)
        self.logger.info('Starting linting process with id: {uuid}'.format(uuid=uuid))
        if type(comment_id) is int and comment_id >= 0:
            self.logger.debug('Comment id is {comment_id}'.format(comment_id=comment_id))

    def clone_repo(self, uuid: UUID, repo: Repo, local_path: str):
        super().clone_repo(uuid, repo, local_path)
        self.logger.info('Cloning repo {repo}'.format(repo=str(repo)))

    def retrieve_file(self, file: str, commit: str):
        super().retrieve_file(file, commit)
        self.logger.info('Retrieving {file} from {commit}'.format(file=file, commit=commit))
