"""
Tests for web search data models and structures.
"""

import pytest
from datetime import datetime

from simple_webagent import (
    WebSearchQuery,
    WebSearchResult,
    WebSearchResponse,
    WebSearchAgentResponse,
)


@pytest.mark.inference
class TestWebSearchQuery:
    """Test WebSearchQuery model."""

    def test_web_search_query_creation(self):
        """Test creating a WebSearchQuery instance."""
        query = WebSearchQuery(
            query_text="What is AI?",
            search_type="search",
            num_results=3,
            api_key="test_key"
        )

        assert query.query_text == "What is AI?"
        assert query.search_type == "search"
        assert query.num_results == 3
        assert query.api_key == "test_key"

    def test_web_search_query_defaults(self):
        """Test WebSearchQuery with default values."""
        query = WebSearchQuery(query_text="Test query")

        assert query.query_text == "Test query"
        assert query.search_type == "search"
        assert query.num_results == 3
        assert query.api_key is None

    def test_web_search_query_validation(self):
        """Test WebSearchQuery validation."""
        # Valid query
        query = WebSearchQuery(
            query_text="Valid query",
            search_type="news",
            num_results=5
        )
        assert query.search_type == "news"
        assert query.num_results == 5


@pytest.mark.inference
class TestWebSearchResult:
    """Test WebSearchResult model."""

    def test_web_search_result_creation(self):
        """Test creating a WebSearchResult instance."""
        result = WebSearchResult(
            title="Test Title",
            url="https://example.com",
            domain="example.com",
            content="This is test content",
            date="2024-01-01",
            source="Test Source"
        )

        assert result.title == "Test Title"
        assert result.url == "https://example.com"
        assert result.domain == "example.com"
        assert result.content == "This is test content"
        assert result.date == "2024-01-01"
        assert result.source == "Test Source"

    def test_web_search_result_optional_fields(self):
        """Test WebSearchResult with optional fields."""
        result = WebSearchResult(
            title="Test Title",
            url="https://example.com",
            domain="example.com",
            content="Test content"
        )

        assert result.title == "Test Title"
        assert result.url == "https://example.com"
        assert result.domain == "example.com"
        assert result.content == "Test content"
        assert result.date is None
        assert result.source is None


@pytest.mark.inference
class TestWebSearchResponse:
    """Test WebSearchResponse model."""

    def test_web_search_response_creation(self):
        """Test creating a WebSearchResponse instance."""
        results = [
            WebSearchResult(
                title="Result 1",
                url="https://example1.com",
                domain="example1.com",
                content="Content 1"
            ),
            WebSearchResult(
                title="Result 2",
                url="https://example2.com",
                domain="example2.com",
                content="Content 2"
            )
        ]

        response = WebSearchResponse(
            query="test query",
            search_type="search",
            results=results,
            summary="Test summary",
            generated_response="Generated response content",
            search_timestamp=datetime.now()
        )

        assert response.query == "test query"
        assert response.search_type == "search"
        assert len(response.results) == 2
        assert response.summary == "Test summary"
        assert response.generated_response == "Generated response content"
        assert isinstance(response.search_timestamp, datetime)


@pytest.mark.inference
class TestWebSearchAgentResponse:
    """Test WebSearchAgentResponse model."""

    def test_web_search_agent_response_creation(self):
        """Test creating a WebSearchAgentResponse instance."""
        sources = [
            "https://source1.com",
            "https://source2.com",
            "https://source3.com"
        ]

        response = WebSearchAgentResponse(
            user_query="What is machine learning?",
            search_results_summary="Summary of search results",
            comprehensive_answer="This is a comprehensive answer about machine learning...",
            sources=sources,
            confidence_level="high"
        )

        assert response.user_query == "What is machine learning?"
        assert response.search_results_summary == "Summary of search results"
        assert response.comprehensive_answer == "This is a comprehensive answer about machine learning..."
        assert len(response.sources) == 3
        assert response.confidence_level == "high"

    def test_web_search_agent_response_empty_sources(self):
        """Test WebSearchAgentResponse with empty sources."""
        response = WebSearchAgentResponse(
            user_query="Test query",
            search_results_summary="Test summary",
            comprehensive_answer="Test answer",
            sources=[],
            confidence_level="medium"
        )

        assert response.user_query == "Test query"
        assert response.search_results_summary == "Test summary"
        assert response.comprehensive_answer == "Test answer"
        assert len(response.sources) == 0
        assert response.confidence_level == "medium"

    def test_confidence_levels(self):
        """Test different confidence levels."""
        for level in ["high", "medium", "low"]:
            response = WebSearchAgentResponse(
                user_query="Test",
                search_results_summary="Summary",
                comprehensive_answer="Answer",
                sources=[],
                confidence_level=level
            )
            assert response.confidence_level == level


@pytest.mark.inference
class TestModelIntegration:
    """Test integration between models."""

    def test_complete_workflow_models(self):
        """Test a complete workflow using all models."""
        # Create search query
        query = WebSearchQuery(
            query_text="What are the benefits of renewable energy?",
            search_type="search",
            num_results=3
        )

        # Create search results
        results = [
            WebSearchResult(
                title="Renewable Energy Benefits",
                url="https://example.com/renewable-benefits",
                domain="example.com",
                content="Renewable energy provides clean, sustainable power...",
                date="2024-01-15",
                source="Energy Journal"
            ),
            WebSearchResult(
                title="Environmental Impact of Renewables",
                url="https://example.com/environmental-impact",
                domain="example.com",
                content="Renewable sources reduce carbon emissions significantly...",
                date="2024-01-10",
                source="Green Energy Magazine"
            )
        ]

        # Create search response
        search_response = WebSearchResponse(
            query=query.query_text,
            search_type=query.search_type,
            results=results,
            summary="Found 2 relevant articles about renewable energy benefits",
            generated_response="Based on the search results, renewable energy offers several key benefits...",
            search_timestamp=datetime.now()
        )

        # Create agent response
        agent_response = WebSearchAgentResponse(
            user_query=query.query_text,
            search_results_summary=search_response.summary,
            comprehensive_answer="Renewable energy benefits include reduced carbon emissions, energy independence, and economic growth...",
            sources=[result.url for result in results],
            confidence_level="high"
        )

        # Verify the complete workflow
        assert agent_response.user_query == query.query_text
        assert len(agent_response.sources) == len(results)
        assert agent_response.confidence_level == "high"
        assert search_response.query == query.query_text
        assert len(search_response.results) == len(results)
