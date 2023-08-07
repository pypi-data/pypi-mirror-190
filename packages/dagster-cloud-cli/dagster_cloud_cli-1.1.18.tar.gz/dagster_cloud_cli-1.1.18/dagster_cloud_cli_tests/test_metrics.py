import datetime
from unittest.mock import ANY, call

import freezegun
import pytest
import typer
from dagster_cloud_cli import ui
from dagster_cloud_cli.commands import metrics
from dagster_cloud_cli.config_utils import (
    dagster_cloud_options,
)
from dagster_cloud_cli.entrypoint import app
from dagster_cloud_cli.types import (
    CliEventTags,
    CliEventType,
)
from dagster_cloud_cli.utils import add_options
from typer.testing import CliRunner


@pytest.mark.parametrize(
    "envs, source",
    [
        ([], CliEventTags.source.cli),
        (["FOO"], CliEventTags.source.cli),
        (["GITHUB_ACTION"], CliEventTags.source.github),
        (["GITHUB_ACTION", "FOO"], CliEventTags.source.github),
        (["GITLAB_CI"], CliEventTags.source.gitlab),
        (["GITLAB_CI", "FOO"], CliEventTags.source.gitlab),
        (["GITHUB_ACTION", "GITLAB_CI"], CliEventTags.source.unknown),
    ],
)
def test_get_source(monkeypatch, envs, source):
    for env in envs:
        monkeypatch.setenv(env, "True")

    assert metrics.get_source() == source


def test_instrument(mocker):
    with freezegun.freeze_time(datetime.datetime.now()) as frozen_datetime:
        gql = mocker.patch("dagster_cloud_cli.commands.metrics.gql", autospec=True)

        app = typer.Typer()

        raising = {"raising": (bool, typer.Option(False, "--raising"))}

        @app.command(name="instrumented")
        @metrics.instrument(CliEventType.DEPLOY)
        @dagster_cloud_options(allow_empty=True, requires_url=True)
        @add_options(raising)
        def instrumented_command(api_token: str, url: str, raising: bool, **kwargs):
            frozen_datetime.tick()
            if raising:
                raise ui.error("boom")
            else:
                ui.print("ok")

        @app.command(name="uninstrumented")
        @dagster_cloud_options(allow_empty=True, requires_url=True)
        @add_options(raising)
        def uninstrumented_command(api_token: str, url: str, raising: bool, **kwargs):
            frozen_datetime.tick()
            if raising:
                raise ui.error("boom")
            else:
                ui.print("ok")

        @app.command(name="instrumented-with-tags")
        @metrics.instrument(CliEventType.DEPLOY, tags=[CliEventTags.server_strategy.pex])
        @dagster_cloud_options(allow_empty=True, requires_url=True)
        @add_options(raising)
        def instrumented_with_tags_command(api_token: str, url: str, raising: bool, **kwargs):
            frozen_datetime.tick()
            if raising:
                raise ui.error("boom")
            else:
                ui.print("ok")

        env = {
            "DAGSTER_CLOUD_API_TOKEN": "fake-token",
            "DAGSTER_CLOUD_ORGANIZATION": "fake-organization",
            "DAGSTER_CLOUD_DEPLOYMENT": "fake-deployment",
        }

        # It doesn't fail even if it can't connect to dagster
        # We never want the cause of the failure to because we can't send metrics
        result = CliRunner().invoke(
            app,
            ["instrumented"],
            env=env,
        )
        assert result.exit_code == 0
        gql.mark_cli_event.assert_not_called()

        env["DAGSTER_CLOUD_URL"] = "fake-url"

        result = CliRunner().invoke(app, ["instrumented"], env=env)
        assert result.exit_code == 0
        gql.mark_cli_event.assert_has_calls(
            [
                call(
                    client=ANY,
                    duration_seconds=1,
                    event_type=CliEventType.DEPLOY,
                    success=True,
                    tags=[],
                ),
            ]
        )

        gql.reset_mock()
        result = CliRunner().invoke(app, ["instrumented", "--raising"], env=env)
        assert result.exit_code == 1
        gql.mark_cli_event.assert_has_calls(
            [
                call(
                    client=ANY,
                    duration_seconds=1,
                    event_type=CliEventType.DEPLOY,
                    success=False,
                    tags=[],
                ),
            ]
        )

        gql.reset_mock()
        result = CliRunner().invoke(app, ["uninstrumented"], env=env)
        assert result.exit_code == 0
        gql.mark_cli_event.assert_not_called()

        gql.reset_mock()
        result = CliRunner().invoke(app, ["uninstrumented", "--raising"], env=env)
        assert result.exit_code == 1
        gql.mark_cli_event.assert_not_called()

        result = CliRunner().invoke(app, ["instrumented-with-tags"], env=env)
        assert result.exit_code == 0
        gql.mark_cli_event.assert_has_calls(
            [
                call(
                    client=ANY,
                    duration_seconds=1,
                    event_type=CliEventType.DEPLOY,
                    success=True,
                    tags=["server-strategy:pex"],
                ),
            ]
        )


@pytest.mark.parametrize(
    "command",
    [
        ["serverless", "build"],
        ["serverless", "build-python-executable", "foo"],
        ["serverless", "deploy-docker"],
        ["serverless", "deploy-python-executable"],
        ["serverless", "upload"],
        ["serverless", "upload-base-image"],
    ],
)
def test_all_instrumented_commands_have_urls(mocker, command):
    gql = mocker.patch("dagster_cloud_cli.commands.metrics.gql", autospec=True)

    env = {
        "DAGSTER_CLOUD_API_TOKEN": "fake-token",
        "DAGSTER_CLOUD_ORGANIZATION": "fake-organization",
        "DAGSTER_CLOUD_DEPLOYMENT": "fake-deployment",
    }

    CliRunner().invoke(app, command, env=env)
    gql.graphql_client_from_url.assert_called()
