import ollama, chromadb
import sys
from pathlib import Path

# constants
DB_DIR = "./vault_db"
LLM_MODEL = "qwen2.5-coder:3b"

# setup chromadb
chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_or_create_collection("obsidian_notes")

# md insertion into db
def index_vault(vault_path):
	# safety guard
	vault_dir = Path(vault_path)
	if not vault_dir.is_dir():
		print(f"File not found or is not a file: {vault_path}")
		return
	# Find md files
	md_files = list(vault_dir.rglob("*.md")) #glob returns generator
	print(f"Found {len(md_files)} markdown files. Indexing...")

	# Example md contents
	# Project Alpha
		# This is the main overview for Project Alpha. It starts on November 1st.

		# ## Server Architecture
		# We are using a microservices approach. 
		# - Auth service runs on port 8080.
		# - Payment service runs on port 9090.

		# ## Database Secrets
		# The production database uses port 5432 with peer authentication. 
		# Never commit the password to GitHub.

		# ## Workouts
		# Leg day is Tuesday and chest day is Thursday. Do not skip.

	# read md files
	count = 0
	for file_path in md_files:
		filename = file_path.stem # name without extension - used for later part

		with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
			content = f.read()
		
		# preparation of md contents
		raw_sections = content.split("\n#")
		for idx, sec in enumerate(raw_sections):
			sec_text = sec.strip()
			if not sec_text:
				continue
			heading = sec_text.split("\n")[0].replace("#","").strip() or "General"
			full_text = f"[[{filename}#{heading}]]\n{sec_text}"

			# vectorization of md
			emb = ollama.embed(model="nomic-embed-text", input=full_text)["embeddings"]
			# db insertion
			collection.upsert(
				ids=[f"{filename}_{idx}"],
				embeddings=emb,
				documents=[full_text],
				metadatas=[{"file": filename, "heading": heading}]
			)
			count += 1

	# insertion summary
	print(f"Indexed {count} note sections into local ChromaDB.")

# question query + context prompt
def search_vault(query):
	# vectorization of question
	q_emb = ollama.embed(model="nomic-embed-text", input=query)["embeddings"]
	# question query
	results = collection.query(
		query_embeddings=q_emb,
		n_results=2
	)
	docs = results["documents"][0]

	if not docs:
		print("No matching notes found.")
		return

	# context prompt
	context = "\n\n---\n\n".join(docs)
	prompt = (
		f"Answer the user query based ONLY on the Obsidian notes below. "
        f"Always reference the note using Obsidian wiki-links (e.g. [[Note#Heading]]).\n\n"
        f"Notes:\n{context}\n\n"
        f"Question: {query}\nAnswer:"
	)

	print("\nAI > ", end="", flush=True)
	stream = ollama.generate(model=LLM_MODEL, prompt=prompt, stream=True)
	for chunk in stream:
		print(chunk["response"], end="", flush=True)
	print()

# program argument
if __name__	== "__main__":
	# ingest md
	if len(sys.argv) > 1 and Path(sys.argv[1]).is_dir():
		index_vault(sys.argv[1])

	print("--- Obsidian Vault Search Ready (Type 'exit' to quit) ---")
	while True:
		q = input("\nQuery Vault > ").strip()
		if q.lower() in ("quit", "exit"):
			break
		if q:
			search_vault(q)



