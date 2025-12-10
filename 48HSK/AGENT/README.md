# Sample AI Agent v1.3 (Semantic Kernel + Shopify + WSO2)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Semantic Kernel](https://img.shields.io/badge/Semantic%20Kernel-Microsoft-purple.svg)](https://github.com/microsoft/semantic-kernel)
[![WSO2](https://img.shields.io/badge/WSO2-API%20Manager-orange.svg)](https://wso2.com)
[![Shopify](https://img.shields.io/badge/Shopify-API-brightgreen.svg)](https://shopify.dev)

A sample intelligent AI agent powered by **Microsoft Semantic Kernel** that integrates WSO2 API Manager as a gateway to access Shopify APIs. This agent provides natural language interactions for managing Shopify stores with enterprise-grade security and AI orchestration capabilities.

## Features

- **Microsoft Semantic Kernel Integration** - Advanced AI orchestration with plugin architecture
- **AI-Powered Natural Language Interface** - Interact with your Shopify store using plain English
- **WSO2 API Manager Integration** - Enterprise-grade API gateway with OAuth2 authentication
- **Complete Shopify Management** - List, search, count, and update products with real-time data
- **Smart Price Management** - Update prices by ID, name, or mathematical operations
- **Secure Credential Management** - Environment-based configuration with .gitignore protection
- **Real-time Progress Indicators** - Visual feedback for all operations
- **Anti-hallucination System** - Only returns real data from Shopify, never invents information
- **Bilingual Support** - Accepts commands in English and Spanish, responds in English
- **Price History & Rollback** - Remember previous prices and restore them when needed

## Prerequisites

- Python 3.8 or higher
- Microsoft Semantic Kernel (installed via pip)
- WSO2 API Manager instance
- Shopify store with API access
- OpenAI API key for AI functionality

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rgranadosd/WSO2.git
   cd "WSO2/Python IA Agent x Wso2"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your credentials
   ```

## Quick Start

```bash
# Start the agent
./start_agent.sh

# Or run directly
python agent_gpt4.py

# Debug mode
python agent_gpt4.py --debug
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Agent      │────│  WSO2 Gateway   │────│  Shopify API    │
│  (Semantic      │    │  (OAuth2 +      │    │  (Products,     │
│   Kernel)       │    │   Routing)      │    │   Pricing)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌────▼────┐             ┌────▼────┐             ┌────▼────┐
    │ OpenAI  │             │ WSO2 AM │             │ Shopify │
    │   API   │             │ Gateway │             │  Store  │
    └─────────┘             └─────────┘             └─────────┘
```

## Microsoft Semantic Kernel Integration

### What is Semantic Kernel?

**Microsoft Semantic Kernel** is an open-source SDK that lets you easily combine AI services like OpenAI, Azure OpenAI, and Hugging Face with conventional programming languages like C#, Python, and Java. It serves as an AI orchestration layer that enables developers to create AI agents that can reason over data and execute code.

### Key Semantic Kernel Concepts Used in This Project

#### Plugin Architecture
```python
@kernel_function(name="get_products_list", description="Gets product list with IDs")
def get_products_list(self) -> str:
    # Function automatically available to AI
```

Our project leverages Semantic Kernel's plugin system to expose Shopify operations as AI-callable functions:

- **`get_products_list()`** - Retrieve all products from Shopify
- **`count_products()`** - Get total product count
- **`update_product_price()`** - Modify product pricing
- **`find_product_by_name()`** - Search products by name with fuzzy matching
- **`update_product_price_with_math()`** - Perform mathematical price operations
- **`revert_price()`** - Restore previous pricing

#### AI Orchestration
```python
kernel = sk.Kernel()
kernel.add_service(OpenAIChatCompletion(service_id="openai", api_key=api_key))
kernel.add_plugin(shopify_plugin, plugin_name="Shopify")
```

Semantic Kernel orchestrates the interaction between:
- **Natural Language Processing** (OpenAI GPT models)
- **Function Calling** (Shopify API operations)
- **Context Management** (Chat history and state)

#### Chat History Management
```python
chat_history = ChatHistory()
chat_history.add_system_message(system_message)
chat_history.add_user_message(user_input)
chat_history.add_assistant_message(response_text)
```

Maintains conversation context for coherent multi-turn interactions.

### Why We Chose Semantic Kernel

#### Advantages for Our Ecommerce Agent

1. **Function Binding**: Automatically exposes Python functions to AI with decorators
2. **AI Orchestration**: Handles the complex flow between user intent and function execution
3. **Context Management**: Maintains conversation state and history
4. **Type Safety**: Strong typing and parameter validation for AI function calls
5. **Extensibility**: Easy to add new Shopify operations as plugins
6. **Prompt Engineering**: Built-in prompt templating and enhancement
7. **Multi-LLM Support**: Can switch between OpenAI, Azure OpenAI, or other providers

#### Our Implementation Pattern

```python
class ShopifyPlugin:
    @kernel_function(name="get_products_list", description="Gets product list")
    def get_products_list(self) -> str:
        # Real Shopify API call through WSO2
        data = self._make_api_call("GET", "/products.json")
        return formatted_product_list

# Register plugin with kernel
kernel.add_plugin(shopify_plugin, plugin_name="Shopify")

# AI automatically decides when to call functions
response = await kernel.invoke_prompt(user_input)
```

#### Benefits in Our Use Case

- **Natural Language to API Calls**: User says "list products" and Semantic Kernel calls `get_products_list()`
- **Context Awareness**: Remembers previous operations and price changes
- **Error Handling**: Gracefully manages API failures and provides meaningful feedback
- **Function Composition**: Can chain multiple operations (search, update, verify)
- **Intent Recognition**: Understands various ways to express the same request

### Semantic Kernel vs Traditional Approaches

| Traditional Chatbot | **Our Semantic Kernel Agent** |
|-------------------|----------------------------|
| Hardcoded responses | Dynamic function calling |
| Limited context | Full conversation history |
| Manual intent parsing | AI-driven intent recognition |
| Static workflows | Flexible AI orchestration |
| Single-turn interactions | Multi-turn conversations |
| Generic responses | Real-time data integration |

### Learn More About Semantic Kernel

- **Official Repository**: [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel)
- **Documentation**: [Semantic Kernel Docs](https://learn.microsoft.com/en-us/semantic-kernel/)
- **Python Samples**: [SK Python Examples](https://github.com/microsoft/semantic-kernel/tree/main/python)

## Project Structure

```
├── agent_gpt4.py              # Main AI agent script
├── start_agent.sh             # Startup script (executable)
├── test.sh                    # Comprehensive test suite
├── check_credential.sh        # WSO2 credential verification
├── env.example                # Environment variables template
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create from template)
├── LICENSE                    # Apache 2.0 License
└── README.md                  # This file
```

## Configuration

### WSO2 API Manager Setup

1. **Create Application in WSO2**
   - Access WSO2 API Manager Developer Portal
   - Create a new application
   - Generate Consumer Key and Consumer Secret
   - Subscribe to the Shopify API

2. **API Configuration**
   - Create API with context: `/shopify/1.0.0`
   - Configure backend endpoint to point to Shopify
   - Set up proper authentication headers
   - Deploy and publish the API

### Shopify Configuration

1. **Generate Private App Token**
   - Go to Shopify Admin → Apps → App and sales channel settings
   - Create a private app or custom app
   - Generate Admin API access token
   - Configure required permissions:
     - `read_products`
     - `write_products`
     - `read_product_listings`

## Advanced Features

### Debug Mode
Enable detailed logging and diagnostic information:
```bash
python agent_gpt4.py --debug
```

### Price Memory System
The agent automatically remembers price changes for rollback functionality:
- Tracks previous prices for all updated products
- Allows reverting to original prices
- Maintains session-based price history

### Anti-Hallucination System
- **Real Data Only**: Never invents product information
- **Error Transparency**: Clearly reports WSO2 Gateway issues
- **Exact Matching**: Uses actual Shopify product IDs and names
- **Verification**: Confirms all price updates with response validation

## Security

- **Environment Variables**: All credentials stored in `.env` file
- **Git Protection**: `.gitignore` prevents credential exposure
- **OAuth2 Flow**: Secure token-based authentication with WSO2
- **HTTPS**: All API communications use encrypted connections
- **Token Rotation**: WSO2 handles automatic token refresh

## Troubleshooting

### Common Issues

**WSO2 Gateway 404 Error**
```
Solution: Verify API context is configured as /shopify/1.0.0 in WSO2
```

**Shopify Authentication Failed**
```
Solution: Check SHOPIFY_API_TOKEN and store URL in .env file
```

**OpenAI API Key Invalid**
```
Solution: Generate new API key from https://platform.openai.com/account/api-keys
```

**Environment Variables Not Loading**
```
Solution: Ensure .env file exists and contains all required variables
```

### Debug Commands

```bash
# Test all connections
./test.sh

# Check WSO2 specifically
./check_credential.sh

# Run with debug logging
python agent_gpt4.py --debug
```

### Our Implementation

```python
@kernel_function(name="get_products_list", description="Gets product list")
def get_products_list(self) -> str:
    # Function automatically available to AI
    data = self._make_api_call("GET", "/products.json")
    return formatted_product_list
```

### Benefits
- **Function Binding**: Automatic Python function exposure to AI
- **AI Orchestration**: Complex user intent to function execution flow
- **Context Management**: Conversation state and history
- **Type Safety**: Parameter validation for AI function calls
- **Multi-LLM Support**: OpenAI, Azure OpenAI, or other providers

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**Made with care for intelligent ecommerce management**
