import json
import logging
import time
from functools import wraps
from typing import List

import click

from clairvoyance import settings
from clairvoyance.notifiers import Notifier, SnsNotifier, StdoutNotifier
from clairvoyance.reporters import EcrReporter, Reporter

logger = logging.getLogger(__name__)


def timeit(func):
    """
    Decorator to time a function.
    """

    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info(f"Function {func.__name__}() took {total_time:.2f} seconds")
        return result

    return timeit_wrapper


class Clairvoyance:
    def __init__(self, reporter: Reporter, notifiers: List[Notifier] = None):
        self._reporter = reporter
        self._notifiers = notifiers
        self._findings = []

    def __repr__(self) -> str:
        return f"Clairvoyance initialized with {self._reporter} {self._notifiers}"

    @timeit
    def scan(self):
        self._findings = self._reporter.analyze()

        logger.info(f"{len(self._findings)} scan reports found")

    def report(self):
        self._reporter.report(self._findings)

    def notify(self):
        for notifier in self._notifiers:
            for finding in self._findings:
                subject = (
                    f"{finding['repositoryName']}:{finding['imageId']['imageTag']}"
                )
                notifier.send(
                    subject=subject,
                    message=json.dumps(finding, default=str),
                )


def init():
    try:
        # Fire the validator
        settings.validators.validate()

        reporter = EcrReporter(
            registry_id=settings.ECR.REGISTRY_ID,
            repositories=settings.ECR.REPOSITORIES,
            allowed_tag_patterns=settings.ECR.ALLOWED_TAG_PATTERNS,
        )

        notifiers = []

        for notifier in settings.NOTIFIERS:
            if notifier.TYPE == "sns":
                notifiers.append(SnsNotifier(topic_arn=notifier.TOPIC_ARN))
            elif notifier.TYPE == "stdout":
                notifiers.append(StdoutNotifier())

        clairvoyance = Clairvoyance(reporter=reporter, notifiers=notifiers)

        logger.info(clairvoyance)

        return clairvoyance
    except Exception as e:
        logger.error(str(e))


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        scan_and_report()


@cli.command()
def scan_and_report():
    clairvoyance = init()
    clairvoyance.scan()
    clairvoyance.report()


@cli.command()
def scan_only():
    clairvoyance = init()
    clairvoyance.scan()


@cli.command()
@click.argument("repository", required=True)
@click.argument("tag", required=True)
def notify(repository, tag):
    settings.ECR.REPOSITORIES = [repository]
    settings.ECR.ALLOWED_TAG_PATTERNS = [tag]

    clairvoyance = init()
    clairvoyance.scan()
    clairvoyance.notify()
