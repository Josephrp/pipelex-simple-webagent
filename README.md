# Simple Web Agent 🤖

*A intelligent web search agent built with Pipelex that performs web searches and generates comprehensive responses incorporating the top search results.*

## 🌟 Features

- **Intelligent Query Optimization**: Automatically converts user questions into effective web search queries
- **Top Results Focus**: Retrieves and analyzes the most relevant search results (configurable 1-20 results)
- **Structured Output**: Returns well-organized responses with sources and confidence levels
- **Multiple Search Types**: Supports both general web search and news-specific search
- **Error Handling**: Graceful handling of API failures and rate limits
- **Source Attribution**: Always cites sources used in the response
- **Rich CLI Interface**: Beautiful command-line interface with rich formatting
- **Programmatic API**: Easy-to-use Python API for integration

## 🚀 Quick Start


🌟 Star This Repository - then 👇🏻

### 1. Clone and Setup

```bash
git clone https://github.com/Josephrp/pipelex-simple-webagent
cd pipelex-simple-webagent

# Run the setup script to configure environment
python setup.py
```

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 3. Configure API Keys

Edit the `.env` file with your API keys:

```bash
# Required: Serper API for web search
SERPER_API_KEY=your_serper_api_key_here

# Required: At least one LLM provider
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# OR
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 4. Get API Keys

- **Serper API**: Sign up at [serper.dev](https://serper.dev) for web search functionality
- **OpenAI**: Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Anthropic**: Get API key from [Anthropic Console](https://console.anthropic.com/)
- **Mistral**: Get API key from [Mistral AI Platform](https://console.mistral.ai/)

### 5. Test the Agent

```bash
# Simple command-line usage
python main.py "What are the latest developments in artificial intelligence?"

# Using the rich CLI
python -m simple_webagent.cli search "What is AI?" --results 5 --verbose

# Search for news
python -m simple_webagent.cli search "Latest climate change news" --news
```

---

## 📖 Usage Guide

### Command Line Interface

The Simple Web Agent provides a rich command-line interface with multiple options:

```bash
# Basic search
python -m simple_webagent.cli search "What is machine learning?"

# News search
python -m simple_webagent.cli search "Latest AI news" --news

# Configure number of results
python -m simple_webagent.cli search "Python tutorials" --results 5

# Verbose output with performance metrics
python -m simple_webagent.cli search "Climate change impacts" --verbose

# Validate setup
python -m simple_webagent.cli validate
```

### Programmatic API

Use the Simple Web Agent in your Python code:

```python
import asyncio
from simple_webagent import WebSearchAgentResponse
from main import search_and_answer, search_and_answer_sync

# Asynchronous usage
async def main():
    response = await search_and_answer(
        "What are the benefits of renewable energy?",
        search_type="search",
        num_results=3
    )

    print(f"Query: {response.user_query}")
    print(f"Answer: {response.comprehensive_answer}")
    print(f"Confidence: {response.confidence_level}")
    print(f"Sources: {response.sources}")

# Synchronous usage (easier for scripts)
response = search_and_answer_sync("Latest developments in quantum computing")
print(response.comprehensive_answer)
```

### Python Integration Example

```python
from simple_webagent import WebSearchAgentResponse
from pipelex import Pipelex
from pipelex.pipeline.execute import execute_pipeline

# Initialize once
Pipelex.make()

async def search_helper(query: str) -> WebSearchAgentResponse:
    """Helper function for easy web search integration"""
    pipe_output = await execute_pipeline(
        pipe_code="web_search_agent",
        input_memory={"user_query": query}
    )
    return pipe_output.main_stuff_as(content_type=WebSearchAgentResponse)

# Use in your application
result = asyncio.run(search_helper("What is the weather today?"))
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SERPER_API_KEY` | Primary Serper API key for web search | Yes |
| `SERPER_API_KEY_FALLBACK` | Fallback Serper API key | No |
| `OPENAI_API_KEY` | OpenAI API key for LLM operations | Yes* |
| `ANTHROPIC_API_KEY` | Anthropic API key (alternative to OpenAI) | No |
| `MISTRAL_API_KEY` | Mistral API key (alternative to OpenAI) | No |
| `ANALYTICS_DATA_DIR` | Directory for analytics data | No |

*At least one LLM API key is required (OpenAI, Anthropic, or Mistral)

### Search Configuration

- **Search Types**: `search` (general web) or `news` (recent news)
- **Result Count**: 1-20 results (default: 3)
- **Rate Limiting**: 360 requests per hour (built-in protection)

## 🏗️ Architecture

The Simple Web Agent consists of several key components:

### Pipeline Structure

1. **Query Optimization** (`create_search_query`): Converts user questions into effective search queries
2. **Web Search** (`perform_web_search`): Executes web searches using the Serper API
3. **Result Parsing** (`parse_search_results`): Extracts and structures information from search results
4. **Response Generation** (`generate_agent_response`): Creates comprehensive answers incorporating search results

### Data Models

- `WebSearchQuery`: Search configuration and parameters
- `WebSearchResult`: Individual search result with metadata
- `WebSearchResponse`: Structured search response with analysis
- `WebSearchAgentResponse`: Final comprehensive response

### Key Features

- **Intelligent Content Extraction**: Uses Trafilatura for robust HTML content extraction
- **Rate Limiting**: Built-in protection against API rate limits
- **Fallback Support**: Automatic fallback to secondary API keys
- **Analytics**: Request tracking and performance metrics
- **Error Handling**: Comprehensive error handling and recovery

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
make test

# Run inference tests (requires API keys)
make test-inference

# Run with prints for debugging
make test-with-prints

# Run specific test file
pytest tests/ -k "test_web_search" -v
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing API Keys**
   ```
   Error: No SERPER API key configured
   ```
   Solution: Set `SERPER_API_KEY` in your `.env` file

2. **Rate Limit Exceeded**
   ```
   Error: Rate limit exceeded. Please try again later
   ```
   Solution: Wait before making more requests (limit: 360/hour)

3. **No Search Results**
   ```
   No search results found for query
   ```
   Solution: Try different keywords or check API key validity

4. **LLM API Errors**
   ```
   Error: Invalid API key for LLM provider
   ```
   Solution: Verify your OpenAI/Anthropic/Mistral API key

### Validation

Validate your setup:

```bash
# Validate pipeline configuration
python -m pipelex.cli._cli validate

# Check dependencies
python setup.py
```

### Performance Tuning

- Reduce `num_results` for faster responses
- Use `search` type for general queries, `news` for time-sensitive topics
- Monitor rate limits and implement backoff strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `make test`
6. Submit a pull request

### Development Setup

```bash
# Install development dependencies
uv sync --dev

# Run linting and type checking
make check

# Format code
make format
```

## 📊 Analytics

The agent includes built-in analytics to track usage:

- Request counts per day
- Response time metrics
- Success/failure rates

Analytics data is stored in `./data/` by default (configurable via `ANALYTICS_DATA_DIR`).

## 📝 License

This project is licensed under the [MIT license](LICENSE). Runtime dependencies are distributed under their own licenses via PyPI.

---

## Contact & Support

| Channel                                | Use case                                                                  |
| -------------------------------------- | ------------------------------------------------------------------------- |
| **GitHub Discussions → "Show & Tell"** | Share ideas, brainstorm, get early feedback.                              |
| **GitHub Issues**                      | Report bugs or request features.                                          |
| **Email (privacy & security)**         | [security@pipelex.com](mailto:security@pipelex.com)                       |
| **Discord**                            | Real-time chat — [https://go.pipelex.com/discord](https://go.pipelex.com/discord) |

---

*Happy searching!* 🔍✨
