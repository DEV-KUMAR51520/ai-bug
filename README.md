# 🐛 AI Bug Hunter

> **An Agentic AI system that detects bugs in code using a multi-agent reasoning pipeline powered by Groq LLMs and vector-based knowledge retrieval.**



## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [System Architecture](#-system-architecture)
- [Agent Pipeline](#-agent-pipeline)
- [MCP Tool Server](#-mcp-tool-server)
- [Vector Retrieval System](#-vector-retrieval-system)
- [Data Flow](#-data-flow)
- [Project Structure](#-project-structure)
- [Key Technologies](#-key-technologies)
- [Example Output](#-example-output)
- [Future Improvements](#-future-improvements)
- [Use Cases](#-use-cases)
- [Author](#-author)

---

## 🔍 Overview

**AI Bug Hunter** is a multi-agent AI debugging system that automatically:

- 🔎 **Detects** suspicious and buggy lines in source code
- 📚 **Retrieves** relevant documentation using RAG (Retrieval Augmented Generation)
- 💡 **Explains** bugs in concise, developer-friendly language

The system combines **Agentic AI architecture**, **LLM reasoning**, **vector embeddings**, and **MCP tool integration** to create an intelligent, automated debugging pipeline.

---

## ❗ Problem Statement

Debugging large codebases is time-consuming and requires deep contextual knowledge of APIs and documentation.

Traditional static analysis tools often fail to understand:

| Challenge | Description |
|-----------|-------------|
| 🧠 Semantic Intent | The *purpose* behind code, not just syntax |
| 📖 Documentation References | Linking bugs to relevant API docs |
| 🌐 Contextual Bugs | Bugs that only manifest in specific usage contexts |

**AI Bug Hunter** addresses this with a multi-agent reasoning pipeline that combines LLM intelligence with vector-based knowledge retrieval.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     AI BUG HUNTER                       │
│                  Multi-Agent Pipeline                   │
└─────────────────────────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Dataset    │
                    │  (CSV)      │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │Orchestrator │
                    │(Coordinates │
                    │  Agents)    │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
   ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
   │   PARSER    │  │  VALIDATOR  │  │  EXPLAINER  │
   │   AGENT     │  │   AGENT     │  │   AGENT     │
   │             │  │             │  │             │
   │ Detects     │  │ Retrieves   │  │ Generates   │
   │ Buggy Lines │  │ Relevant    │  │ Bug         │
   │             │  │ Docs        │  │ Explanation │
   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
          │                │                │
          │         ┌──────▼──────┐         │
          │         │ MCP Client  │         │
          │         └──────┬──────┘         │
          │                │                │
          │         ┌──────▼──────┐         │
          │         │ MCP Server  │         │
          │         │ (FastMCP)   │         │
          │         └──────┬──────┘         │
          │                │                │
          │         ┌──────▼──────┐         │
          │         │   Vector    │         │
          │         │  Database   │         │
          │         │(LlamaIndex) │         │
          │         └─────────────┘         │
          │                                 │
          └──────────────┬──────────────────┘
                         │
                  ┌──────▼──────┐
                  │ Output CSV  │
                  │(Bug Report) │
                  └─────────────┘
```

---

## 🤖 Agent Pipeline

The system uses **three specialized agents**, each with one focused responsibility:

### 1. 🔬 Parser Agent

Analyzes raw source code to identify suspicious lines.

```
Input:  Numbered source code lines
          │
          ▼
      Groq LLM
      (Code Analysis)
          │
          ▼
Output: [buggy_line_numbers]
```

- Uses **Groq LLM** for intelligent code inspection
- Returns line numbers of likely bugs
- Narrows debugging focus for downstream agents

---

### 2. ✅ Validator Agent

Retrieves relevant technical documentation to support bug analysis.

```
Input:  Code context + buggy line
          │
          ▼
      MCP Client
          │
          ▼
      MCP Server
      (FastMCP Tool)
          │
          ▼
    Vector Retrieval
    (LlamaIndex + BAAI embeddings)
          │
          ▼
Output: Top-K relevant documents
```

- Queries the **vector knowledge base** via MCP server
- Returns semantically similar documentation chunks
- Provides grounding context to the Explainer Agent

---

### 3. 💬 Explainer Agent

Generates a single, concise bug explanation from all available context.

```
Inputs:
  ├── Original source code
  ├── Identified buggy line(s)
  └── Retrieved documentation
          │
          ▼
      Groq LLM
      (Reasoning)
          │
          ▼
Output: One-sentence bug explanation
```

**Example Output:**
```
"Missing semicolon after variable declaration on line 5"
```

---

## 🛠️ MCP Tool Server

The system includes a **FastMCP tool server** that exposes modular tools to agents.

| Tool | Description |
|------|-------------|
| `add()` | Addition utility |
| `multiply()` | Multiplication utility |
| `sine()` | Sine function |
| `list_files_and_folders()` | Filesystem introspection |
| `search_documents()` | ⭐ **Core RAG retrieval tool** |

The most critical tool is `search_documents()`, which performs **semantic similarity search** over the indexed documentation corpus.

```python
# Example MCP tool invocation
result = mcp_client.call("search_documents", query="null pointer dereference C++")
# Returns: Top-K semantically relevant documentation chunks
```

---

## 🔮 Vector Retrieval System

The knowledge retrieval backbone uses **LlamaIndex** for document indexing and semantic search.

```
Query String
     │
     ▼
┌─────────────────────┐
│  Embedding Model    │
│  BAAI/bge-base-     │
│  en-v1.5            │
│  (HuggingFace)      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Vector Similarity  │
│  Search             │
│  (Cosine Distance)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Top-K Documents    │
│  (Ranked Results)   │
└─────────────────────┘
```

**Why `BAAI/bge-base-en-v1.5`?**

- ✅ High-quality semantic embeddings
- ✅ Strong performance on retrieval benchmarks
- ✅ Optimized for RAG pipelines
- ✅ Efficient inference speed

---

## 🔄 Data Flow

Complete end-to-end execution trace:

```
Step 1: Load CSV dataset
         │
         ▼
Step 2: Iterate each code sample
         │
         ▼
Step 3: Parser Agent
         → Analyze code with Groq LLM
         → Return buggy line numbers
         │
         ▼
Step 4: Validator Agent
         → Build semantic query from context
         → Call MCP search_documents tool
         → Retrieve top-K relevant docs
         │
         ▼
Step 5: Explainer Agent
         → Combine code + bug line + docs
         → Generate one-sentence explanation via Groq LLM
         │
         ▼
Step 6: Append result to output CSV
         │
         ▼
Step 7: Repeat for all samples → Final CSV report
```

---

## 📁 Project Structure

```
ai-bug-hunter/
│
├── agents/
│   ├── parser_agent.py        # Detects suspicious code lines
│   ├── validator_agent.py     # Retrieves relevant documentation
│   └── explainer_agent.py     # Generates bug explanations
│
├── tools/
│   └── mcp_client.py          # MCP tool client interface
│
├── server/
│   ├── embedding_model/       # BAAI embedding model files
│   └── storage/               # LlamaIndex vector store
│
├── orchestrator.py            # Coordinates agent pipeline
├── main.py                    # Entry point
├── config.py                  # API keys & configuration
├── samples.csv                # Input dataset
├── output.csv                 # Generated bug reports
└── README.md
```

---

## ⚙️ Key Technologies

| Technology | Role | Why |
|------------|------|-----|
| **Groq API** | LLM inference | Ultra-low latency, high throughput — ideal for agent loops |
| **LlamaIndex** | Vector retrieval & RAG | Production-grade document indexing and semantic search |
| **FastMCP** | Tool server framework | Modular, fast tool exposure for agent use |
| **HuggingFace** | Embedding model hosting | Access to `BAAI/bge-base-en-v1.5` |
| **Pandas** | Dataset processing | Efficient CSV I/O and tabular manipulation |
| **Python 3.10+** | Core runtime | Async support, type hints, modern tooling |

---

## 📊 Example Output

### Input (`samples.csv`)
```csv
ID,Code,Description
1,"int x = 5\nprintf('%d', x)","Print integer variable"
2,"void foo() {\n  int* p;\n  *p = 10;\n}","Assign via pointer"
```

### Output (`output.csv`)
```csv
ID,Bug Line,Explanation
1,1,Missing semicolon after variable declaration on line 1
2,3,Dereferencing uninitialized pointer p causes undefined behavior
```

---

## 🚀 Future Improvements

- [ ] **Parallel agent execution** — run Parser and Validator concurrently to reduce latency
- [ ] **LLM response caching** — avoid redundant API calls for identical inputs
- [ ] **Improved bug classification** — categorize bugs (memory, logic, syntax, concurrency)
- [ ] **Confidence scoring** — attach a confidence probability to each detected bug
- [ ] **Automated code repair suggestions** — generate fixed code alongside explanations
- [ ] **UI dashboard** — visual interface for browsing and filtering bug reports
- [ ] **Multi-language support** — extend beyond C++ to Python, Java, Rust

---

## 💼 Use Cases

| Use Case | Description |
|----------|-------------|
| 🤖 Automated Debugging | Scan large codebases for bugs without human intervention |
| 🔍 AI-Powered Code Review | Augment PR reviews with intelligent bug detection |
| ⚡ Developer Productivity | Speed up debugging cycles during development |
| 📐 Intelligent Static Analysis | Context-aware analysis beyond traditional linters |

---


⚠⚠⚠ NOTE:
THE MCP SERVER IS DEPLOYED ON RENDER ON A FREE VERSION AND WITH INACTIVITY THE FREE INSTANCE WILL SPIN DOWN, AND IT CAN DELAY THE REQUESTS BY 50s OR MORE.


## 👤 Author

**Dev Kumar**
*AI Engineer & Developer*

Focused on building agentic AI systems, developer tools, and intelligent automation pipelines.