# Diagrams for PowerPoint Presentation

This document contains simplified diagrams ready to use in PowerPoint presentations.

---

## Diagram 1: High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HIGH-LEVEL ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  User    │
    │  (NLP)   │
    └────┬─────┘
         │
         │ Natural language query
         ▼
    ┌─────────────────────┐
    │  Python Agent       │
    │  (Orchestrator)     │
    └────┬────────────────┘
         │
         │ Processed query
         ▼
    ┌─────────────────────┐
    │ Semantic Kernel     │
    │  (AI Orchestration) │
    └────┬────────────────┘
         │
         ├─────────────────┬──────────────┐
         │                 │              │
         ▼                 ▼              │
    ┌──────────┐    ┌──────────────┐
    │ Plugin   │    │   LLM        │
    │ Shopify  │    │  Requests    │
    │          │    │  (OpenAI)    │
    └────┬─────┘    └──────┬───────┘
         │                 │
         └─────────┬───────┴──────────────┘
                   │
                   │ OAuth2
                   │ (All external calls)
                   ▼
         ┌─────────────────────┐
         │  WSO2 API Gateway   │
         │  (Centralized)      │
         └────┬─────────────────┘
              │
              ├─────────────────┬──────────────┐
              │                 │              │
              ▼                 ▼
    ┌─────────────────┐  ┌─────────────────┐
    │   Shopify API   │  │   OpenAI API    │
    │                 │  │  (AI Gateway)   │
    └─────────────────┘  └─────────────────┘
```

---

## Diagram 2: Call Flow (Simplified)

```
┌─────────────────────────────────────────────────────────────────────┐
│              CALL FLOW - UPDATE PRICE                              │
└─────────────────────────────────────────────────────────────────────┘

1. USER
   "Update price ID 123456 to 99.99"
         │
         ▼
2. PYTHON AGENT
   • Detects intention: UPDATE_PRICE
   • Extracts: ID=123456, price=99.99
         │
         ▼
3. SEMANTIC KERNEL
   • Orchestrates execution
   • Calls plugin function
         │
         ▼
4. SHOPIFY PLUGIN
   • Gets current price ($150.00)
   • Prepares update
         │
         ▼
5. WSO2 AUTHENTICATION
   • Gets OAuth2 token
         │
         ▼
6. WSO2 GATEWAY
   • Validates token
   • Routes to Shopify
         │
         ▼
7. SHOPIFY API
   • Updates price to $99.99
   • Confirms change
         │
         ▼
8. RESPONSE
   • Plugin validates success
   • Saves to memory
         │
         ▼
9. SEMANTIC KERNEL
   • Prepares prompt for LLM
         │
         │ OAuth2
         ▼
10. WSO2 AI GATEWAY
    • Validates token
    • Routes to OpenAI
         │
         ▼
11. OPENAI API
    • Processes prompt
    • Generates natural response
         │
         │ Response via WSO2
         ▼
12. SEMANTIC KERNEL
    • Receives formatted response
         │
         ▼
13. USER
    "Price updated from $150.00 to $99.99"
```

---

## Diagram 3: Components and Responsibilities

```
┌─────────────────────────────────────────────────────────────────────┐
│              COMPONENTS AND THEIR RESPONSIBILITIES                 │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│   USER               │
│ • Sends queries       │
│ • Receives responses  │
└──────────────────────┘

┌──────────────────────┐
│   PYTHON AGENT       │
│ • Orchestration       │
│ • Intent detection    │
│ • State management    │
│ • Price memory        │
└──────────────────────┘

┌──────────────────────┐
│ SEMANTIC KERNEL      │
│ • Connects LLM and    │
│   functions          │
│ • Manages context     │
│ • Plugin system       │
└──────────────────────┘

┌──────────────────────┐
│   OPENAI GPT-4o-mini  │
│ • Processes natural   │
│   language            │
│ • Generates responses │
│ • Anti-hallucination  │
│ • Access via WSO2     │
│   AI Gateway          │
└──────────────────────┘

┌──────────────────────┐
│  SHOPIFY PLUGIN      │
│ • Executable functions│
│ • API abstraction     │
│ • CRUD operations     │
└──────────────────────┘

┌──────────────────────┐
│  WSO2 API GATEWAY    │
│ • OAuth2 authentication│
│ • Routing             │
│   - Shopify API       │
│   - OpenAI API        │
│ • Security            │
│ • Rate limiting       │
│ • Centralized         │
└──────────────────────┘

┌──────────────────────┐
│   SHOPIFY API        │
│ • Product management  │
│ • Price updates       │
│ • Search              │
│ • Access via WSO2     │
└──────────────────────┘
```

---

## Diagram 4: OAuth2 Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OAUTH2 CLIENT CREDENTIALS FLOW                  │
└─────────────────────────────────────────────────────────────────────┘

PYTHON AGENT                    WSO2 TOKEN ENDPOINT
┌─────────────┐                  ┌──────────────────┐
│             │                  │                  │
│ Needs       │                  │                  │
│ token       │                  │                  │
│             │                  │                  │
│ POST /token │─────────────────►│ Validates        │
│ Headers:    │                  │ credentials       │
│ Basic auth  │                  │                  │
│             │                  │ Generates         │
│             │                  │ access_token      │
│             │◄─────────────────│                  │
│ Stores      │                  │ Response:         │
│ token       │                  │ {access_token}    │
│             │                  │                  │
└──────┬──────┘                  └──────────────────┘
       │
       │ Uses token in calls
       │ Authorization: Bearer {token}
       ▼
WSO2 API GATEWAY
┌─────────────────────────────┐
│                             │
│ Validates token             │
│                             │
│ Routes to:                  │
│  • Shopify API              │
│  • OpenAI API (AI Gateway)  │
│                             │
└─────────────────────────────┘
```

---

## Diagram 5: Technology Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY STACK                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  • Command line interface (CLI)                              │
│  • Natural language (Spanish/English)                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  • Python 3.8+                                               │
│  • Microsoft Semantic Kernel                                 │
│  • OpenAI GPT-4o-mini                                        │
│  • Plugin system                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                        │
│  • WSO2 API Manager (Gateway)                                │
│  • OAuth2 Client Credentials                                 │
│  • REST API                                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DATA/SERVICES LAYER                      │
│  • Shopify Admin API (via WSO2 Gateway)                     │
│  • OpenAI API (via WSO2 AI Gateway)                          │
│  • Product management                                        │
│  • Price management                                          │
│  • Natural language processing                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 6: Shopify Plugin Functions

```
┌─────────────────────────────────────────────────────────────────────┐
│              FUNCTIONS EXPOSED TO LLM                            │
└─────────────────────────────────────────────────────────────────────┘

PLUGIN SHOPIFY
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  QUERIES                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • get_products_list()                               │   │
│  │   → Lists all products                              │   │
│  │                                                      │   │
│  │ • get_products_sorted(order)                        │   │
│  │   → Products sorted by price                        │   │
│  │                                                      │   │
│  │ • count_products()                                  │   │
│  │   → Total product count                             │   │
│  │                                                      │   │
│  │ • find_product_by_name(name)                        │   │
│  │   → Search with fuzzy matching                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  UPDATES                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • update_product_price(id, price)                   │   │
│  │   → Updates by ID                                    │   │
│  │                                                      │   │
│  │ • update_product_price_by_name(name, price)        │   │
│  │   → Updates by name                                 │   │
│  │                                                      │   │
│  │ • update_product_price_with_math(id, op, value)    │   │
│  │   → Mathematical operations                         │   │
│  │                                                      │   │
│  │ • revert_price(id)                                  │   │
│  │   → Restores previous price                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 7: Main Use Cases

```
┌─────────────────────────────────────────────────────────────────────┐
│                      MAIN USE CASES                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  1. LIST PRODUCTS                                           │
│  User: "List the products"                                  │
│  → get_products_list()                                      │
│  → Response: Complete list with IDs and prices              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  2. COUNT PRODUCTS                                          │
│  User: "How many products are there?"                       │
│  → count_products()                                         │
│  → Response: "The store has X products"                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  3. UPDATE PRICE BY ID                                      │
│  User: "Update price ID 123456 to 99.99"                    │
│  → update_product_price(123456, "99.99")                   │
│  → Response: "Price updated from $X to $99.99"              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  4. UPDATE PRICE BY NAME                                    │
│  User: "Change price of Gift Card to 200"                   │
│  → find_product_by_name("Gift Card")                        │
│  → update_product_price_by_name("Gift Card", "200")         │
│  → Response: "Price updated..."                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  5. MATHEMATICAL OPERATION                                  │
│  User: "Add 1000 to the price of X"                         │
│  → update_product_price_with_math(id, "add", 1000)        │
│  → Response: "Price updated from $X to $Y (adding...)"      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  6. REVERT PRICE                                            │
│  User: "Restore original price of ID 123456"                │
│  → revert_price(123456)                                     │
│  → Response: "Price restored to $X"                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 8: Architecture Advantages

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE ADVANTAGES                     │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│   SECURITY           │  │   SCALABILITY        │
│ • OAuth2             │  │ • Independent        │
│ • WSO2 Gateway       │  │   components         │
│   Centralized        │  │ • Horizontal scaling │
│ • Secure tokens      │  │ • Gateway as single  │
│ • All APIs           │  │   entry point        │
│   via gateway        │  │                     │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│   MAINTAINABILITY    │  │   EXTENSIBILITY      │
│ • Modular code       │  │ • New plugins        │
│ • Separation of      │  │ • New functions      │
│   responsibilities   │  │ • Easy integration   │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│   USER EXPERIENCE    │  │   RELIABILITY       │
│ • Natural language    │  │ • Anti-hallucination │
│ • Bilingual           │  │ • Data validation    │
│ • Clear responses     │  │ • Verification       │
└──────────────────────┘  └──────────────────────┘
```

---

## Diagram 9: Detailed Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                  DETAILED DATA FLOW                         │
└─────────────────────────────────────────────────────────────────────┘

USER
  │
  │ "Update price ID 123456 to 99.99"
  ▼
PYTHON AGENT
  │ • Parses input
  │ • Detects: UPDATE_PRICE
  │ • Extracts: ID=123456, price=99.99
  ▼
SEMANTIC KERNEL
  │ • Builds prompt
  │ • Identifies function: update_product_price()
  │ • Prepares context
  ▼
SHOPIFY PLUGIN
  │ • Executes update_product_price()
  │ • STEP 1: GET /products/123456.json
  │   → Gets current price: $150.00
  │ • STEP 2: Prepares PUT payload
  │ • STEP 3: PUT /products/123456.json
  │   → Updates to $99.99
  │ • STEP 4: Validates response
  │ • STEP 5: Saves to PriceMemory
  ▼
WSO2 GATEWAY
  │ • Authenticates with OAuth2
  │ • Routes requests
  │ • Applies policies
  ▼
SHOPIFY API
  │ • Processes GET (get current)
  │ • Processes PUT (update)
  │ • Returns confirmation
  ▼
RESPONSE
  │ • Plugin returns: "Success: $150.00 → $99.99"
  ▼
SEMANTIC KERNEL
  │ • Builds enhanced prompt
  │ • Prepares LLM call
  │ • OAuth2 for OpenAI
  ▼
WSO2 AI GATEWAY
  │ • Validates OAuth2 token
  │ • Routes to OpenAI API
  │ • Applies policies
  ▼
OPENAI GPT-4o-mini
  │ • Receives prompt via WSO2 Gateway
  │ • Generates natural response
  │ • "The price of product ID 123456
  │    has been updated from $150.00 to $99.99"
  │ • Returns via WSO2 Gateway
  ▼
SEMANTIC KERNEL
  │ • Receives formatted response
  │ • Processes and returns
  ▼
USER
  │ Receives formatted response
  └
```

---

## Diagram 10: Price Memory System

```
┌─────────────────────────────────────────────────────────────────────┐
│              PRICE MEMORY SYSTEM (PriceMemory)           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PRICE MEMORY                                                │
│  ┌───────────────────────────────────────────────────────┐   │
│  │  price_history = {                                    │   │
│  │    "123456": {                                        │   │
│  │      "previous": "150.00",                            │   │
│  │      "current": "99.99"                               │   │
│  │    },                                                 │   │
│  │    "789012": {                                        │   │
│  │      "previous": "200.00",                            │   │
│  │      "current": "250.00"                              │   │
│  │    }                                                  │   │
│  │  }                                                    │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  OPERATIONS:                                                │
│  • remember_price_change(id, old, new)                       │
│  • get_previous_price(id)                                    │
│  • has_history(id)                                           │
│  • revert_price(id) → Restores previous price              │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 11: What is Semantic Kernel? (Visual Explanation)

```
┌─────────────────────────────────────────────────────────────────────┐
│              WHAT IS SEMANTIC KERNEL AND WHAT IS IT FOR?              │
└─────────────────────────────────────────────────────────────────────┘

PROBLEM WITHOUT SEMANTIC KERNEL:
┌─────────────────────────────────────────────────────────────┐
│  User: "Update price of Gift Card to 200"                  │
│                                                             │
│  Traditional code needs:                                    │
│  • Manual text parsing                                     │
│  • Manual parameter extraction                              │
│  • Handling multiple variations                            │
│  • Complex conditional logic                                │
│                                                             │
│  if "update" in text and "price" in text:                  │
│      product = extract_product(text)                       │
│      price = extract_price(text)                           │
│      update(product, price)                                │
└─────────────────────────────────────────────────────────────┘

SOLUTION WITH SEMANTIC KERNEL:
┌─────────────────────────────────────────────────────────────┐
│  User: "Update price of Gift Card to 200"                  │
│                                                             │
│  Semantic Kernel automatically:                             │
│  1. LLM analyzes the intention                             │
│  2. LLM decides which function to call                      │
│  3. LLM extracts parameters automatically                   │
│  4. Executes the function                                  │
│  5. LLM generates natural response                         │
│                                                             │
│  kernel.invoke_prompt("Update price...")                    │
│  → LLM calls: update_product_price_by_name(                 │
│       "Gift Card", "200")                                   │
│  → Response: "Price updated successfully"                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 12: Semantic Kernel Flow (Detailed Example)

```
┌─────────────────────────────────────────────────────────────────────┐
│         SEMANTIC KERNEL FLOW - STEP BY STEP EXAMPLE              │
└─────────────────────────────────────────────────────────────────────┘

USER INPUT
┌─────────────────────────────────────┐
│ "Update the price of product       │
│  Gift Card to 200 dollars"         │
└──────────────┬─────────────────────┘
                │
                ▼
SEMANTIC KERNEL RECEIVES MESSAGE
┌─────────────────────────────────────┐
│ • Adds message to ChatHistory        │
│ • Prepares context for LLM          │
└──────────────┬─────────────────────┘
                │
                ▼
LLM (OpenAI) ANALYZES INTENTION
┌─────────────────────────────────────┐
│ Analysis:                           │
│ • Intention: UPDATE_PRICE           │
│ • Entity: product = "Gift Card"    │
│ • Entity: price = "200"             │
│ • Required action: call function     │
└──────────────┬─────────────────────┘
                │
                ▼
LLM DECIDES WHICH FUNCTION TO CALL
┌─────────────────────────────────────┐
│ Available functions:                │
│ • update_product_price(id, price)    │
│ • update_product_price_by_name(...)  │ ← SELECTS THIS
│ • get_products_list()                │
│ • count_products()                   │
└──────────────┬─────────────────────┘
                │
                ▼
LLM EXTRACTS PARAMETERS
┌─────────────────────────────────────┐
│ Extracted parameters:               │
│ • product_name = "Gift Card"        │
│ • new_price = "200"                  │
└──────────────┬─────────────────────┘
                │
                ▼
SEMANTIC KERNEL EXECUTES FUNCTION
┌─────────────────────────────────────┐
│ shopify_plugin.update_product_       │
│   price_by_name("Gift Card", "200")  │
│                                      │
│ → Searches product by name           │
│ → Gets product ID                     │
│ → Updates price via WSO2             │
│ → Returns: "Success: $150 → $200"   │
└──────────────┬─────────────────────┘
                │
                ▼
LLM RECEIVES RESULT AND GENERATES RESPONSE
┌─────────────────────────────────────┐
│ Result received:                     │
│ "Success: Price updated from         │
│  $150.00 to $200.00"                 │
│                                      │
│ LLM generates natural response:      │
│ "The price of product Gift Card      │
│  has been successfully updated       │
│  from $150.00 to $200.00."           │
└──────────────┬─────────────────────┘
                │
                ▼
RESPONSE TO USER
┌─────────────────────────────────────┐
│ "The price of product Gift Card    │
│  has been successfully updated     │
│  from $150.00 to $200.00."         │
└─────────────────────────────────────┘
```

---

## Diagram 13: Semantic Kernel Advantages

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SEMANTIC KERNEL ADVANTAGES                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  1. NO MANUAL PARSING NEEDED                                 │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ Understands multiple ways to express the same thing:  │   │
│  │ • "Update price of X to Y"                             │   │
│  │ • "Change the price of X to Y"                        │   │
│  │ • "Modify price of X to Y"                            │   │
│  │ • "Set the price of X to Y"                           │   │
│  │ • "Update price of X to Y" (English too)             │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  2. AUTOMATIC PARAMETER EXTRACTION                           │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ LLM automatically identifies:                          │   │
│  │ • What is the product name                            │   │
│  │ • What is the price                                    │   │
│  │ • What is the ID                                        │   │
│  │ • What operation to perform                           │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  3. CONTEXT HANDLING                                         │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ User: "List the products"                              │   │
│  │ System: [Shows list]                                    │   │
│  │ User: "Update the first one to 100"                    │   │
│  │ System: [Understands "the first one" = first product]  │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  4. FUNCTION COMPOSITION                                     │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ User: "Find the most expensive product and reduce 10%"│   │
│  │ → LLM calls: get_products_sorted("desc")               │   │
│  │ → LLM calls: update_product_price_with_math(          │   │
│  │     id, "percent_reduce", 10)                          │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  5. INTELLIGENT ERROR HANDLING                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ If a function fails, the LLM can:                      │   │
│  │ • Try another strategy                                 │   │
│  │ • Suggest alternatives                                 │   │
│  │ • Explain the error naturally                          │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 14: Python Agent Components - Detailed Explanation

```
┌─────────────────────────────────────────────────────────────────────┐
│         PYTHON AGENT COMPONENTS - FUNCTIONALITIES             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  1. INTENT DETECTION                                         │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  WHAT DOES IT DO?                                       │   │
│  │  Analyzes user text to identify                        │   │
│  │  what action they want to perform                      │   │
│  │                                                         │   │
│  │  HOW IT WORKS:                                          │   │
│  │  • Uses keyword dictionaries                           │   │
│  │  • Detects patterns with regex                         │   │
│  │  • Works in Spanish and English                        │   │
│  │  • Extracts parameters automatically                    │   │
│  │                                                         │   │
│  │  EXAMPLE:                                               │   │
│  │  User: "Update price ID 123456 to 99.99"               │   │
│  │  → Detects: 'update_price'                             │   │
│  │  → Extracts: ID=123456, price=99.99                    │   │
│  │                                                         │   │
│  │  Detected keywords:                                     │   │
│  │  • List: ['products', 'list', 'show', ...]            │   │
│  │  • Update: ['update', 'change', ...]                   │   │
│  │  • Count: ['how many', 'quantity', ...]               │   │
│  │  • Operations: ['add', 'subtract', ...]                │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  2. PRICE MEMORY                                             │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  WHAT DOES IT DO?                                       │   │
│  │  Stores price change history to                        │   │
│  │  allow reverting changes                                │   │
│  │                                                         │   │
│  │  HOW IT WORKS:                                          │   │
│  │  • When updating price, saves previous price            │   │
│  │  • Maintains in-memory dictionary                        │   │
│  │  • Allows querying previous price                       │   │
│  │  • Allows reverting changes                             │   │
│  │                                                         │   │
│  │  DATA STRUCTURE:                                        │   │
│  │  price_history = {                                      │   │
│  │    "123456": {                                          │   │
│  │      "previous": "150.00",                              │   │
│  │      "current": "99.99"                                 │   │
│  │    }                                                    │   │
│  │  }                                                      │   │
│  │                                                         │   │
│  │  EXAMPLE:                                               │   │
│  │  1. User: "Update ID 123456 to 99.99"                  │   │
│  │     → Saves: previous=$150.00, current=$99.99         │   │
│  │                                                         │   │
│  │  2. User: "Restore original price ID 123456"           │   │
│  │     → Queries: get_previous_price("123456")            │   │
│  │     → Returns: "150.00"                                 │   │
│  │     → Restores price to $150.00                         │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  3. THINKING INDICATOR (Progress Indicator)                 │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  WHAT DOES IT DO?                                       │   │
│  │  Shows animated visual indicator while                  │   │
│  │  processing the query                                    │   │
│  │                                                         │   │
│  │  HOW IT WORKS:                                          │   │
│  │  • Activates at start of processing                     │   │
│  │  • Shows animation: "Thinking...", "Thinking...."     │   │
│  │  • Runs in separate thread                             │   │
│  │  • Stops when finished                                  │   │
│  │                                                         │   │
│  │  VISUAL EXAMPLE:                                        │   │
│  │  User: "List the products"                              │   │
│  │  → Shows: "Thinking..." (animated)                      │   │
│  │  → [Processing...]                                      │   │
│  │  → [Getting data...]                                    │   │
│  │  → Hides: "Thinking..."                                 │   │
│  │  → Shows: "Products found..."                          │   │
│  │                                                         │   │
│  │  ADVANTAGES:                                            │   │
│  │  • Better user experience                                │   │
│  │  • Immediate visual feedback                            │   │
│  │  • Prevents feeling of system "frozen"                  │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 15: Intent Detection Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│              INTENT DETECTION FLOW                     │
└─────────────────────────────────────────────────────────────────────┘

USUARIO ENVÍA CONSULTA
┌─────────────────────────────────────┐
│ "Actualiza precio ID 123456 a 99.99"│
└──────────────┬─────────────────────┘
               │
               ▼
AGENTE PYTHON RECIBE TEXTO
┌─────────────────────────────────────┐
│ • Convierte a minúsculas            │
│ • Prepara para análisis              │
└──────────────┬─────────────────────┘
               │
               ▼
ANÁLISIS DE PALABRAS CLAVE
┌─────────────────────────────────────┐
│ Busca en diccionarios:              │
│                                     │
│ UPDATE_PRICE keywords:              │
│ ['actualizar', 'cambiar', 'modificar',│
│  'update', 'change', 'modify']      │
│                                     │
│ ✓ Encontrado: "actualiza"           │
└──────────────┬─────────────────────┘
               │
               ▼
DETECCIÓN DE PATRONES (REGEX)
┌─────────────────────────────────────┐
│ Patrones de precio:                 │
│ • r'id[:\s]*(\d+)'                  │
│ • r'a\s+[\$€]?\d+'                  │
│ • r'precio\s+[\$€]?\d+'             │
│                                     │
│ ✓ Encontrado: ID=123456             │
│ ✓ Encontrado: precio=99.99          │
└──────────────┬─────────────────────┘
               │
               ▼
RESULTADO DE DETECCIÓN
┌─────────────────────────────────────┐
│ Intención: UPDATE_PRICE              │
│ Parámetros extraídos:                │
│ • product_id = "123456"              │
│ • new_price = "99.99"                │
│ • product_name = None                │
│ • math_operation = None              │
└──────────────┬─────────────────────┘
               │
               ▼
EJECUCIÓN DE FUNCIÓN
┌─────────────────────────────────────┐
│ shopify_plugin.update_product_price( │
│   "123456", "99.99")                │
└─────────────────────────────────────┘
```

---

## Diagram 16: PriceMemory Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PRICE MEMORY FLOW                           │
└─────────────────────────────────────────────────────────────────────┘

SCENARIO 1: UPDATE PRICE
┌─────────────────────────────────────────────────────────────┐
│ User: "Update price ID 123456 to 99.99"                    │
│                                                             │
│ 1. System gets current price: $150.00                    │
│ 2. Updates price to $99.99                                 │
│ 3. PriceMemory automatically saves:                        │
│                                                             │
│    price_history["123456"] = {                              │
│      "previous": "150.00",                                 │
│      "current": "99.99"                                     │
│    }                                                        │
│                                                             │
│ 4. Confirmation: "Price updated from $150.00 to $99.99"   │
└─────────────────────────────────────────────────────────────┘

SCENARIO 2: REVERT PRICE
┌─────────────────────────────────────────────────────────────┐
│ User: "Restore original price of ID 123456"               │
│                                                             │
│ 1. System queries PriceMemory:                            │
│    → has_history("123456") = True                          │
│    → get_previous_price("123456") = "150.00"               │
│                                                             │
│ 2. System restores price:                                  │
│    → update_product_price("123456", "150.00")              │
│                                                             │
│ 3. PriceMemory updates:                                     │
│    price_history["123456"] = {                              │
│      "previous": "99.99",   (now is the previous)         │
│      "current": "150.00"    (restored price)                │
│    }                                                        │
│                                                             │
│ 4. Confirmation: "Price restored to $150.00"              │
└─────────────────────────────────────────────────────────────┘

MEMORY STATE
┌─────────────────────────────────────────────────────────────┐
│ price_history = {                                           │
│   "123456": {                                               │
│     "previous": "150.00",                                   │
│     "current": "99.99"                                      │
│   },                                                         │
│   "789012": {                                               │
│     "previous": "200.00",                                   │
│     "current": "250.00"                                     │
│   }                                                          │
│ }                                                            │
│                                                              │
│ Available operations:                                       │
│ • remember_price_change(id, old, new)                       │
│ • get_previous_price(id)                                    │
│ • has_history(id)                                           │
│ • revert_price(id)                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagram 17: ThinkingIndicator Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                  THINKING INDICATOR FLOW                       │
└─────────────────────────────────────────────────────────────────────┘

PROCESSING START
┌─────────────────────────────────────┐
│ User: "List the products"            │
└──────────────┬─────────────────────┘
               │
               ▼
THINKING INDICATOR ACTIVATES
┌─────────────────────────────────────┐
│ thinking = ThinkingIndicator(        │
│   "Processing query")                │
│ thinking.start()                     │
│                                      │
│ Screen shows:                        │
│ "Processing query..." (animated)     │
│                                      │
│ [Separate thread runs animation]    │
└──────────────┬─────────────────────┘
               │
               ▼
PARALLEL PROCESSING
┌─────────────────────────────────────┐
│ [Thread 1: Animation]                │
│ "Processing query..."                 │
│ "Processing query...."                │
│ "Processing query....."               │
│ "Processing query...."                │
│ (continuous cycle)                    │
│                                      │
│ [Thread 2: Processing]               │
│ • Detect intention                    │
│ • Call Shopify                        │
│ • Get data                            │
│ • Generate response                   │
└──────────────┬─────────────────────┘
               │
               ▼
COMPLETION
┌─────────────────────────────────────┐
│ thinking.stop()                      │
│                                      │
│ • Stops animation                    │
│ • Clears line                         │
│ • Shows response                      │
│                                      │
│ Screen shows:                        │
│ "Products found (5 total):          │
│  - ID: 123456 - Gift Card - $150.00" │
└─────────────────────────────────────┘

COMPLETE VISUAL EXAMPLE
┌─────────────────────────────────────┐
│ User: List the products              │
│                                      │
│ System: Processing query...           │
│          Processing query....        │
│          Processing query.....       │
│          Processing query....        │
│                                      │
│ System: [Clears line]                │
│                                      │
│ System: Products found:              │
│          - ID: 123456 - Gift Card    │
│          - ID: 789012 - Snowboard    │
└─────────────────────────────────────┘
```

---

## Instructions for PowerPoint

### Suggested Colors:
- **User**: Light blue (#E3F2FD)
- **Python Agent**: Green (#C8E6C9)
- **Semantic Kernel**: Purple (#E1BEE7)
- **OpenAI**: Orange (#FFE0B2)
- **WSO2 Gateway**: Red/Orange (#FFCCBC)
- **Shopify**: Emerald green (#B2DFDB)

### Typography:
- Titles: Arial Bold, 24pt
- Subtitles: Arial Bold, 18pt
- Text: Arial Regular, 14pt
- Code: Courier New, 12pt

### Suggested Animations:
- Component entry: Appear one by one
- Flows: Animated arrows following order
- Highlight: Active component with glow effect

### Transitions:
- Between slides: Soft fade
- Between sections: Vertical curtain

---

**Diagram document for PowerPoint presentation**  
**Version**: 1.0  
**Date**: 2024

