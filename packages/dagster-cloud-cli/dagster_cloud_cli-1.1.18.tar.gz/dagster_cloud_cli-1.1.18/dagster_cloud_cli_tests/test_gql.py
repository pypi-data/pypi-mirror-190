from unittest.mock import MagicMock

from dagster_cloud_cli.core.graphql_client import GqlShimClient
from dagster_cloud_cli.gql import mark_cli_event


def test_mark_cli_event_doesnt_raise():
    client = MagicMock(GqlShimClient, autospec=True)
    client.execute.side_effect = Exception("boom")

    mark_cli_event(
        client=client,
        event_type=MagicMock(),
        duration_seconds=MagicMock(),
        tags=MagicMock(),
    )
