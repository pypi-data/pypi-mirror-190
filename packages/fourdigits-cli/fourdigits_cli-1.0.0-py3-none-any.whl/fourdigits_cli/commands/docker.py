import logging
import os
import re
from typing import Iterator
from uuid import uuid4

import click
from packaging.version import InvalidVersion, Version
from packaging.version import parse as version_parser

from fourdigits_cli.settings import DEFAULT_CONFIG
from fourdigits_cli.utils.docker import Docker, DockerException
from fourdigits_cli.utils.git import Git, GitException

logger = logging.getLogger(__name__)

group = click.Group(help="Docker helper command for auto building and pushing")


@click.group()
@click.option(
    "--registry-domain",
    help="Defaults to docker.io, env override DOCKER_REGISTRY_DOMAIN",
)
@click.option("--registry-user", help="env override DOCKER_REGISTRY_USER")
@click.option("--registry-password", help="env override DOCKER_REGISTRY_PASSWORD")
@click.option(
    "--image-user",
    help=f"Defaults to settings ({DEFAULT_CONFIG.docker_image_user}), env override DOCKER_IMAGE_USER",  # noqa: E501
)
@click.pass_context
def group(ctx, **options):
    ctx.obj = Docker(
        registry_user=options["registry_user"]
        or os.environ.get("DOCKER_REGISTRY_USER"),
        registry_password=options["registry_password"]
        or os.environ.get("DOCKER_REGISTRY_PASSWORD"),
        registry=options["registry_domain"]
        or os.environ.get("DOCKER_REGISTRY_DOMAIN", "docker.io"),
        image_user=options["image_user"]
        or os.environ.get("DOCKER_IMAGE_USER", DEFAULT_CONFIG.docker_image_user),
    )


@group.command()
@click.option(
    "--version",
    help="Version to build. If no version is supplied, it will try to get the current git tag",  # noqa: E501
)
@click.option("--target")
@click.option("--file", default="Dockerfile", show_default=True)
@click.option("--context", default=".", show_default=True)
@click.pass_obj
def build(docker: Docker, **options):
    version = get_and_check_version(options.get("version"))
    build_image_name = uuid4().hex
    try:
        docker.build(
            build_image_name,
            file=options.get("file"),
            context=options.get("context"),
            target=options.get("target"),
            build_tag=str(version),
        )
        for tag in generate_tags(version):
            docker.image_tag(
                build_image_name,
                docker.get_image_name(
                    repo=DEFAULT_CONFIG.docker_repo,
                    tag=tag,
                ),
            )
    except (DockerException, GitException) as e:
        raise click.UsageError(e)


@group.command()
@click.option(
    "--version",
    help="Version to build. If no version is supplied, it will try to get the current git tag",  # noqa: E501
)
@click.pass_obj
def push(docker: Docker, **options):
    version = get_and_check_version(options.get("version"))
    try:
        for tag in generate_tags(version):
            docker.push(
                docker.get_image_name(
                    repo=DEFAULT_CONFIG.docker_repo,
                    tag=tag,
                )
            )
    except (DockerException, GitException) as e:
        raise click.UsageError(e)


@group.command(help="Build and deploy given environment")
@click.argument("environment")
@click.option(
    "--version",
    help="Version to build. If no version is supplied, it will try to get the current git tag",  # noqa: E501
)
@click.option("--target")
@click.option("--file", default="Dockerfile", show_default=True)
@click.option("--context", default=".", show_default=True)
@click.pass_obj
def deploy(docker: Docker, environment, **options):
    if environment not in DEFAULT_CONFIG.environments:
        raise click.UsageError("Environment doesn't exists in the pyproject.toml")

    version = Git().rev_parse("--short", "HEAD").strip()

    # extra checks for acc and prd
    if environment in ["acc", "prd"]:
        current_commit_tags = Git().tag("--points-at", "HEAD").splitlines()
        for tag_version in current_commit_tags:
            try:
                version = version_parser(tag_version.strip())
            except (IndexError, InvalidVersion):
                continue

            if environment == "acc" and version.pre:
                break
            if environment == "prd" and not (
                version.pre or version.post or version.dev or version.local
            ):
                break
        else:
            if environment == "acc":
                raise click.UsageError(
                    f"Could not get valid version tag for ACC on current commit ({current_commit_tags}), valid format is: <major>.<minor>.<patch>rc<number>"  # noqa: E501
                )
            elif environment == "prd":
                raise click.UsageError(
                    f"Could not get valid version tag for PRD on current commit ({current_commit_tags}), valid format is: <major>.<minor>.<patch>"  # noqa: E501
                )

    # Download the latest image to increase build process
    latest_image = docker.get_image_name(
        repo=DEFAULT_CONFIG.docker_repo, tag=environment
    )
    try:
        docker.pull(latest_image)
    except DockerException:
        latest_image = None

    # Docker build, tag and push image
    build_image_name = uuid4().hex
    try:
        docker.build(
            build_image_name,
            file=options.get("file"),
            context=options.get("context"),
            target=options.get("target"),
            build_tag=str(version),
            cache_from=latest_image,
        )
        for tag in [environment, str(version)]:
            docker.image_tag(
                build_image_name,
                docker.get_image_name(
                    repo=DEFAULT_CONFIG.docker_repo,
                    tag=tag,
                ),
            )
            docker.push(
                docker.get_image_name(
                    repo=DEFAULT_CONFIG.docker_repo,
                    tag=tag,
                )
            )
    except DockerException as e:
        raise click.UsageError(e)


def get_and_check_version(version) -> Version:
    if not version:
        try:
            version = Git().describe("--abbrev=0", "--tags").strip()
        except GitException:
            raise click.UsageError("Could not get version from git repository")

    try:
        version_parser(version.strip())
    except InvalidVersion:
        raise click.UsageError(f"Invalid version number: {version}")

    return version


def generate_tags(version) -> list[str]:
    version = version if isinstance(version, Version) else version_parser(version)
    is_latest = True
    is_latest_major = True
    versions = [str(version)]

    if version.pre or version.post or version.dev or version.local:
        # If version has alpha/beta/rc/post/dev/local suffix,
        # don't update latest and latest major
        return versions

    for existing_version in get_all_git_version_tags():
        if version < existing_version:
            is_latest = False
        if version.major == existing_version.major and version < existing_version:
            is_latest_major = False

    if is_latest_major:
        versions.append(str(version.major))

    if is_latest:
        versions.append("latest")

    return versions


def get_all_git_version_tags() -> Iterator[Version]:
    for line in Git().ls_remote("--tags").splitlines():
        match = re.match(r".*refs/tags/([\d\.]+)$", line)
        if match:
            try:
                yield version_parser(match.group(1))
            except InvalidVersion:
                logger.debug(f"Could not parse version: {match.group(1)}")
