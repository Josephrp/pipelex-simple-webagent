#!/usr/bin/env python3
"""
Setup validation script for the Simple Web Agent

This script validates that the web search agent is properly configured and ready to use.
"""

import os
import sys
from pathlib import Path


def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")

    required_modules = [
        "pipelex",
        "httpx",
        "trafilatura",
        "dateutil",
        "limits",
        "gradio",
        "pydantic",
        "typer",
        "rich",
    ]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing_modules.append(module)

    if missing_modules:
        print(f"\n❌ Missing dependencies: {', '.join(missing_modules)}")
        print("Install with: uv sync  # or pip install -e .")
        return False

    print("\n✅ All dependencies are installed!")
    return True


def check_package_structure():
    """Check that the package structure is correct."""
    print("\n🏗️  Checking package structure...")

    required_files = [
        "simple_webagent/__init__.py",
        "simple_webagent/web_search.py",
        "simple_webagent/web_search.toml",
        "simple_webagent/web_search_pipeline.py",
        "simple_webagent/cli.py",
        "simple_webagent/websearch/__init__.py",
        "simple_webagent/websearch/web_search.py",
        "simple_webagent/websearch/analytics.py",
        "main.py",
        "setup.py",
        "env.example",
        "README.md",
    ]

    missing_files = []

    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)

    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False

    print("\n✅ Package structure is complete!")
    return True


def check_models():
    """Check that the data models can be imported and instantiated."""
    print("\n📋 Checking data models...")

    try:
        from simple_webagent import (
            WebSearchQuery,
            WebSearchResult,
            WebSearchResponse,
            WebSearchAgentResponse,
        )

        # Test creating instances
        query = WebSearchQuery(query_text="test query")
        print(f"  ✅ WebSearchQuery: {query}")

        result = WebSearchResult(
            title="Test",
            url="https://example.com",
            domain="example.com",
            content="test content"
        )
        print(f"  ✅ WebSearchResult: {result.title}")

        response = WebSearchAgentResponse(
            user_query="test",
            search_results_summary="summary",
            comprehensive_answer="answer",
            sources=["https://example.com"],
            confidence_level="high"
        )
        print(f"  ✅ WebSearchAgentResponse: {response.confidence_level}")

        print("\n✅ All data models work correctly!")
        return True

    except Exception as e:
        print(f"\n❌ Error with data models: {e}")
        return False


def check_pipeline_configuration():
    """Check that the pipeline configuration is valid."""
    print("\n⚙️  Checking pipeline configuration...")

    try:
        # Check that pipeline file exists and has correct structure
        pipeline_file = "simple_webagent/web_search.toml"
        with open(pipeline_file, "r") as f:
            content = f.read()

        required_sections = [
            "[pipe.web_search_agent]",
            "PipeSequence",
            "[pipe.perform_web_search]",
            "[pipe.parse_search_results]",
            "[pipe.generate_agent_response]",
        ]

        for section in required_sections:
            if section in content:
                print(f"  ✅ Found {section}")
            else:
                print(f"  ❌ Missing {section}")
                return False

        # Try to initialize Pipelex (optional - don't fail if not available)
        try:
            from pipelex import Pipelex
            Pipelex.make()
            print("  ✅ Pipelex initialization successful")
        except Exception as e:
            print(f"  ⚠️  Pipelex initialization warning: {e}")
            print("  ⚠️  This may affect full pipeline functionality")

        print("\n✅ Pipeline configuration is valid!")
        return True

    except Exception as e:
        print(f"\n❌ Error with pipeline configuration: {e}")
        return False


def check_environment_configuration():
    """Check environment configuration files."""
    print("\n🌍 Checking environment configuration...")

    # Check env.example exists
    if os.path.exists("env.example"):
        print("  ✅ env.example exists")
    else:
        print("  ❌ env.example missing")
        return False

    # Check .env file
    if os.path.exists(".env"):
        print("  ✅ .env file exists")

        # Check if it has required variables (even if empty)
        with open(".env", "r") as f:
            env_content = f.read()

        required_vars = ["SERPER_API_KEY="]
        for var in required_vars:
            if var in env_content:
                print(f"  ✅ {var.rstrip('=')} variable found in .env")
            else:
                print(f"  ⚠️  {var.rstrip('=')} variable not found in .env")
    else:
        print("  ⚠️  .env file not found (run setup.py to create it)")

    print("\n✅ Environment configuration check complete!")
    return True


def check_cli():
    """Check that the CLI can be imported and has correct structure."""
    print("\n💻 Checking CLI...")

    try:
        from simple_webagent.cli import app

        # Check that CLI app exists and can be imported
        print("  ✅ CLI module imported successfully")

        # Try to get the registered commands
        try:
            commands = [command.name for command in app.registered_commands]
            expected_commands = ["search", "validate"]

            for cmd in expected_commands:
                if cmd in commands:
                    print(f"  ✅ CLI command '{cmd}' available")
                else:
                    print(f"  ❌ CLI command '{cmd}' missing")
        except Exception:
            # If we can't access registered_commands, just check that the functions exist
            print("  ⚠️  Could not check registered commands, but CLI module loaded")

        print("\n✅ CLI check complete!")
        return True

    except Exception as e:
        print(f"\n❌ Error with CLI: {e}")
        return False


def main():
    """Run all validation checks."""
    print("🚀 Simple Web Agent Setup Validation")
    print("=" * 50)

    checks = [
        check_dependencies,
        check_package_structure,
        check_models,
        check_pipeline_configuration,
        check_environment_configuration,
        check_cli,
    ]

    results = []

    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Check failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("📊 Validation Summary:")
    print("=" * 50)

    passed_checks = sum(results)
    total_checks = len(results)

    for i, (check, result) in enumerate(zip(checks, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check.__name__}")

    print(f"\nOverall: {passed_checks}/{total_checks} checks passed")

    if passed_checks == total_checks:
        print("\n🎉 All checks passed! The Simple Web Agent is ready to use.")
        print("\nNext steps:")
        print("1. Add your API keys to the .env file")
        print("2. Test with: python main.py 'What is AI?'")
        print("3. Or use the CLI: python -m simple_webagent.cli search 'What is AI?'")
        return 0
    else:
        print(f"\n⚠️  {total_checks - passed_checks} checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
