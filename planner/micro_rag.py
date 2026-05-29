def retrieve_micro_rag_context(current_subgoal, afp_index, top_k=5):
    # Step 1: Convert the text of the subgoal into a vector embedding
    goal_embedding = sentence_transformer.encode(current_subgoal)
    
    # Step 2: Search the pre-compiled AFP database for closest matches
    # (Uses Cosine Similarity to find overlaps in mathematical structure)
    similar_lemmas = afp_index.search(goal_embedding, limit=top_k)
    
    # Step 3: Format the retrieved lemmas into a context string
    rag_context = "Helpful Lemmas from AFP:\n"
    for lemma in similar_lemmas:
        rag_context += f"- {lemma.name}: {lemma.statement}\n"
        
    return rag_context

def generate_proof_step(subgoal, ...):
    # Fetch context before asking the LLM
    context = retrieve_micro_rag_context(subgoal, global_afp_index)
    
    # Inject the RAG context directly into the LLM prompt
    prompt = f"{context}\nSolve the following Isabelle/HOL goal:\n{subgoal}"
    return llm.generate(prompt)