#!/usr/bin/env python3
"""
Main entry point for the Simple Web Agent

This module provides both programmatic and CLI interfaces for the web search agent.
"""

import asyncio
import sys
from typing import Optional

from pipelex import pretty_print
from pipelex.hub import get_pipeline_tracker, get_report_delegate
from pipelex.pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline
from simple_webagent import WebSearchAgentResponse


async def search_and_answer(
    user_query: str,
    search_type: str = "search",
    num_results: int = 3,
) -> WebSearchAgentResponse:
    """
    Perform a web search and generate a comprehensive answer.

    Args:
        user_query: The user's question or query
        search_type: Type of search ("search" or "news")
        num_results: Number of search results to retrieve

    Returns:
        WebSearchAgentResponse: Comprehensive response with search results and analysis

    Example:
        >>> response = await search_and_answer("What is AI?")
        >>> print(response.comprehensive_answer)
    """
    # Initialize Pipelex if not already done
    Pipelex.make()

    # Run the web search agent pipeline
    pipe_output = await execute_pipeline(
        pipe_code="web_search_agent",
        input_memory={
            "user_query": user_query,
        },
    )

    # Return the structured response
    return pipe_output.main_stuff_as(content_type=WebSearchAgentResponse)


def search_and_answer_sync(
    user_query: str,
    search_type: str = "search",
    num_results: int = 3,
) -> WebSearchAgentResponse:
    """
    Synchronous version of search_and_answer for easier use in scripts.

    Args:
        user_query: The user's question or query
        search_type: Type of search ("search" or "news")
        num_results: Number of search results to retrieve

    Returns:
        WebSearchAgentResponse: Comprehensive response with search results and analysis
    """
    return asyncio.run(search_and_answer(user_query, search_type, num_results))


def main():
    """CLI entry point for the web search agent."""
    if len(sys.argv) < 2:
        print("Usage: python main.py 'your search query' [--news] [--results N]")
        print("\nExamples:")
        print("  python main.py 'What is artificial intelligence?'")
        print("  python main.py 'Latest news about climate change' --news")
        print("  python main.py 'Python tutorials' --results 5")
        sys.exit(1)

    query = sys.argv[1]

    # Parse optional arguments
    search_type = "search"
    num_results = 3

    if "--news" in sys.argv:
        search_type = "news"
        sys.argv.remove("--news")

    if "--results" in sys.argv:
        try:
            results_idx = sys.argv.index("--results")
            if results_idx + 1 < len(sys.argv):
                num_results = int(sys.argv[results_idx + 1])
                sys.argv.pop(results_idx + 1)
                sys.argv.pop(results_idx)
        except (ValueError, IndexError):
            print("Error: --results requires a number")
            sys.exit(1)

    print(f"🔍 Searching for: '{query}'")
    print(f"   Search type: {search_type}")
    print(f"   Number of results: {num_results}")
    print("-" * 60)

    try:
        # Perform the search
        response = search_and_answer_sync(query, search_type, num_results)

        # Display results
        print("✅ Search completed successfully!")
        print(f"Confidence Level: {response.confidence_level}")
        print(f"Number of Sources: {len(response.sources)}")
        print()

        # Display the comprehensive answer
        print("📝 Comprehensive Answer:")
        print("=" * 40)
        print(response.comprehensive_answer)
        print()

        # Display sources
        if response.sources:
            print("🔗 Sources:")
            print("=" * 40)
            for i, source in enumerate(response.sources, 1):
                print(f"{i}. {source}")
            print()

        # Display search summary
        if response.search_results_summary:
            print("📊 Search Summary:")
            print("=" * 40)
            print(response.search_results_summary)
            print()

        # Display cost and performance info
        get_report_delegate().generate_report()
        get_pipeline_tracker().output_flowchart()

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Set up your environment variables (see env.example)")
        print("2. Installed dependencies: pip install -e .")
        print("3. Valid API keys for Serper and at least one LLM provider")
        sys.exit(1)


if __name__ == "__main__":
    main()
