import ollama, chromadb
import pprint

# setup chromadb
client = chromadb.Client()
collection = client.get_or_create_collection("vault_skeleton")

# notes and preparation
sample_note = """
# Project Titan
The server migration to Singapore region completed on August 15.
# Database Secrets
The production database uses port 5432 with peer authentication.
# Workouts
Leg day is Tuesday and chest day is Thursday.
"""

sections = [s.strip() for s in sample_note.split("# ") if s.strip()]

for i, sec in enumerate(sections):
	title = sec.split("\n")[0]
	# vectorization
	emb = ollama.embed(model="nomic-embed-text", input=sec)["embeddings"]
	# db insertion
	collection.add(ids=[str(i)], embeddings=emb, documents=[sec], metadatas=[{"heading":title}]) # there is no single correct schema for metadatas criterias

# question and preparation
q = "Where did we migrate our servers?"
# vectorization
q_emb = ollama.embed(model="nomic-embed-text", input=q)["embeddings"]
# query
match = collection.query(query_embeddings=q_emb, n_results=1)

# output observation
# print(match)
# print()
# pprint.pprint(match) # using ppprint to prettify output

# question + answer presentation
print(f"Matched Section: [[{match['metadatas'][0][0]['heading']}]]")
print(f"Content: {match['documents'][0][0]}")

