# Customer Support AI Agent

An AI-powered customer support backend built with **Python, FastAPI, LangGraph, PostgreSQL/Supabase, and Retrieval-Augmented Generation (RAG)**.

The goal is to build a modular AI agent that can understand customer queries, retrieve relevant business records, search company policies, and generate grounded responses through a structured workflow.

> **Project status:** This project is under active development. Database access functions, the policy RAG pipeline, LangChain tools, and an initial FastAPI API have been developed incrementally. Full end-to-end integration, persistent conversations, human approval, evaluation, and production deployment should be verified against the current code before being considered complete.

---

## Table of Contents

- [Overview](#overview)
- [Project Goals](#project-goals)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Knowledge Base and RAG](#knowledge-base-and-rag)
- [LangGraph and Agent Tools](#langgraph-and-agent-tools)
- [FastAPI Backend](#fastapi-backend)
- [Frontend Integration](#frontend-integration)
- [Evaluation Dataset](#evaluation-dataset)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)
- [License](#license)

## Overview

Traditional customer support systems often rely on predefined responses or manual database lookups. An AI-powered support agent can combine natural-language understanding, structured business data, and company policies to assist customers more efficiently.

This project explores a tool-enabled, graph-orchestrated approach to customer support.

For example, when a customer asks:

> Where is my order, and what happens if it arrives late?

The intended workflow can:

1. Interpret the customer's question.
2. Identify the required business-data and policy lookups.
3. Retrieve the relevant order information from PostgreSQL.
4. Search the company knowledge base for the delayed-delivery policy.
5. Combine the available evidence.
6. Generate a response based on the retrieved information.
7. Request clarification or escalate when necessary.

The application separates API handling, agent orchestration, database operations, and policy retrieval so that each component can be tested and improved independently.

## Project Goals

- Build a modular customer support AI agent.
- Use LangGraph to orchestrate multi-step workflows.
- Retrieve structured customer, order, product, payment, seller, and review information.
- Use RAG to ground policy-related responses in company documentation.
- Expose the agent through a FastAPI backend.
- Support multi-turn conversations and conversation persistence.
- Introduce safe ticket-management workflows and human approval.
- Evaluate response quality using customer-support conversations.
- Prepare the application for monitoring and production deployment.

## Architecture

```text
                  Customer / Frontend
                          |
                          | HTTP POST
                          v
                    FastAPI API
                          |
                          v
                   LangGraph Workflow
                    /             \
                   v               v
           Business Data       Policy Search
               Tools             Tool
                   |               |
                   v               v
              PostgreSQL       RAG Retriever
              / Supabase           |
                   |               v
                   |          pgvector
                   |               |
                   +-------+-------+
                           |
                           v
                    Answer Generation
                           |
                           v
                    JSON API Response
                           |
                           v
                     Customer UI
```

### Component responsibilities

| Component | Responsibility |
|---|---|
| FastAPI | Receives HTTP requests, validates inputs, and returns responses. |
| LangGraph | Coordinates workflow state, routing, and tool execution. |
| LangChain tools | Provide defined interfaces to business-data and policy-search functions. |
| Database service layer | Executes database queries and returns relevant records. |
| PostgreSQL/Supabase | Stores structured business data and policy vectors. |
| RAG pipeline | Loads, chunks, embeds, indexes, and retrieves policy content. |
| LLM integration | Supports reasoning, structured output, and response generation. |
| Frontend or API client | Sends messages and displays responses. |

## Features

### 1. Structured business-data retrieval

The project uses the Olist Brazilian E-Commerce dataset as sample business data.

Database service functions support lookups involving:

- Customer records
- Orders
- Order items
- Products purchased
- Sellers associated with orders
- Payments
- Reviews

Additional service functions support direct customer, order, product, and order-customer verification lookups.

### 2. Retrieval-Augmented Generation

The policy knowledge base contains Markdown documents covering topics such as:

- Order tracking and cancellation
- Failed orders
- Shipping and delayed delivery
- Lost and damaged packages
- Returns and replacements
- Refunds and payment failures
- Product warranties
- Customer verification
- Escalation and human handoff

The RAG pipeline retrieves relevant policy passages to provide evidence for policy-related answers.

### 3. Tool-enabled agent workflow

The project defines tools for accessing structured business data and searching company policies.

The intended agent workflow selects the operations needed to answer a customer's question rather than querying every data source for every message.

### 4. Structured model output

Pydantic schemas can constrain the model's output to a known set of function names. This helps the application validate the structure of model responses before using them.

Structured output alone does not guarantee that the selected function is appropriate, that the customer is authorized, or that the returned data is correct. Those checks belong in the application.

### 5. FastAPI integration

The API layer provides an HTTP interface for testing through Swagger UI, Postman, Python clients, and browser-based frontends.

### 6. Customer-support evaluation data

CuCom conversation data has been prepared in JSON Lines format for evaluation experiments. Its order identifiers are separate from the Olist dataset and should not be treated as live Olist records.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | HTTP API framework |
| Uvicorn | ASGI server |
| Pydantic | Request validation and structured data |
| LangChain | LLM integration and tool definitions |
| LangGraph | Workflow orchestration and state management |
| Groq | Hosted chat model API |
| SQLAlchemy | Database connectivity and SQL execution |
| PostgreSQL | Relational database |
| Supabase | Hosted PostgreSQL platform |
| pgvector | Vector similarity search |
| Sentence Transformers | Local text embedding generation |
| `python-dotenv` | Environment-variable loading |
| pandas | Dataset inspection and preparation |

The embedding model currently used is `sentence-transformers/all-MiniLM-L6-v2`, which produces 384-dimensional embeddings.

## Project Structure

The following represents the project's observed and intended high-level structure. File names and implementation status may change as development progresses.

```text
Customer_support/
├── api/
│   ├── __init__.py
│   └── main.py
│
├── database/
│   ├── connection.py
│   └── customer_service.py
│
├── graph/
│   ├── __init__.py
│   ├── main.py
│   ├── nodes.py
│   └── state.py
│
├── tools/
│   ├── olist_tools.py
│   ├── rag_tools.py
│   └── test_rag_tools.py
│
├── rag/
│   ├── load_documents.py
│   ├── chunk_documents.py
│   ├── create_embeddings.py
│   ├── ingest_vectors.py
│   ├── retriever.py
│   ├── retriever_test.py
│   └── rag.py
│
├── knowledge/
│   ├── orders/
│   ├── delivery/
│   ├── returns/
│   ├── payments/
│   ├── products/
│   └── support/
│
├── cucom/
│   ├── merged.jsonl
│   └── support_eval.jsonl
│
├── llm.py
├── .env
├── .gitignore
└── README.md
```

**Important:** Never commit `.env`, API keys, database credentials, or private customer information to source control.

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or a version supported by your installed dependencies.
- Git.
- A Supabase PostgreSQL database or another compatible PostgreSQL instance.
- The PostgreSQL `pgvector` extension enabled.
- A Groq API key.
- Internet access for package installation, initial embedding-model downloads, and hosted model calls.

## Installation

The following commands use Windows PowerShell and assume you are working from the repository root.

### Step 1: Clone the repository

```powershell
git clone <YOUR_REPOSITORY_URL>
cd Customer_support
```

Replace the placeholder with your repository URL.

### Step 2: Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

If a `requirements.txt` file exists:

```powershell
python -m pip install -r requirements.txt
```

Otherwise, install the core packages used by the project:

```powershell
python -m pip install fastapi "uvicorn[standard]" pydantic sqlalchemy psycopg2-binary python-dotenv pandas langchain langchain-core langchain-text-splitters langchain-groq langgraph sentence-transformers
```

Create and maintain a dependency file with tested versions so the environment can be reproduced consistently.

### Step 4: Configure environment variables

Create a `.env` file in the project root. See [Environment Configuration](#environment-configuration).

### Step 5: Prepare the database and knowledge base

- Load the Olist business tables into PostgreSQL.
- Enable `pgvector`.
- Create the `knowledge_chunks` table.
- Ingest the policy documents using the RAG pipeline.

See the corresponding sections below.

### Step 6: Start FastAPI

From the repository root:

```powershell
python -m uvicorn api.main:app --reload
```

Once the server starts, visit:

- API root: `http://127.0.0.1:8000/`
- Health endpoint, if defined: `http://127.0.0.1:8000/health`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

The `--reload` flag is for local development, not production.

## Environment Configuration

Create a `.env` file in the project root:

```dotenv
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholders with the credentials from your providers.

The database connection module reads `DATABASE_URL` through `python-dotenv` and SQLAlchemy. The LLM configuration reads `GROQ_API_KEY` and initializes the configured Groq chat model.

The model name is currently configured in `llm.py`. Verify that it is available to your Groq account.

### Security rules

- Do not commit `.env`.
- Do not publish credentials in screenshots, logs, or issue reports.
- Use a separate set of credentials for development and production.
- If a credential is exposed, revoke it and generate a replacement.

## Database Setup

### Olist dataset

The sample database contains the following tables and approximate row counts from the development dataset:

| Table | Approximate rows |
|---|---:|
| `customers` | 99,441 |
| `sellers` | 3,095 |
| `products` | 32,951 |
| `orders` | 99,441 |
| `order_items` | 112,650 |
| `payments` | 103,886 |
| `reviews` | 99,224 |

Counts may vary depending on the loading process.

The tables are related through customer, order, product, seller, payment, and review identifiers. The database service layer uses these relationships to retrieve records associated with a customer.

### Customer identity considerations

In Olist, `customer_id` identifies a customer record associated with an order, while `customer_unique_id` can connect multiple records belonging to the same underlying customer.

Consequently, a query restricted to one `customer_id` may not find every order placed by the same person.

For a real deployment, customer identity must come from authenticated and authorized application context. A customer ID provided by the client must not, by itself, be treated as proof of identity.

### Vector table

The policy knowledge base uses a table similar to:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    chunk_id INTEGER NOT NULL,
    embedding VECTOR(384) NOT NULL
);
```

The 384-dimensional vector column matches the output of `sentence-transformers/all-MiniLM-L6-v2`. If the embedding model changes, the vector dimension and stored embeddings must be updated accordingly.

The retriever uses PostgreSQL vector distance operators, including cosine distance via `<=>`.

## Knowledge Base and RAG

### Pipeline

```text
Markdown policy documents
          |
          v
Load documents
          |
          v
Split into chunks
          |
          v
Generate embeddings
          |
          v
Store content and vectors in PostgreSQL
          |
          v
Retrieve relevant chunks for a query
          |
          v
Use retrieved policy context in answer generation
```

### Chunking configuration

The current text splitter uses:

- Chunk size: `800`
- Chunk overlap: `100`
- Splitter: `RecursiveCharacterTextSplitter`

The retriever requests up to three relevant chunks in the policy-search tool.

### Policy search tool

The `search_company_policy` tool accepts a question and returns relevant policy content, source names, chunk IDs, and similarity scores.

When no relevant content is found, it returns a not-found result rather than policy passages.

Retrieval provides supporting evidence, not a guarantee of correctness. The agent should avoid making unsupported policy claims and should ask clarifying questions or escalate when evidence is insufficient.

### Re-indexing policy documents

When Markdown policy files change, rerun the document-loading, chunking, embedding, and ingestion pipeline as appropriate.

Ensure ingestion handles updates and duplicate records intentionally. Blindly appending every chunk on each run can create duplicate policy entries.

## LangGraph and Agent Tools

The graph layer is intended to orchestrate the conversation workflow using shared state, model calls, routing, and tool execution.

The project has used structured output to select among known function names, including customer/order-related lookups and `search_company_policy`.

### Tool categories

**Business-data tools**

- `lookup_customer`
- `lookup_orders`
- `lookup_order_items`
- `lookup_products`
- `lookup_sellers`
- `lookup_payments`
- `lookup_reviews`

These tools accept a customer identifier and return records associated with that identifier, according to the database service implementation.

**Policy-search tool**

- `search_company_policy`

This tool retrieves relevant passages from the company knowledge base.

The exact tool registry and graph routing should be verified against the current source code.

### State and multi-turn conversations

LangGraph state can hold message history, selected functions, tool results, and other workflow data.

For multi-turn conversations, a checkpointer can persist state across graph invocations. A stable thread or conversation identifier is generally used to resume the correct conversation.

The end of one graph invocation does not necessarily mean the overall customer conversation is finished.

Conversation identifiers must be bound to authenticated users. Never let a caller access another customer's conversation simply by changing the thread ID.

## FastAPI Backend

FastAPI exposes Python functions through HTTP endpoints.

A client sends a request to a URL. FastAPI matches the HTTP method and route, validates the request, calls the endpoint function, and returns a response.

### Example chat request

The exact endpoint contract must match the current implementation in `api/main.py`. A typical chat request might look like:

```http
POST /chat
Content-Type: application/json
```

Request body:

```json
{
  "conversation_id": "conv_123",
  "message": "Where is my order?"
}
```

Example response:

```json
{
  "conversation_id": "conv_123",
  "answer": "The answer generated by the agent..."
}
```

These examples illustrate a possible API contract; verify the actual field names and response format in the current source code.

### Calling FastAPI from a browser frontend

A JavaScript frontend can send a request using `fetch()`:

```javascript
async function sendMessage(message, conversationId) {
  const response = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      message: message
    })
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return await response.json();
}
```

This function sends a JSON request and returns the parsed JSON response. The frontend can then display the answer in the chat interface.

For a browser frontend hosted on a different origin, configure FastAPI CORS for the specific frontend origin. `127.0.0.1` is suitable for local development but is not a public server address.

### Calling FastAPI from Python

A Python script can use the `requests` package:

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={
        "conversation_id": "conv_123",
        "message": "Where is my order?"
    },
    timeout=30
)

response.raise_for_status()
print(response.json())
```

Install `requests` in the client environment if it is not already available.

## Evaluation Dataset

The project includes CuCom customer-support conversation data prepared for evaluation experiments.

| Property | Value |
|---|---|
| Original dataset file | `cucom/merged.jsonl` |
| Normalized file | `cucom/support_eval.jsonl` |
| Approximate conversation count | 6,000 |
| Average conversation length | 11.95 turns |
| Maximum observed turns | 16 |

The role labels have been normalized for evaluation.

**Important:** CuCom contains Amazon-like order identifiers that do not match Olist order identifiers. Use this dataset for dialogue evaluation, not as live Olist business data and not as a source of valid Olist order IDs.

Potential evaluation metrics include:

- Factual correctness
- Policy grounding
- Appropriate tool selection
- Correct use of customer/order records
- Clarification and escalation behavior
- Latency and failure rates

## Testing

### API testing

Start the development server:

```powershell
python -m uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` and execute the endpoints defined by the application.

### RAG testing

Run the retriever and policy-tool tests using the invocation style supported by the current scripts. For example:

```powershell
python -m rag.retriever_test
python -m tools.test_rag_tools
```

These commands assume the scripts are runnable as Python modules from the repository root.

### Recommended additional tests

- Database service functions return the expected records.
- Customer-scoped queries do not expose another customer's data.
- Empty and invalid identifiers are handled correctly.
- Policy retrieval returns relevant sources.
- The graph chooses suitable tools for different customer intents.
- The API validates request bodies and handles errors.
- Conversation history persists only for the correct authorized user.
- Model, database, and retrieval failures produce controlled error responses.

## Troubleshooting

| Problem | What to check |
|---|---|
| `DATABASE_URL not found` | Check that `.env` is in the project root and the variable name is correct. |
| Database connection failure | Verify host, port, username, password, network access, SSL requirements, and connection-string format. |
| Missing vector extension or operator | Enable `pgvector` and verify the table schema. |
| Embedding dimension mismatch | Ensure the embedding model and `VECTOR(...)` column use matching dimensions. |
| No policy results | Check that documents were loaded, chunked, embedded, and ingested; then test the query. |
| Groq authentication error | Verify `GROQ_API_KEY` and model availability. |
| Browser CORS error | Configure CORS for the frontend's actual origin. |
| Import errors | Run commands from the repository root and activate the intended virtual environment. |
| Conversation history disappears | Check graph checkpointer configuration and reuse the same authorized conversation/thread ID. |
| Duplicate knowledge chunks | Review ingestion logic and how existing records are replaced or deduplicated. |

Avoid logging secrets, payment information, or unnecessary customer data while troubleshooting.

## Security Considerations

This project is a development system and should undergo a security review before public or production use.

Before deployment:

- Authenticate users and authorize access to customer records.
- Derive customer identity from trusted authentication context rather than trusting a client-supplied ID.
- Bind conversation IDs to authenticated users.
- Validate inputs and limit request sizes.
- Use HTTPS for deployed environments.
- Store secrets in environment variables or a managed secret store.
- Use least-privilege database credentials and parameterized SQL queries.
- Add rate limits, timeouts, logging, and monitoring.
- Treat customer messages and retrieved documents as untrusted input.
- Do not let model output alone authorize refunds, cancellations, or other sensitive actions.
- Add human approval where high-impact actions require it.
- Define conversation retention and access policies.
- Restrict CORS to known frontend origins.
- Use a production ASGI configuration rather than development reload mode.

## Development Roadmap

The following checklist can be updated as features are completed and tested.

- [ ] Finalize and document the LangGraph state, nodes, and routing.
- [ ] Connect the FastAPI chat endpoint to the compiled graph.
- [ ] Add persistent multi-turn conversations with a checkpointer.
- [ ] Bind conversations to authenticated users.
- [ ] Standardize request/response schemas and API error handling.
- [ ] Add comprehensive database, RAG, graph, and API tests.
- [ ] Implement support-ticket creation and updates.
- [ ] Add human approval for sensitive operations.
- [ ] Build an evaluation harness using `support_eval.jsonl`.
- [ ] Add tracing, metrics, and latency measurement.
- [ ] Build a web chat frontend.
- [ ] Add containerization and deployment configuration.
- [ ] Explore MCP integration for exposing tools through a standard tool protocol.

## Contributing

Contributions and improvements are welcome.

1. Create a feature branch.
2. Keep API, graph, database, tools, and RAG code modular.
3. Add tests for new behavior.
4. Never commit credentials or sensitive customer data.
5. Update this README whenever commands, schemas, endpoints, or architecture change.

## License

No project license has been specified yet. Add a `LICENSE` file before distributing the project or accepting external contributions. Ensure that the Olist and CuCom datasets and all third-party dependencies are used according to their applicable licenses.
