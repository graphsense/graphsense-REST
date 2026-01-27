"""Tests for TagAccessLoggerTagstoreProxy."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from graphsenselib.tagstore.db.queries import TagPublic

from gsrest.dependencies import TagAccessLoggerTagstoreProxy


def create_mock_tag(
    identifier: str = "test_address",
    creator: str = "test_creator",
    network: str = "btc",
) -> TagPublic:
    """Create a mock TagPublic object for testing."""
    return TagPublic(
        identifier=identifier,
        label="Test Label",
        source="test_source",
        creator=creator,
        confidence="high",
        confidence_level=100,
        tag_subject="address",
        tag_type="direct",
        actor=None,
        primary_concept=None,
        additional_concepts=[],
        is_cluster_definer=False,
        network=network,
        lastmod=1234567890,
        group="public",
        inherited_from=None,
        tagpack_title="Test Tagpack",
        tagpack_uri=None,
    )


class TestShouldLogResult:
    """Tests for _should_log_result method."""

    def setup_method(self):
        self.mock_tagstore_db = MagicMock()
        self.mock_redis = AsyncMock()
        self.proxy = TagAccessLoggerTagstoreProxy(
            self.mock_tagstore_db, self.mock_redis, "test_prefix"
        )

    def test_returns_false_for_none(self):
        """Should return (False, False) for None result."""
        result = self.proxy._should_log_result(None)
        assert result == (False, False)

    def test_returns_false_for_empty_list(self):
        """Should return (False, False) for empty list."""
        result = self.proxy._should_log_result([])
        assert result == (False, False)

    def test_returns_false_for_empty_string(self):
        """Should return (False, False) for empty string."""
        result = self.proxy._should_log_result("")
        assert result == (False, False)

    def test_returns_true_for_single_tag(self):
        """Should return (True, False) for a single TagPublic object."""
        tag = create_mock_tag()
        result = self.proxy._should_log_result(tag)
        assert result == (True, False)

    def test_returns_true_true_for_list_of_tags(self):
        """Should return (True, True) for a list of TagPublic objects."""
        tags = [create_mock_tag(identifier="addr1"), create_mock_tag(identifier="addr2")]
        result = self.proxy._should_log_result(tags)
        assert result == (True, True)

    def test_returns_false_for_string(self):
        """Should return (False, False) for string result."""
        result = self.proxy._should_log_result("some string")
        assert result == (False, False)

    def test_returns_false_for_dict(self):
        """Should return (False, False) for dict result."""
        result = self.proxy._should_log_result({"key": "value"})
        assert result == (False, False)

    def test_returns_false_for_list_of_non_tags(self):
        """Should return (False, False) for list of non-TagPublic objects."""
        result = self.proxy._should_log_result([1, 2, 3])
        assert result == (False, False)

    def test_returns_false_for_integer(self):
        """Should return (False, False) for integer result."""
        result = self.proxy._should_log_result(42)
        assert result == (False, False)


class TestLogTagAccess:
    """Tests for _log_tag_access method."""

    def setup_method(self):
        self.mock_tagstore_db = MagicMock()
        self.mock_redis = AsyncMock()
        self.proxy = TagAccessLoggerTagstoreProxy(
            self.mock_tagstore_db, self.mock_redis, "tag_access"
        )

    @pytest.mark.asyncio
    async def test_increments_redis_key_with_correct_format(self):
        """Should call redis.incr with correctly formatted key."""
        tag = create_mock_tag(
            identifier="1ABC123", creator="iknaio", network="btc"
        )

        with patch("gsrest.dependencies.time") as mock_time:
            mock_time.localtime.return_value = None
            mock_time.strftime.return_value = "2025-01-27"

            await self.proxy._log_tag_access("get_tags", tag)

        expected_key = "tag_access|2025-01-27|iknaio|btc|1ABC123"
        self.mock_redis.incr.assert_called_once_with(expected_key)

    @pytest.mark.asyncio
    async def test_uses_configured_prefix(self):
        """Should use the configured prefix in the Redis key."""
        proxy = TagAccessLoggerTagstoreProxy(
            self.mock_tagstore_db, self.mock_redis, "custom_prefix"
        )
        tag = create_mock_tag(identifier="addr1", creator="creator1", network="eth")

        with patch("gsrest.dependencies.time") as mock_time:
            mock_time.localtime.return_value = None
            mock_time.strftime.return_value = "2025-12-31"

            await proxy._log_tag_access("some_method", tag)

        expected_key = "custom_prefix|2025-12-31|creator1|eth|addr1"
        self.mock_redis.incr.assert_called_once_with(expected_key)


class TestProxyMethodCalls:
    """Tests for __getattr__ proxy behavior."""

    def setup_method(self):
        self.mock_tagstore_db = MagicMock()
        self.mock_redis = AsyncMock()
        self.proxy = TagAccessLoggerTagstoreProxy(
            self.mock_tagstore_db, self.mock_redis, "test_prefix"
        )

    @pytest.mark.asyncio
    async def test_proxies_method_call_to_underlying_db(self):
        """Should proxy method calls to the underlying tagstore_db."""
        mock_method = AsyncMock(return_value=None)
        self.mock_tagstore_db.get_tags = mock_method

        await self.proxy.get_tags("btc", "some_address")

        mock_method.assert_called_once_with("btc", "some_address")

    @pytest.mark.asyncio
    async def test_returns_result_from_underlying_method(self):
        """Should return the result from the underlying method."""
        expected_result = {"data": "test"}
        self.mock_tagstore_db.some_method = AsyncMock(return_value=expected_result)

        result = await self.proxy.some_method()

        assert result == expected_result

    @pytest.mark.asyncio
    async def test_logs_single_tag_result(self):
        """Should log access when method returns a single TagPublic."""
        tag = create_mock_tag(identifier="addr1", creator="creator1", network="btc")
        self.mock_tagstore_db.get_tag = AsyncMock(return_value=tag)

        with patch("gsrest.dependencies.time") as mock_time:
            mock_time.localtime.return_value = None
            mock_time.strftime.return_value = "2025-01-27"

            result = await self.proxy.get_tag("btc", "addr1")

        assert result == tag
        self.mock_redis.incr.assert_called_once()
        call_args = self.mock_redis.incr.call_args[0][0]
        assert "test_prefix|2025-01-27|creator1|btc|addr1" == call_args

    @pytest.mark.asyncio
    async def test_logs_each_tag_in_list_result(self):
        """Should log access for each tag when method returns a list."""
        tags = [
            create_mock_tag(identifier="addr1", creator="creator1", network="btc"),
            create_mock_tag(identifier="addr2", creator="creator2", network="btc"),
        ]
        self.mock_tagstore_db.get_tags = AsyncMock(return_value=tags)

        with patch("gsrest.dependencies.time") as mock_time:
            mock_time.localtime.return_value = None
            mock_time.strftime.return_value = "2025-01-27"

            result = await self.proxy.get_tags("btc", ["addr1", "addr2"])

        assert result == tags
        assert self.mock_redis.incr.call_count == 2

    @pytest.mark.asyncio
    async def test_does_not_log_non_tag_results(self):
        """Should not log when method returns non-TagPublic results."""
        self.mock_tagstore_db.get_count = AsyncMock(return_value=42)

        result = await self.proxy.get_count()

        assert result == 42
        self.mock_redis.incr.assert_not_called()

    @pytest.mark.asyncio
    async def test_does_not_log_when_redis_client_is_none(self):
        """Should not attempt to log when redis_client is None."""
        proxy = TagAccessLoggerTagstoreProxy(
            self.mock_tagstore_db, None, "test_prefix"
        )
        tag = create_mock_tag()
        self.mock_tagstore_db.get_tag = AsyncMock(return_value=tag)

        result = await proxy.get_tag("btc", "addr1")

        assert result == tag
        # No exception should be raised

    def test_proxies_non_callable_attributes(self):
        """Should proxy non-callable attributes directly."""
        self.mock_tagstore_db.some_attribute = "test_value"

        result = self.proxy.some_attribute

        assert result == "test_value"
