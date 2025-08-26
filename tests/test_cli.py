"""
Tests for the CLI interface.
"""

import pytest
from typer.testing import CliRunner

from simple_webagent.cli import app


@pytest.mark.inference
class TestCLI:
    """Test CLI functionality."""

    @pytest.fixture
    def runner(self):
        """CLI runner fixture."""
        return CliRunner()

    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "simple-webagent" in result.output.lower()
        assert "web search agent" in result.output.lower()

    def test_search_help(self, runner):
        """Test search command help."""
        result = runner.invoke(app, ["search", "--help"])
        assert result.exit_code == 0
        assert "search" in result.output
        assert "--news" in result.output
        assert "--results" in result.output
        assert "--verbose" in result.output

    def test_validate_help(self, runner):
        """Test validate command help."""
        result = runner.invoke(app, ["validate", "--help"])
        assert result.exit_code == 0
        assert "validate" in result.output

    def test_search_missing_query(self, runner):
        """Test search command with missing query."""
        result = runner.invoke(app, ["search"])
        assert result.exit_code != 0
        assert "missing" in result.output.lower()

    def test_search_invalid_results_count(self, runner):
        """Test search command with invalid results count."""
        result = runner.invoke(app, ["search", "test query", "--results", "0"])
        assert result.exit_code != 0

        result = runner.invoke(app, ["search", "test query", "--results", "25"])
        assert result.exit_code != 0

    def test_search_valid_results_count(self, runner):
        """Test search command with valid results count."""
        # This would normally fail due to missing API keys, but we're testing argument parsing
        result = runner.invoke(app, ["search", "test query", "--results", "5"])
        # The command will fail due to missing API keys, but not due to invalid arguments
        assert "error:" in result.output.lower() or "no serper api key" in result.output.lower()

    def test_search_with_news_flag(self, runner):
        """Test search command with news flag."""
        result = runner.invoke(app, ["search", "test query", "--news"])
        # Will fail due to missing API keys but should parse arguments correctly
        assert "error:" in result.output.lower() or "no serper api key" in result.output.lower()

    def test_validate_command(self, runner):
        """Test validate command (may fail if Pipelex not properly configured)."""
        result = runner.invoke(app, ["validate"])
        # This might succeed or fail depending on configuration
        # We just verify the command runs
        assert result.exit_code in [0, 1]


@pytest.mark.inference
class TestCLIOutput:
    """Test CLI output formatting."""

    @pytest.fixture
    def runner(self):
        """CLI runner fixture."""
        return CliRunner()

    def test_cli_error_formatting(self, runner):
        """Test that CLI errors are properly formatted."""
        result = runner.invoke(app, ["search", "test"])
        assert result.exit_code != 0
        # Should contain some form of error message
        assert len(result.output.strip()) > 0

    def test_cli_argument_validation(self, runner):
        """Test CLI argument validation messages."""
        # Test negative results count
        result = runner.invoke(app, ["search", "test", "--results", "-1"])
        assert result.exit_code != 0

        # Test zero results count
        result = runner.invoke(app, ["search", "test", "--results", "0"])
        assert result.exit_code != 0

        # Test too many results
        result = runner.invoke(app, ["search", "test", "--results", "21"])
        assert result.exit_code != 0
