def cegis_proof_repair_loop(initial_proof_script, max_global_attempts = 10):
    current_script = initial_proof_script
    attempts = 0
    
    while (attempts < max_global_attempts):
        verification_result = isabelle_server.check_proof(current_script)
        
        if (verification_result.is_successful and not verification_result.contains_sorry()):
            return (current_script)
            
        if (verification_result.contains_sorry()):
            hole = verification_result.get_first_sorry()
            context = extract_subgoal_context(hole)
            # Ask Prover to generate a tactic for this gap
            patch = stepwise_prover.solve_subgoal(context) 
            current_script = apply_patch_to_script(current_script, hole, patch)
            continue
            
        error = verification_result.get_earliest_error()
        
        # Escalate repair strategies based on consecutive failures at the same spot
        failure_streak = track_failures(error.location)
        
        if (failure_streak < 3):
            # Stage 1: Local Repair (Fix just the single broken have/show line)
            current_script = perform_stage_1_repair(current_script, error, llm)
            
        elif (failure_streak < 6):
            # Stage 2: Subproof Repair (Regenerate the whole inner block/case branch)
            current_script = perform_stage_2_repair(current_script, error, llm)
            
        else:
            # Stage 3: Whole Proof Repair (Scrap it and try a new global approach)
            current_script = perform_stage_3_repair(current_script, error, llm)
            
        attempts += 1
        
    return "FAILED: Global timeout reached."

def perform_stage_1_repair(script, error, llm):
    # Prompt the LLM with the exact error message and the broken line
    prompt = f"Isabelle threw this error: {error.message}. Fix this specific line: {error.line_text}"
    new_line = llm.generate(prompt)
    return replace_line(script, error.line_number, new_line)
