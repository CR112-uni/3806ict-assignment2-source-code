def cegis_proof_repair_loop(initial_proof_script, max_global_attempts=10):
    current_script = initial_proof_script
    attempts = 0
    
    while attempts < max_global_attempts:
        # Step 1: Send the current script to the Isabelle Verification Server
        verification_result = isabelle_server.check_proof(current_script)
        
        # Step 2: Success Condition
        if verification_result.is_successful and not verification_result.contains_sorry():
            return current_script # Proof is complete and verified!
            
        # Step 3: Fill Operation (Handling 'sorry' holes)
        if verification_result.contains_sorry():
            hole = verification_result.get_first_sorry()
            context = extract_subgoal_context(hole)
            # Ask Stepwise Prover to generate a tactic for this specific gap
            patch = stepwise_prover.solve_subgoal(context) 
            current_script = apply_patch_to_script(current_script, hole, patch)
            continue # Re-verify the newly patched script
            
        # Step 4: Repair Operation (Handling outright Isabelle errors/type failures)
        error = verification_result.get_earliest_error()
        
        # Escalate repair strategies based on consecutive failures at the same spot
        failure_streak = track_failures(error.location)
        
        if failure_streak < 3:
            # Stage 1: Local Repair (Fix just the single broken have/show line)
            current_script = perform_stage_1_repair(current_script, error, llm)
            
        elif failure_streak < 6:
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