# 🦘 Personal Knowledge Base RAG (Obsidian Semantic Search)

A fully local, private, header-aware Retrieval-Augmented Generation (RAG) pipeline. This tool indexes a directory of Markdown notes, chunks them by semantic headers, and allows you to query your notes using a local LLM that cites its sources using native Obsidian wiki-links.

## ✨ Features

*   **Header-Aware Chunking:** Instead of blindly slicing text at character limits, this pipeline splits notes by Markdown headers (`#`, `##`). This ensures every chunk is a self-contained idea with natural context.
*   **Semantic Search:** Uses `nomic-embed-text` to convert text into mathematical vectors for cosine similarity search.
*   **Obsidian Integration:** The LLM is prompted to cite its source using native wiki-links (e.g., `[[NoteName#Heading]]`), allowing for instant click-through navigation in Obsidian.
*   **Hallucination Guardrails:** The prompt strictly limits the LLM to the retrieved context. If the answer isn't in your notes, it will refuse to answer.
*   **Persistent Local DB:** Uses ChromaDB to save vectors locally so you only have to index your vault once.
*   **Robust File Handling:** Uses modern Python `pathlib` and `errors="ignore"` to ensure the indexing pipeline never crashes on weirdly encoded files or emojis.

---

## 🔄 The RAG Data Flow

Here is exactly how data moves through the system, from raw Markdown files to AI-generated answers.

```mermaid
flowchart LR
    A[Markdown Vault] -->|1. Read & Split on #| B(Header Chunks)
    B -->|2. Ollama: nomic-embed-text| C{Vector Embeddings}
    C -->|3. Upsert| D[(ChromaDB\nvault_db)]
    
    Q[User Query] -->|4. Ollama: nomic-embed-text| QE{Query Vector}
    QE -->|5. Cosine Similarity| D
    D -->|6. Top 2 Matches| P[Context + Prompt]
    Q --> P
    P -->|7. Ollama: qwen2.5-coder:3b| AI[Final Answer with\n[[Wiki-Links]]]
```

### Step-by-Step Breakdown:
1.  **Scan:** Recursively scans the target folder for `.md` files using `Path().rglob()`.
2.  **Chunk:** Splits the content on newlines followed by a hash (`\n#`).
3.  **Clean:** Extracts the heading, strips the hashes, and formats the chunk as `[[filename#heading]] + raw_text`.
4.  **Embed:** Sends the chunk to `nomic-embed-text` via Ollama to generate a vector array.
5.  **Store:** Saves the vector, text, and metadata (filename, heading) into ChromaDB using `upsert` (to prevent crashes on re-indexing).
6.  **Query:** Takes a user question, embeds it, and performs a cosine similarity search against ChromaDB.
7.  **Generate:** Feeds the top 2 matching chunks into `qwen2.5-coder:3b` with strict instructions to answer only from the provided context and cite the wiki-link.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.10+ 
*   **Local AI Engine:** [Ollama](https://ollama.com/)
*   **Embedding Model:** `nomic-embed-text`
*   **LLM:** `qwen2.5-coder:3b` (or `llama3.2:3b`)
*   **Vector Database:** `chromadb`
*   **File System:** `pathlib`

---

## 🚀 Setup & Installation

**1. Install and start Ollama**
Ensure Ollama is running locally, then pull the required models:
```bash
ollama pull nomic-embed-text
ollama pull qwen2.5-coder:3b
```

**2. Clone the repo and set up the environment**
```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install ollama chromadb
```

**3. Prepare your Markdown files**
Create a folder named `notes` (or point to your actual Obsidian vault) and drop some `.md` files inside.

**4. Run the script**
Pass the path to your Markdown folder as an argument:
```powershell
python vault_search.py ./notes
```

*(If you run the script without a path argument later, it will skip indexing and jump straight to the query prompt, using the database you already built.)*

---

## 🧠 Lessons Learned & Design Choices

Building this pipeline from scratch surfaced a ton of real-world debugging scenarios. Here is a comprehensive log of the obstacles conquered and the concepts mastered during development.

### 💥 Code Bugs & Debugging
*   **The 3D Array Error:** Hit `ValueError: Expected embeddings to be a list... got [[[...]]]` twice. *Realization: The modern `ollama.embed()` API returns a list of lists. Wrapping it in brackets `[emb]` creates a 3D array. ChromaDB only wants a 2D array.*
*   **The Nested Output Hierarchy:** ChromaDB returns `[0]` results wrapped in lists to support batch queries. *Realization: Learned to use `pprint(match)` to visualize the raw data structure and "unpack" the data safely before writing final print statements.*

### 🧠 Core RAG Concepts
*   **`add` vs. `upsert`:** *Realization: `add` is strict and crashes on duplicate IDs. `upsert` (Update + Insert) is mandatory for persistent databases so re-indexing doesn't crash the script.*
*   **Metadata Criteria:** *Realization: Metadata schemas are subjective, but should always be designed based on what you intend to filter by later (e.g., `heading`, `file`).*

### 🐍 Modern Python & File System Mastery
*   **`pathlib` vs. `os` & `glob`:** Replaced the old way with `Path(vault_path).rglob("*.md")` and `.stem`. *Realization: `rglob()` returns a memory-efficient generator, but needs `list()` if you want to use `len()`.*
*   **`errors="ignore"`:** Spotted in the `open()` function. *Realization: It's a survival tactic. It prevents a single emoji or weirdly encoded character from crashing the entire indexing pipeline with a `UnicodeDecodeError`.*
*   **`open()` Flexibility:** *Realization: `open()` accepts both strings and `Path` objects seamlessly.*