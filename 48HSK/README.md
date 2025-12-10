#  48h Survival Kit for the Agentic Era 

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Demonstration repository containing multiple projects related to artificial intelligence, natural language processing, and API management.

## 📋 Project Structure

This repository contains three main components:

### 🤖 AGENT - Sample AI Agent
AI agent based on **Microsoft Semantic Kernel** that integrates WSO2 API Manager as a gateway to access Shopify APIs. Allows managing Shopify stores using natural language with enterprise-grade security.

**Main features:**
- Microsoft Semantic Kernel integration
- Natural language interface (English and Spanish)
- WSO2 API Manager integration (OAuth2)
- Complete Shopify product management
- Anti-hallucination system (real data only)
- Price history and rollback

**Location:** `AGENT/SampleAIAgent/`

### 📚 RAG - Retrieval Augmented Generation
RAG (Retrieval Augmented Generation) system implemented in Python that combines local embedding models with LLM APIs to provide document-based answers.

**Main features:**
- Local embedding models (Mistral E5 Multilingual)
- Groq and OpenAI integration
- Document processing
- Semantic retrieval system
- Interactive and automatic demos

**Location:** `RAG/python-rag/`

### 🔌 MCP - Model Context Protocol Bridge
Bridge to connect OBS Studio with the Model Context Protocol (MCP), allowing OBS control through standard protocols.

**Main features:**
- OBS Studio integration
- Standard MCP protocol
- REST API for remote control
- Asynchronous command support

**Location:** `MCP/`

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js (for MCP component)
- Access to required APIs (OpenAI, Groq, WSO2, Shopify depending on component)

### Credentials Configuration

**⚠️ IMPORTANT: Credentials are stored in `.env` files that should NOT be uploaded to the repository.**

All `.env` files are protected by `.gitignore`. To configure each component:

1. **AGENT:**
   ```bash
   cd AGENT/SampleAIAgent/SampleAIAgent
   cp env.example .env
   # Edit .env with your credentials:
   # - WSO2_TOKEN_ENDPOINT
   # - WSO2_CONSUMER_KEY
   # - WSO2_CONSUMER_SECRET
   # - WSO2_GW_URL
   # - SHOPIFY_API_TOKEN
   # - OPENAI_API_KEY
   ```

2. **RAG:**
   ```bash
   cd RAG/python-rag
   # Create a .env file with:
   # - GROQ-TOKEN=your_groq_token
   # - OPENAI_API_KEY=your_openai_key
   ```

3. **MCP:**
   ```bash
   cd MCP
   # Configure OBS credentials in bridge.py or use environment variables
   ```

## 📖 Detailed Documentation

Each component has its own documentation:

- **AGENT:** See `AGENT/SampleAIAgent/SampleAIAgent/README.md`
- **RAG:** See `RAG/README.md` and `RAG/python-rag/README.md`
- **MCP:** See `MCP/README.md`

## 🔒 Security

### Credentials Management

- ✅ All `.env` files are in `.gitignore`
- ✅ `env.example` files contain templates without real credentials
- ✅ Never upload files with credentials to the repository
- ✅ Use environment variables for all sensitive configurations

### Protected Files

The `.gitignore` includes:
- `*.env` and `.env.*` - Environment variables
- `config.yaml` - Sensitive configuration files
- `venv/` and `.venv/` - Virtual environments
- `node_modules/` - Node.js dependencies
- `__pycache__/` - Python compiled files
- Copy and temporary files

## 🛠️ Installation by Component

### AGENT

```bash
cd AGENT/SampleAIAgent/SampleAIAgent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your credentials
./start_agent.sh
```

### RAG

```bash
cd RAG/python-rag
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env with your credentials
python demo_auto.py  # Automatic demo
python demo_interactiva.py  # Interactive demo
```

### MCP

```bash
cd MCP
npm install
# Configure OBS credentials
npm start
```

## 📝 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for more details.

## 🤝 Contributing

This is a demonstration repository. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Important Notes

- **Don't upload credentials:** All `.env` files must remain local
- **Use example files:** `env.example` files are safe templates
- **Virtual environments:** Each component has its own virtual environment
- **Dependencies:** Install dependencies for each component separately

## 📞 Support

For issues or questions about each component, consult the specific documentation in each directory.

---

**Developed as a demonstration of AI/ML technology integration with enterprise APIs.**
