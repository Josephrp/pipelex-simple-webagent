#!/usr/bin/env python3
"""
Command Line Interface for the Simple Web Agent
"""

import asyncio
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Pipelex imports are done conditionally to handle import errors gracefully
from . import WebSearchAgentResponse

app = typer.Typer(
    name="simple-webagent",
    help="A simple web search agent built with Pipelex",
    add_completion=False,
)
console = Console()


@app.command()
def search(
    query: str = typer.Argument(..., help="The search query or question"),
    news: bool = typer.Option(False, "--news", help="Search for news instead of general web results"),
    results: int = typer.Option(3, "--results", "-n", help="Number of search results to retrieve (1-20)", min=1, max=20),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output including pipeline flow"),
):
    """
    Perform a web search and get comprehensive answers.

    Examples:
        simple-webagent search "What is artificial intelligence?"
        simple-webagent search "Latest climate change news" --news
        simple-webagent search "Python tutorials" --results 5 --verbose
    """
    # Try to initialize Pipelex
    try:
        from pipelex import Pipelex
        Pipelex.make()
    except Exception as e:
        console.print(f"[yellow]⚠️  Warning: Could not initialize Pipelex: {e}[/yellow]")
        console.print("[yellow]Some features may not work correctly.[/yellow]")

    search_type = "news" if news else "search"

    # Show search info
    console.print(f"\n[bold blue]🔍 Searching for:[/bold blue] '{query}'")
    console.print(f"[dim]Search type: {search_type} | Results: {results}[/dim]\n")

    try:
        # Perform the search
        response = asyncio.run(_perform_search(query, search_type, results))

        # Display results
        _display_results(response, verbose)

        if verbose:
            try:
                # Show cost and performance info
                console.print("\n[bold green]📊 Performance Report:[/bold green]")
                from pipelex.hub import get_report_delegate, get_pipeline_tracker
                get_report_delegate().generate_report()
                get_pipeline_tracker().output_flowchart()
            except Exception:
                console.print("[dim]Performance reporting not available[/dim]")

    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        console.print("\n[dim]Make sure you have:[/dim]")
        console.print("1. Set up your environment variables (see env.example)")
        console.print("2. Installed dependencies: pip install -e .")
        console.print("3. Valid API keys for Serper and at least one LLM provider")
        raise typer.Exit(1)


@app.command()
def validate():
    """Validate the web search agent setup and configuration."""
    console.print("[bold blue]🔧 Validating setup...[/bold blue]")

    try:
        # Basic validation - check if we can import and initialize components
        from simple_webagent import WebSearchAgentResponse, WebSearchQuery
        from simple_webagent.websearch.web_search import search_web

        # Try to create a test query
        test_query = WebSearchQuery(query_text="test")
        console.print("[green]✅ Data models work correctly[/green]")

        # Check if web search module can be imported
        console.print("[green]✅ Web search module imported successfully[/green]")

        console.print("[bold green]✅ Basic validation successful![/bold green]")
        console.print("[dim]The web search agent components are properly configured.[/dim]")
        console.print("[dim]Note: Full pipeline validation requires API keys.[/dim]")

    except Exception as e:
        console.print(f"[bold red]❌ Validation failed:[/bold red] {e}")
        console.print("\n[dim]Please check your configuration and try again.[/dim]")
        raise typer.Exit(1)


async def _perform_search(query: str, search_type: str, num_results: int) -> WebSearchAgentResponse:
    """Perform the actual web search."""
    try:
        from pipelex.pipeline.execute import execute_pipeline

        pipe_output = await execute_pipeline(
            pipe_code="web_search_agent",
            input_memory={
                "user_query": query,
            },
        )

        return pipe_output.main_stuff_as(content_type=WebSearchAgentResponse)
    except Exception as e:
        # Fallback: create a mock response for testing
        return WebSearchAgentResponse(
            user_query=query,
            search_results_summary="Pipeline execution failed - check API keys and configuration",
            comprehensive_answer=f"Error: {str(e)}",
            sources=[],
            confidence_level="low"
        )


def _display_results(response: WebSearchAgentResponse, verbose: bool = False):
    """Display the search results in a formatted way."""

    # Main answer panel
    answer_panel = Panel(
        response.comprehensive_answer,
        title="📝 Comprehensive Answer",
        border_style="green",
        padding=(1, 2),
    )
    console.print(answer_panel)

    # Confidence and sources info
    info_text = f"🎯 Confidence: [bold]{response.confidence_level}[/bold] | 🔗 Sources: {len(response.sources)}"
    console.print(f"\n[dim]{info_text}[/dim]")

    # Sources panel
    if response.sources:
        sources_text = "\n".join(f"{i+1}. {source}" for i, source in enumerate(response.sources))
        sources_panel = Panel(
            sources_text,
            title="🔗 Sources",
            border_style="blue",
            padding=(1, 2),
        )
        console.print(sources_panel)

    # Search summary (if verbose)
    if verbose and response.search_results_summary:
        summary_panel = Panel(
            response.search_results_summary,
            title="📊 Search Summary",
            border_style="yellow",
            padding=(1, 2),
        )
        console.print(summary_panel)


@app.callback()
def callback():
    """Simple Web Agent - Intelligent web search powered by Pipelex."""
    pass


if __name__ == "__main__":
    app()
