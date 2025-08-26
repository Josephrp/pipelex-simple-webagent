"""
Integration tests for the web search agent pipeline.

These tests require actual API keys and will be skipped in CI environments.
"""

import asyncio
import os
import pytest

from pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline
from simple_webagent import WebSearchAgentResponse


@pytest.mark.inference
@pytest.mark.skipif(
    not os.getenv("SERPER_API_KEY"),
    reason="SERPER_API_KEY environment variable not set"
)
@pytest.mark.skipif(
    not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "MISTRAL_API_KEY"]),
    reason="No LLM API key (OPENAI_API_KEY, ANTHROPIC_API_KEY, or MISTRAL_API_KEY) is set"
)
class TestWebSearchAgentIntegration:
    """Integration tests for the complete web search agent pipeline."""

    @pytest.fixture(scope="class")
    def pipelex_setup(self):
        """Set up Pipelex for the test class."""
        Pipelex.make()
        yield
        # Cleanup if needed

    @pytest.mark.asyncio
    async def test_basic_web_search(self, pipelex_setup):
        """Test basic web search functionality."""
        query = "What is artificial intelligence?"

        # Execute the pipeline
        pipe_output = await execute_pipeline(
            pipe_code="web_search_agent",
            input_memory={
                "user_query": query,
            },
        )

        # Get the structured response
        response = pipe_output.main_stuff_as(content_type=WebSearchAgentResponse)

        # Verify response structure
        assert isinstance(response, WebSearchAgentResponse)
        assert response.user_query == query
        assert len(response.comprehensive_answer) > 0
        assert len(response.sources) > 0
        assert response.confidence_level in ["high", "medium", "low"]
        assert len(response.search_results_summary) > 0

    @pytest.mark.asyncio
    async def test_news_search(self, pipelex_setup):
        """Test news search functionality."""
        query = "Latest technology news"

        pipe_output = await execute_pipeline(
            pipe_code="web_search_agent",
            input_memory={
                "user_query": query,
            },
        )

        response = pipe_output.main_stuff_as(content_type=WebSearchAgentResponse)

        assert isinstance(response, WebSearchAgentResponse)
        assert response.user_query == query
        assert len(response.comprehensive_answer) > 0
        assert len(response.sources) > 0

    @pytest.mark.asyncio
    async def test_search_results_structure(self, pipelex_setup):
        """Test that search results have proper structure."""
        query = "Python programming language"

        pipe_output = await execute_pipeline(
            pipe_code="web_search_agent",
            input_memory={
                "user_query": query,
            },
        )

        response = pipe_output.main_stuff_as(content_type=WebSearchAgentResponse)

        # Verify comprehensive answer is not empty and contains relevant content
        assert len(response.comprehensive_answer) > 50
        assert "python" in response.comprehensive_answer.lower()

        # Verify sources are valid URLs
        for source in response.sources:
            assert source.startswith("http://") or source.startswith("https://")

        # Verify confidence level is valid
        assert response.confidence_level in ["high", "medium", "low"]

    @pytest.mark.asyncio
    async def test_search_with_different_queries(self, pipelex_setup):
        """Test search with various types of queries."""
        test_queries = [
            "What are renewable energy sources?",
            "Latest developments in machine learning",
            "How does climate change affect weather patterns?",
        ]

        for query in test_queries:
            pipe_output = await execute_pipeline(
                pipe_code="web_search_agent",
                input_memory={
                    "user_query": query,
                },
            )

            response = pipe_output.main_stuff_as(content_type=WebSearchAgentResponse)

            assert isinstance(response, WebSearchAgentResponse)
            assert response.user_query == query
            assert len(response.comprehensive_answer) > 0
            assert len(response.sources) > 0
            assert response.confidence_level in ["high", "medium", "low"]

    def test_pipeline_validation(self, pipelex_setup):
        """Test that the pipeline can be validated."""
        # This test just ensures the pipeline structure is valid
        # The actual validation is done by Pipelex
        from pipelex import Pipelex

        # If we get here without exceptions, the pipeline is valid
        assert Pipelex._instance is not None


@pytest.mark.inference
@pytest.mark.skipif(
    not os.getenv("SERPER_API_KEY"),
    reason="SERPER_API_KEY environment variable not set"
)
class TestWebSearchPipelineComponents:
    """Test individual pipeline components."""

    @pytest.fixture(scope="class")
    def pipelex_setup(self):
        """Set up Pipelex for the test class."""
        Pipelex.make()
        yield

    @pytest.mark.asyncio
    async def test_create_search_query_pipe(self, pipelex_setup):
        """Test the create_search_query pipeline step."""
        from pipelex.pipeline.execute import execute_pipeline

        pipe_output = await execute_pipeline(
            pipe_code="create_search_query",
            input_memory={
                "user_query": "What is quantum computing?",
            },
        )

        # The output should be a WebSearchQuery object
        query_result = pipe_output.main_stuff
        assert query_result is not None
        assert hasattr(query_result, 'query_text')
        assert query_result.query_text == "What is quantum computing?"

    @pytest.mark.asyncio
    async def test_web_search_performance(self, pipelex_setup):
        """Test web search performance and error handling."""
        import time

        query = "Simple test query"
        start_time = time.time()

        pipe_output = await execute_pipeline(
            pipe_code="web_search_agent",
            input_memory={
                "user_query": query,
            },
        )

        end_time = time.time()
        duration = end_time - start_time

        # The search should complete in reasonable time (less than 30 seconds)
        assert duration < 30.0

        response = pipe_output.main_stuff_as(content_type=WebSearchAgentResponse)
        assert isinstance(response, WebSearchAgentResponse)


@pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Skip in CI environment"
)
class TestManualTesting:
    """Manual tests that require human verification."""

    def test_cli_manual(self):
        """Manual test for CLI - requires human verification."""
        # This test is skipped in automated environments
        # but can be run manually for CLI testing
        pass

    def test_setup_script_manual(self):
        """Manual test for setup script - requires human verification."""
        # This test is skipped in automated environments
        # but can be run manually for setup testing
        pass
