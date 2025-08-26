"""
Tests for the main application entry point.
"""

import asyncio
import os
import pytest
from unittest.mock import patch, MagicMock

from main import search_and_answer, search_and_answer_sync


@pytest.mark.inference
class TestMainApplication:
    """Test main application functions."""

    @pytest.mark.skipif(
        not os.getenv("SERPER_API_KEY"),
        reason="SERPER_API_KEY environment variable not set"
    )
    @pytest.mark.skipif(
        not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "MISTRAL_API_KEY"]),
        reason="No LLM API key is set"
    )
    def test_search_and_answer_sync(self):
        """Test synchronous search function."""
        query = "What is AI?"
        response = search_and_answer_sync(query)

        assert response is not None
        assert hasattr(response, 'user_query')
        assert hasattr(response, 'comprehensive_answer')
        assert hasattr(response, 'sources')
        assert hasattr(response, 'confidence_level')
        assert response.user_query == query
        assert len(response.comprehensive_answer) > 0
        assert len(response.sources) > 0
        assert response.confidence_level in ["high", "medium", "low"]

    @pytest.mark.skipif(
        not os.getenv("SERPER_API_KEY"),
        reason="SERPER_API_KEY environment variable not set"
    )
    @pytest.mark.skipif(
        not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "MISTRAL_API_KEY"]),
        reason="No LLM API key is set"
    )
    @pytest.mark.asyncio
    async def test_search_and_answer_async(self):
        """Test asynchronous search function."""
        query = "What is machine learning?"
        response = await search_and_answer(query)

        assert response is not None
        assert response.user_query == query
        assert len(response.comprehensive_answer) > 0
        assert len(response.sources) > 0
        assert response.confidence_level in ["high", "medium", "low"]

    def test_search_without_api_keys_sync(self):
        """Test that functions handle missing API keys gracefully."""
        # Temporarily remove API keys
        original_serper = os.environ.get("SERPER_API_KEY")
        original_openai = os.environ.get("OPENAI_API_KEY")
        original_anthropic = os.environ.get("ANTHROPIC_API_KEY")
        original_mistral = os.environ.get("MISTRAL_API_KEY")

        try:
            # Remove API keys
            for key in ["SERPER_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "MISTRAL_API_KEY"]:
                os.environ.pop(key, None)

            # This should raise an exception
            with pytest.raises(Exception):
                search_and_answer_sync("test query")

        finally:
            # Restore original API keys
            if original_serper:
                os.environ["SERPER_API_KEY"] = original_serper
            if original_openai:
                os.environ["OPENAI_API_KEY"] = original_openai
            if original_anthropic:
                os.environ["ANTHROPIC_API_KEY"] = original_anthropic
            if original_mistral:
                os.environ["MISTRAL_API_KEY"] = original_mistral

    @pytest.mark.asyncio
    async def test_search_without_api_keys_async(self):
        """Test that async function handles missing API keys gracefully."""
        # Temporarily remove API keys
        original_serper = os.environ.get("SERPER_API_KEY")
        original_openai = os.environ.get("OPENAI_API_KEY")
        original_anthropic = os.environ.get("ANTHROPIC_API_KEY")
        original_mistral = os.environ.get("MISTRAL_API_KEY")

        try:
            # Remove API keys
            for key in ["SERPER_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "MISTRAL_API_KEY"]:
                os.environ.pop(key, None)

            # This should raise an exception
            with pytest.raises(Exception):
                await search_and_answer("test query")

        finally:
            # Restore original API keys
            if original_serper:
                os.environ["SERPER_API_KEY"] = original_serper
            if original_openai:
                os.environ["OPENAI_API_KEY"] = original_openai
            if original_anthropic:
                os.environ["ANTHROPIC_API_KEY"] = original_anthropic
            if original_mistral:
                os.environ["MISTRAL_API_KEY"] = original_mistral


@pytest.mark.inference
class TestMainCLI:
    """Test main CLI functionality."""

    @pytest.fixture
    def mock_argv(self):
        """Mock sys.argv for testing."""
        return ["main.py", "test query"]

    def test_main_without_args(self):
        """Test main function without arguments."""
        with patch("sys.argv", ["main.py"]):
            with patch("sys.exit") as mock_exit:
                import main
                main.main()
                mock_exit.assert_called_once_with(1)

    def test_main_with_args_but_no_api_keys(self):
        """Test main function with arguments but no API keys."""
        with patch("sys.argv", ["main.py", "test query"]):
            with patch("sys.exit") as mock_exit:
                import main
                main.main()
                mock_exit.assert_called_once_with(1)

    @pytest.mark.skipif(
        not os.getenv("SERPER_API_KEY"),
        reason="SERPER_API_KEY environment variable not set"
    )
    @pytest.mark.skipif(
        not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "MISTRAL_API_KEY"]),
        reason="No LLM API key is set"
    )
    def test_main_with_valid_args(self):
        """Test main function with valid arguments and API keys."""
        with patch("sys.argv", ["main.py", "What is AI?"]):
            with patch("sys.exit") as mock_exit:
                import main
                main.main()
                # Should not exit with error code if API keys are valid
                # Note: This test might be slow due to actual API calls


@pytest.mark.inference
class TestConfiguration:
    """Test configuration and setup."""

    def test_environment_variables_exist(self):
        """Test that environment variables are properly loaded."""
        # Check if .env file exists
        env_file_exists = os.path.exists(".env")

        # Check if env.example exists
        example_file_exists = os.path.exists("env.example")

        assert example_file_exists, "env.example file should exist"

        # If .env exists, check that it has required structure
        if env_file_exists:
            with open(".env", "r") as f:
                env_content = f.read()
                # Should contain key variable names (even if values are empty)
                assert "SERPER_API_KEY=" in env_content

    def test_package_imports(self):
        """Test that all package imports work correctly."""
        # Test main package import
        import simple_webagent
        assert simple_webagent is not None

        # Test submodules
        from simple_webagent import WebSearchAgentResponse, WebSearchQuery
        assert WebSearchAgentResponse is not None
        assert WebSearchQuery is not None

        # Test CLI import
        from simple_webagent import cli
        assert cli is not None

    def test_pipeline_structure(self):
        """Test that pipeline TOML files exist and have correct structure."""
        import os

        # Check that web search pipeline exists
        pipeline_file = "simple_webagent/web_search.toml"
        assert os.path.exists(pipeline_file), f"Pipeline file {pipeline_file} should exist"

        # Read and check basic structure
        with open(pipeline_file, "r") as f:
            content = f.read()
            assert "[pipe.web_search_agent]" in content
            assert "PipeSequence" in content
            assert "inputs" in content
            assert "steps" in content
