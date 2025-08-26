#!/usr/bin/env python3
"""
Setup script for the Simple Web Agent

This script helps users set up the web search agent with proper environment configuration.
"""

import os
import shutil
from pathlib import Path

def setup_environment():
    """Set up environment configuration for the web search agent."""
    print("🚀 Simple Web Agent Setup")
    print("=" * 40)

    # Check if .env already exists
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled. Your existing .env file was preserved.")
            return

    # Copy env.example to .env
    example_file = Path("env.example")
    if not example_file.exists():
        print("❌ env.example file not found! Please make sure you're in the project root.")
        return

    shutil.copy(example_file, env_file)
    print("✅ Created .env file from env.example")

    # Guide user through configuration
    print("\n📝 Next steps:")
    print("1. Edit the .env file with your API keys:")
    print("   • SERPER_API_KEY (required) - Get from https://serper.dev")
    print("   • OPENAI_API_KEY (recommended) - Get from https://platform.openai.com")
    print("   • ANTHROPIC_API_KEY (optional) - Get from https://console.anthropic.com")
    print("   • MISTRAL_API_KEY (optional) - Get from https://console.mistral.ai")

    print("\n2. Install dependencies:")
    print("   uv sync  # if using uv")
    print("   # OR")
    print("   pip install -e .  # if using pip")

    print("\n3. Test the setup:")
    print("   python main.py 'What is AI?'")
    print("   # OR")
    print("   python -m simple_webagent.cli search 'What is AI?'")

    print("\n4. Validate configuration:")
    print("   python -m simple_webagent.cli validate")

    print("\n🎉 Setup complete! Don't forget to add your API keys to the .env file.")


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n🔍 Checking dependencies...")

    required_modules = [
        "pipelex",
        "httpx",
        "trafilatura",
        "dateutil",
        "limits",
        "gradio",
        "pydantic",
    ]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing_modules.append(module)

    if missing_modules:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_modules)}")
        print("Install with: uv sync  # or pip install -e .")
        return False

    print("\n✅ All dependencies are installed!")
    return True


if __name__ == "__main__":
    # Check current directory
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory.")
        exit(1)

    # Check dependencies first
    deps_ok = check_dependencies()

    # Set up environment
    setup_environment()

    if deps_ok:
        print("\n🚀 You can now start using the web search agent!")
    else:
        print("\n⚠️  Please install missing dependencies before using the agent.")
