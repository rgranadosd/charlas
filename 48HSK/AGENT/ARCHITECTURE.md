# Architectural Document: AI Agent for Ecommerce with WSO2

## System Overview

This document describes the complete architecture of the **Sample AI Agent** that integrates Microsoft Semantic Kernel, WSO2 API Manager, and Shopify API to provide a natural language interface for managing ecommerce stores.

---

## System Components

### 1. **User/Client**
- **Role**: End-user interface
- **Responsibility**: Send queries in natural language (Spanish/English)
- **Query Examples**:
  - "List the products"
  - "Update the price of product ID 123456 to 99.99"
  - "How many products are there?"
  - "Show products sorted from lowest to highest price"

### 2. **Python Agent (agent_gpt4.py)**
- **Role**: Main orchestrator and entry point
- **Technology**: Python 3.8+
- **Responsibilities**:
  - Receive and process user input
  - Manage application lifecycle
  - Coordinate between Semantic Kernel and plugins
  - Handle conversation history
  - Provide visual progress indicators
  - Price memory system (PriceMemory)
  - Enhanced intent detection (bilingual)

#### Key Components of the Python Agent:

##### 1. **Intent Detection**

**What does it do?**
Analyzes user text to automatically identify what action they want to perform, before Semantic Kernel processes the query.

**How it works:**
- Uses keyword dictionaries in Spanish and English
- Detects patterns using regular expressions (regex)
- Identifies multiple ways to express the same intention
- Automatically extracts parameters (IDs, prices, product names)

**Detection Examples:**

```python
# Intent: LIST PRODUCTS
Keywords detected: ['productos', 'lista', 'catálogo', 'mostrar', 'ver', 
                   'products', 'list', 'catalog', 'show', 'display']
User says: "Lista los productos" → Detects: 'list'
User says: "Muéstrame el catálogo" → Detects: 'list'
User says: "Show products" → Detects: 'list'

# Intent: UPDATE PRICE
Keywords detected: ['actualizar', 'cambiar', 'modificar', 'update', 
                   'change', 'modify', 'set']
Price patterns: r'a\s+[\$€]?\d+', r'precio\s+[\$€]?\d+', r'to\s+[\$€]?\d+'
User says: "Actualiza precio ID 123456 a 99.99" 
→ Detects: 'update_price', extracts: ID=123456, price=99.99

User says: "Cambia el precio de Gift Card a 200"
→ Detects: 'update_price', extracts: name="Gift Card", price=200

# Intent: MATHEMATICAL OPERATIONS
Keywords: ['añadir', 'sumar', 'restar', 'aumentar', 'incrementar', 
          'add', 'subtract', 'increase']
User says: "Añade 1000 al precio de X"
→ Detects: 'update_price', operation='add', value=1000

User says: "Incrementa un 10% el precio"
→ Detects: 'update_price', operation='percent_increase', value=10
```

**Advantages:**
- **Bilingual**: Works in Spanish and English
- **Flexible**: Understands multiple ways to express the same thing
- **Precise**: Automatically extracts parameters using regex
- **Fast**: Processes before sending to Semantic Kernel, optimizing the flow

##### 2. **PriceMemory (Price Memory)**

**What does it do?**
Memory system that stores the history of price changes for each product, allowing to revert changes and maintain a record of modifications.

**How it works:**
- When updating a price, automatically saves the previous and new price
- Maintains an in-memory dictionary: `{product_id: {previous: old_price, current: current_price}}`
- Allows querying the previous price of any product
- Allows reverting changes by restoring the previous price

**Practical Example:**

```python
# User updates price
User: "Actualiza precio ID 123456 a 99.99"
System executes: update_product_price("123456", "99.99")

# PriceMemory automatically saves:
price_history = {
    "123456": {
        "previous": "150.00",  # Previous price
        "current": "99.99"      # New price
    }
}

# Later, user wants to revert
User: "Vuelve el precio original del ID 123456"
System queries PriceMemory:
→ get_previous_price("123456") returns "150.00"
→ Executes: update_product_price("123456", "150.00")
→ Response: "Price restored to $150.00"
```

**Available Operations:**
- `remember_price_change(id, old_price, new_price)`: Saves a change
- `get_previous_price(id)`: Gets the previous price
- `has_history(id)`: Checks if there's history for a product
- `revert_price(id)`: Restores the previous price

**Advantages:**
- **Change history**: Maintains record of all modifications
- **Easy reversion**: Allows undoing changes with a simple command
- **Persistent session**: History is maintained throughout the session
- **No database**: In-memory storage (fast and simple)

##### 3. **ThinkingIndicator (Progress Indicator)**

**What does it do?**
Shows an animated visual indicator ("Thinking...") while the system processes the user's query, improving user experience.

**How it works:**
- Automatically activates when processing begins
- Shows an animation of dots: "Thinking...", "Thinking....", "Thinking.....", etc.
- Runs in a separate thread (doesn't block processing)
- Automatically stops when the response is ready

**Visual Example:**

```
User: "Lista los productos"
         │
         ▼
System shows: "Thinking..." (with animated dots)
         │
         ▼
[Processing query...]
[Getting data from Shopify...]
[Generating response...]
         │
         ▼
System hides: "Thinking..."
         │
         ▼
Response: "Products found (5 total):
           - ID: 123456 - Gift Card - $150.00
           - ID: 789012 - Snowboard - $500.00
           ..."
```

**Features:**
- **Smooth animation**: Dots that appear and disappear cyclically
- **Non-intrusive**: Only shows when necessary (not in debug mode)
- **Auto-cleanup**: Cleans the line when finished
- **Thread-safe**: Doesn't interfere with main processing

**Example Code:**

```python
# At the start of processing
thinking = ThinkingIndicator("Processing query")
thinking.start()  # Shows "Processing query..."

# ... processing ...

# When finished
thinking.stop()  # Hides indicator and cleans the line
print("Response: ...")
```

**Advantages:**
- **Better UX**: User knows the system is working
- **Visual feedback**: Prevents user from thinking the system "froze"
- **Professional**: Gives feeling of active and responsive system
- **Configurable**: Can be disabled in debug mode to see technical details

### 3. **Microsoft Semantic Kernel**
- **Role**: AI orchestration framework
- **Technology**: Microsoft Semantic Kernel SDK (Python)
- **Responsibilities**:
  - Connect the LLM with executable functions
  - Manage conversation context (ChatHistory)
  - Route user intentions to appropriate functions
  - Provide extensible plugin system
  - Handle LLM prompts and responses
  - Validate and execute functions decorated with `@kernel_function`

#### What is Semantic Kernel and what is it for?

**Microsoft Semantic Kernel** is an open-source framework developed by Microsoft that allows creating AI agents capable of combining the power of natural language processing (LLM) with executable functions written in traditional code (Python, C#, Java, etc.).

**Problem it solves:**
- LLMs like ChatGPT are excellent at understanding natural language, but cannot execute code directly
- You need a way to connect user intentions (expressed in natural language) with real actions (API calls, database operations, etc.)
- Semantic Kernel acts as the "bridge" between natural language and executable functions

**Main Features:**

1. **Function Calling**: Allows the LLM to decide when and how to call Python functions
2. **Plugin System**: Organizes related functions into reusable plugins
3. **Context Management**: Maintains conversation history for coherent context
4. **Prompt Engineering**: Facilitates building and improving prompts for the LLM
5. **Multi-LLM Support**: Can work with OpenAI, Azure OpenAI, or other providers

#### Practical Example in Our Project:

**Scenario:** User says: *"Update the price of product Gift Card to 200 dollars"*

**Without Semantic Kernel (traditional approach):**
```python
# You would have to do manual parsing:
if "actualiza" in user_input and "precio" in user_input:
    # Manually extract product name
    # Manually extract price
    # Search for product
    # Update price
    # Format response
```

**With Semantic Kernel:**

**Step 1:** We define functions as plugins:
```python
class ShopifyPlugin:
    @kernel_function(name="update_product_price_by_name", 
                     description="Updates the price of a product using its name")
    def update_product_price_by_name(self, product_name: str, new_price: str) -> str:
        # This function is automatically executed when the LLM needs it
        search_result = self.find_product_by_name(product_name)
        if search_result['found']:
            return self.update_product_price(search_result['id'], new_price)
        return f"Error: Product '{product_name}' not found"
```

**Step 2:** We register the plugin with Semantic Kernel:
```python
kernel = sk.Kernel()
kernel.add_service(OpenAIChatCompletion(...))  # Connects OpenAI
kernel.add_plugin(shopify_plugin, plugin_name="Shopify")  # Registers functions
```

**Step 3:** The LLM automatically decides what to do:
```python
# User: "Update the price of product Gift Card to 200 dollars"

# Semantic Kernel automatically:
# 1. LLM analyzes the intention
# 2. LLM decides it needs to call update_product_price_by_name()
# 3. LLM extracts parameters: product_name="Gift Card", new_price="200"
# 4. Semantic Kernel executes the function
# 5. LLM receives the result and generates a natural response
```

**Complete Flow:**

```
User: "Actualiza precio de Gift Card a 200"
    │
    ▼
Semantic Kernel receives the message
    │
    ▼
LLM (OpenAI) analyzes: "I need to update a price"
    │
    ▼
LLM decides: "I must call update_product_price_by_name()"
    │
    ▼
LLM extracts parameters: product_name="Gift Card", new_price="200"
    │
    ▼
Semantic Kernel executes: shopify_plugin.update_product_price_by_name("Gift Card", "200")
    │
    ▼
Function searches for product and updates price via WSO2 Gateway
    │
    ▼
Result: "Success: Price updated from $150.00 to $200.00"
    │
    ▼
LLM receives result and generates natural response:
"The price of product Gift Card has been successfully updated from $150.00 to $200.00"
    │
    ▼
User receives formatted response
```

**Advantages of Using Semantic Kernel:**

1. **No manual parsing needed**: The LLM understands multiple ways to express the same thing
   - "Update price of X to Y"
   - "Change the price of X to Y"
   - "Modify the price of X to Y"
   - "Set the price of X to Y"

2. **Automatic parameter extraction**: The LLM automatically identifies what is the product name and what is the price

3. **Context handling**: Semantic Kernel maintains conversation history
   ```
   User: "List the products"
   System: [Lists products]
   User: "Update the first one to 100"
   System: [Understands "the first one" refers to the first product from the previous list]
   ```

4. **Function composition**: The LLM can call multiple functions in sequence
   ```
   User: "Find the most expensive product and reduce its price by 10%"
   → LLM calls: get_products_sorted("desc") 
   → LLM calls: update_product_price_with_math(id, "percent_reduce", 10)
   ```

5. **Intelligent error handling**: If a function fails, the LLM can try another strategy
   ```
   User: "Update price of X to 200"
   → update_product_price_by_name("X") fails (not found)
   → LLM can suggest: "I didn't find 'X', did you mean 'Gift Card'?"
   ```

**In summary:** Semantic Kernel allows the LLM to "think" and "decide" which functions to execute based on user intention, instead of having to manually program all possible command combinations.

### 4. **OpenAI GPT-4o-mini (LLM) via WSO2 AI Gateway**
- **Role**: Natural language processing engine
- **Technology**: OpenAI API (gpt-4o-mini model) accessed through WSO2 AI Gateway
- **Access**: All LLM calls pass through WSO2 API Gateway (no direct access)
- **Responsibilities**:
  - Interpret natural language queries
  - Understand user intention
  - Generate natural and contextualized responses
  - Process Shopify data and format it for the user
  - Anti-hallucination system (real data only)

### 5. **WSO2 API Gateway**
- **Role**: Enterprise gateway and centralized security point
- **Technology**: WSO2 API Manager
- **Responsibilities**:
  - OAuth2 authentication (Client Credentials)
  - Routing requests to external services:
    - **Shopify API** (context: `/shopify/1.0.0`)
    - **OpenAI/ChatGPT API** (AI Gateway)
  - Access token management
  - Security policies and rate limiting
  - Header transformation
  - Centralization of all external calls
  - Monitoring and logging of all APIs

### 6. **Shopify API**
- **Role**: Ecommerce backend
- **Technology**: Shopify Admin REST API
- **Responsibilities**:
  - Product management
  - Price query and update
  - Product search by ID or name
  - CRUD operations on catalog
  - Endpoints used:
    - `GET /products.json` - List products
    - `GET /products/{id}.json` - Get specific product
    - `GET /products/count.json` - Count products
    - `PUT /products/{id}.json` - Update product

### 7. **Shopify Plugin (ShopifyPlugin)**
- **Role**: Abstraction layer between Semantic Kernel and Shopify
- **Technology**: Python class with `@kernel_function` decorators
- **Functions exposed to LLM**:
  - `get_products_list()` - Lists all products
  - `get_products_sorted(order)` - Products sorted by price
  - `count_products()` - Total product count
  - `find_product_by_name(name)` - Search by name with fuzzy matching
  - `update_product_price(id, price)` - Update price by ID
  - `update_product_price_by_name(name, price)` - Update price by name
  - `update_product_price_with_math(id, operation, value)` - Mathematical operations
  - `revert_price(id)` - Restore previous price

---

## Complete Call Flow

### Scenario: User requests "Update the price of product ID 123456 to 99.99"

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE CALL FLOW                               │
└─────────────────────────────────────────────────────────────────────────┘

1. USER INPUT
   ┌─────────────┐
   │   User      │
   │  "Update    │
   │   the price │
   │   of ID     │
   │   123456 to │
   │   99.99"    │
   └──────┬──────┘
          │
          ▼
2. PYTHON AGENT (agent_gpt4.py)
   ┌─────────────────────────────────────┐
   │  • Receives user input              │
   │  • Starts ThinkingIndicator         │
   │  • Detects intention: UPDATE_PRICE  │
   │  • Extracts parameters:              │
   │    - product_id: "123456"           │
   │    - new_price: "99.99"             │
   └──────┬──────────────────────────────┘
          │
          ▼
3. MICROSOFT SEMANTIC KERNEL
   ┌─────────────────────────────────────┐
   │  • Adds message to ChatHistory      │
   │  • Prepares enhanced prompt          │
   │  • Routes to appropriate function    │
   │  • Invokes Shopify plugin            │
   └──────┬──────────────────────────────┘
          │
          ▼
4. SHOPIFY PLUGIN (ShopifyPlugin)
   ┌─────────────────────────────────────┐
   │  • update_product_price() executed │
   │  • STEP 1: Get current price        │
   │    - Calls _make_api_call()         │
   └──────┬──────────────────────────────┘
          │
          ▼
5. WSO2 AUTHENTICATION (OAuth2)
   ┌─────────────────────────────────────┐
   │  • _get_wso2_access_token()         │
   │  • POST to WSO2_TOKEN_ENDPOINT       │
   │  • Headers:                          │
   │    Authorization: Basic {creds}      │
   │  • Payload: grant_type=client_       │
   │    credentials                       │
   │  • Response: access_token           │
   └──────┬──────────────────────────────┘
          │
          ▼
6. CALL TO SHOPIFY VIA WSO2 GATEWAY
   ┌─────────────────────────────────────┐
   │  • URL: {WSO2_GW_URL}/shopify/      │
   │    1.0.0/products/123456.json       │
   │  • Method: GET (get current)        │
   │  • Headers:                         │
   │    Authorization: Bearer {token}    │
   │    X-Shopify-Access-Token: {token}  │
   └──────┬──────────────────────────────┘
          │
          ▼
7. WSO2 API GATEWAY
   ┌─────────────────────────────────────┐
   │  • Validates OAuth2 token           │
   │  • Applies security policies        │
   │  • Routes to Shopify backend        │
   │  • Transforms headers                │
   │  • Request proxy                    │
   └──────┬──────────────────────────────┘
          │
          ▼
8. SHOPIFY API
   ┌─────────────────────────────────────┐
   │  • Validates Shopify token          │
   │  • Gets product ID 123456           │
   │  • Returns current price: $150.00   │
   └──────┬──────────────────────────────┘
          │
          ▼
9. RESPONSE BACK (GET)
   ┌─────────────────────────────────────┐
   │  WSO2 Gateway ← Shopify API         │
   │  • JSON response with product       │
   │  • Current price: $150.00           │
   └──────┬──────────────────────────────┘
          │
          ▼
10. SHOPIFY PLUGIN (Continuation)
    ┌─────────────────────────────────────┐
    │  • Saves previous price: $150.00    │
    │  • STEP 2: Prepare update          │
    │  • Gets variant_id                  │
    │  • Builds payload:                  │
    │    {                                 │
    │      "product": {                    │
    │        "id": 123456,                 │
    │        "variants": [{                │
    │          "id": variant_id,          │
    │          "price": "99.99"            │
    │        }]                            │
    │      }                               │
    │    }                                 │
    └──────┬──────────────────────────────┘
           │
           ▼
11. WSO2 AUTHENTICATION (OAuth2) - Reuses token
    ┌─────────────────────────────────────┐
    │  • Uses existing token or renews   │
    └──────┬──────────────────────────────┘
           │
           ▼
12. UPDATE CALL TO SHOPIFY VIA WSO2
    ┌─────────────────────────────────────┐
    │  • URL: {WSO2_GW_URL}/shopify/      │
    │    1.0.0/products/123456.json       │
    │  • Method: PUT                      │
    │  • Headers:                         │
    │    Authorization: Bearer {token}   │
    │    X-Shopify-Access-Token: {token}  │
    │    Content-Type: application/json   │
    │  • Body: JSON payload               │
    └──────┬──────────────────────────────┘
           │
           ▼
13. WSO2 API GATEWAY
    ┌─────────────────────────────────────┐
    │  • Validates token                  │
    │  • Applies policies                 │
    │  • Routes PUT to Shopify            │
    └──────┬──────────────────────────────┘
           │
           ▼
14. SHOPIFY API (Update)
    ┌─────────────────────────────────────┐
    │  • Updates price to $99.99          │
    │  • Returns updated product          │
    │  • Confirms new price: $99.99       │
    └──────┬──────────────────────────────┘
           │
           ▼
15. RESPONSE BACK (PUT)
    ┌─────────────────────────────────────┐
    │  WSO2 Gateway ← Shopify API         │
    │  • JSON response with product       │
    │  • Confirmed price: $99.99          │
    └──────┬──────────────────────────────┘
           │
           ▼
16. SHOPIFY PLUGIN (Validation)
    ┌─────────────────────────────────────┐
    │  • Verifies response                │
    │  • Compares sent vs received price │
    │  • Saves to PriceMemory:            │
    │    previous: $150.00                │
    │    current: $99.99                   │
    │  • Returns success message          │
    └──────┬──────────────────────────────┘
           │
           ▼
17. SEMANTIC KERNEL (Processing)
    ┌─────────────────────────────────────┐
    │  • Receives Shopify data            │
    │  • Builds enhanced prompt:          │
    │    "SUCCESSFUL UPDATE                │
    │     CONFIRMED: ..."                 │
    │  • Prepares LLM call                │
    └──────┬──────────────────────────────┘
           │
           │ POST /openai/v1/chat/completions
           │ Headers: Authorization: Bearer {token}
           ▼
17a. WSO2 AUTHENTICATION (OAuth2) - For OpenAI
    ┌─────────────────────────────────────┐
    │  • Gets OAuth2 token                │
    │  • (Can reuse existing token)       │
    └──────┬──────────────────────────────┘
           │
           ▼
17b. CALL TO OPENAI VIA WSO2 AI GATEWAY
    ┌─────────────────────────────────────┐
    │  • URL: {WSO2_GW_URL}/openai/...    │
    │  • Method: POST                     │
    │  • Headers:                          │
    │    Authorization: Bearer {wso2_token}│
    │  • Body: JSON prompt                 │
    └──────┬──────────────────────────────┘
           │
           ▼
17c. WSO2 AI GATEWAY
    ┌─────────────────────────────────────┐
    │  • Validates OAuth2 token            │
    │  • Applies security policies        │
    │  • Routes to OpenAI API             │
    │  • Transforms headers if needed     │
    └──────┬──────────────────────────────┘
           │
           ▼
18. OPENAI GPT-4o-mini (LLM)
    ┌─────────────────────────────────────┐
    │  • Receives prompt via WSO2 Gateway │
    │  • Processes prompt                 │
    │  • Generates natural response:      │
    │    "The price of product ID         │
    │     123456 has been successfully    │
    │     updated from $150.00 to         │
    │     $99.99."                        │
    └──────┬──────────────────────────────┘
           │
           │ JSON Response
           ▼
18a. RESPONSE BACK (OpenAI)
    ┌─────────────────────────────────────┐
    │  WSO2 AI Gateway ← OpenAI API        │
    │  • JSON response with text          │
    │  • Formatted by the LLM             │
    └──────┬──────────────────────────────┘
           │
           ▼
19. SEMANTIC KERNEL (Finalization)
    ┌─────────────────────────────────────┐
    │  • Adds response to ChatHistory     │
    │  • Returns formatted text           │
    └──────┬──────────────────────────────┘
           │
           ▼
20. PYTHON AGENT (Output)
    ┌─────────────────────────────────────┐
    │  • Stops ThinkingIndicator          │
    │  • Shows response to user            │
    │  • Waits for next query              │
    └──────┬──────────────────────────────┘
           │
           ▼
21. RESPONSE TO USER
    ┌─────────────┐
    │   User      │
    │  "The price │
    │   of        │
    │   product   │
    │   ID 123456 │
    │   has been  │
    │   updated   │
    │   from      │
    │   $150.00   │
    │   to $99.99"│
    └─────────────┘
```

---

## Component Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SYSTEM ARCHITECTURE                             │
└─────────────────────────────────────────────────────────────────────────┘


---

## OAuth2 Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OAUTH2 AUTHENTICATION FLOW                          │
└─────────────────────────────────────────────────────────────────────────┘

1. PYTHON AGENT
   ┌─────────────────────┐
   │  Needs token         │
   │  to call API         │
   └──────────┬───────────┘
              │
              │ POST /token
              │ Headers:
              │   Authorization: Basic {base64(consumer_key:consumer_secret)}
              │ Body:
              │   grant_type=client_credentials
              ▼
2. WSO2 TOKEN ENDPOINT
   ┌─────────────────────┐
   │  Validates credentials│
   │  Generates access_token │
   │  (expires in X time)│
   └──────────┬───────────┘
              │
              │ Response:
              │ {
              │   "access_token": "abc123...",
              │   "token_type": "Bearer",
              │   "expires_in": 3600
              │ }
              ▼
3. PYTHON AGENT
   ┌─────────────────────┐
   │  Stores token        │
   │  Uses in API calls   │
   └──────────┬───────────┘
              │
              ├─────────────────────┬─────────────────────┐
              │                     │                     │
              │ GET/PUT /shopify/   │ POST /openai/...    │
              │ 1.0.0/products/...  │                     │
              │ Headers:            │ Headers:            │
              │   Authorization:    │   Authorization:    │
              │   Bearer {token}    │   Bearer {token}    │
              │   X-Shopify-Access- │                     │
              │   Token: {token}   │                     │
              ▼                     ▼                     ▼
4. WSO2 API GATEWAY
   ┌─────────────────────────────────────────────────────┐
   │  Validates access_token                             │
   │  ├─ Routes to Shopify (/shopify/1.0.0)             │
   │  └─ Routes to OpenAI (/openai/...) [AI Gateway]    │
   └─────────────────────────────────────────────────────┘
```

---

## Technologies and Protocols Used

### Languages and Frameworks
- **Python 3.8+**: Main agent language
- **Microsoft Semantic Kernel**: AI orchestration framework
- **OpenAI API**: LLM service

### Communication Protocols
- **HTTP/HTTPS**: Communication protocol between components
- **REST API**: API architecture for Shopify
- **OAuth2 Client Credentials**: Authentication flow with WSO2
- **JSON**: Data exchange format

### External Services
- **WSO2 API Manager**: Centralized enterprise gateway
  - Routes calls to Shopify API
  - Routes calls to OpenAI API (AI Gateway)
- **Shopify Admin API**: Ecommerce API (accessed via WSO2)
- **OpenAI GPT-4o-mini**: Language model (accessed via WSO2 AI Gateway)

### Security
- **OAuth2**: Authentication and authorization
- **Bearer Tokens**: Access tokens
- **HTTPS**: Encrypted communication
- **Environment Variables**: Secure credential management

---

## Key System Features

### 1. **Anti-Hallucination System**
- Only returns real data from Shopify
- Never invents products, prices, or IDs
- Verifies all operations before confirming

### 2. **Price Memory (PriceMemory)**
- Remembers previous price changes
- Allows reverting to original prices
- Maintains history during the session

### 3. **Intelligent Intent Detection**
- Bilingual support (Spanish/English)
- Recognition of multiple ways to express the same thing
- Automatic parameter extraction

### 4. **Mathematical Operations**
- Add/subtract values
- Multiply/divide prices
- Percentage increments/decrements
- Special operations (half, double)

### 5. **Flexible Search**
- Search by exact ID
- Search by name with fuzzy matching
- Suggestions when there's no exact match

---

## Environment Variables Configuration

```bash
# WSO2 Configuration
WSO2_TOKEN_ENDPOINT=https://wso2-instance.com/token
WSO2_CONSUMER_KEY=your_consumer_key
WSO2_CONSUMER_SECRET=your_consumer_secret
WSO2_GW_URL=https://wso2-gateway.com:8243

# Shopify Configuration
SHOPIFY_API_TOKEN=your_shopify_token

# OpenAI Configuration
OPENAI_API_KEY=your_openai_key
```

---

## Endpoints and Routes

### WSO2 Gateway Endpoints
- **Token**: `POST {WSO2_TOKEN_ENDPOINT}/token`
- **Shopify API Base**: `{WSO2_GW_URL}/shopify/1.0.0`
- **OpenAI AI Gateway Base**: `{WSO2_GW_URL}/openai/...`

### Shopify API Endpoints (via WSO2 Gateway)
- `GET /shopify/1.0.0/products.json` - List products
- `GET /shopify/1.0.0/products/{id}.json` - Get product
- `GET /shopify/1.0.0/products/count.json` - Count products
- `PUT /shopify/1.0.0/products/{id}.json` - Update product

### OpenAI API Endpoints (via WSO2 AI Gateway)
- `POST /openai/v1/chat/completions` - Complete conversation (ChatGPT)
- `POST /openai/v1/completions` - Complete text
- `POST /openai/v1/embeddings` - Generate embeddings
- All OpenAI calls pass through WSO2 Gateway (no direct access)

---

## Main Use Cases

### 1. List Products
**User**: "List the products"  
**Flow**: User → Agent → Semantic Kernel → Plugin → WSO2 → Shopify → Response

### 2. Count Products
**User**: "How many products are there?"  
**Flow**: Similar to above, but executes `count_products()`

### 3. Update Price by ID
**User**: "Update the price of ID 123456 to 99.99"  
**Flow**: Complete as shown above (21 steps)

### 4. Update Price by Name
**User**: "Change the price of Gift Card to 200"  
**Flow**: Includes name search before updating

### 5. Mathematical Operations
**User**: "Add 1000 to the price of The Complete Snowboard"  
**Flow**: Gets current price, calculates new price, updates

### 6. Revert Price
**User**: "Restore the original price of ID 123456"  
**Flow**: Queries PriceMemory, restores previous price

---

## Advantages of this Architecture

1. **Enterprise Security**: Centralized WSO2 Gateway provides robust security layer for all APIs (Shopify and OpenAI)
2. **Centralization**: All external calls pass through a single control point (WSO2 Gateway)
3. **Scalability**: Modular architecture allows scaling components independently
4. **Maintainability**: Clear separation of responsibilities
5. **Extensibility**: Easy to add new plugins and functions
6. **User Experience**: Natural language makes the system accessible
7. **Reliability**: Anti-hallucination system ensures accurate data
8. **Observability**: Debug mode allows detailed diagnosis
9. **API Governance**: Centralized control of policies, rate limiting, and monitoring for all APIs

---

## Notes for PowerPoint Presentation

### Suggested Slides:

1. **Title**: AI Agent Architecture for Ecommerce
2. **Components**: Main components diagram
3. **Complete Flow**: Call flow diagram (21 steps)
4. **Authentication**: Detailed OAuth2 flow
5. **Technologies**: Technology stack used
6. **Use Cases**: Practical usage examples
7. **Advantages**: Architecture benefits

### Recommended Visual Elements:
- Use consistent colors for each component
- Clear arrows showing flow direction
- Icons for each technology (WSO2, Shopify, OpenAI, Python)
- Sequential numbering in the complete flow
- Highlight critical points (authentication, validation)

---

**Document generated for architectural presentation**  
**Version**: 1.0  
**Date**: 2024
