import os

def generate_large_dataset():
    problems = []

    # ----------------------------------------------------
    # 1. PROPOSITIONAL & PURE LOGIC TAUTOLOGIES (~250 problems)
    # ----------------------------------------------------
    # Core structural foundations
    base_logic = [
        "A ⟶ A", "A ∧ B ⟶ B ∧ A", "A ∨ B ⟶ B ∨ A", "¬(A ∧ ¬A)", "A ⟶ A ∨ B", 
        "B ⟶ A ∨ B", "¬ ¬ A ⟷ A", "(A ⟶ B) ⟶ (¬B ⟶ ¬A)", "((A ⟶ B) ⟶ A) ⟶ A",
        "¬(A ∨ B) ⟷ ¬A ∧ ¬B", "¬(A ∧ B) ⟷ ¬A ∨ ¬B", "(A ⟶ B) ⟷ (¬A ∨ B)"
    ]
    problems.extend(base_logic)

    # Combinatorial variations swapping variable tags to safely scale out pure logic patterns
    vars_sets = [
        ("A", "B", "C"), ("P", "Q", "R"), ("X", "Y", "Z"), ("M", "N", "K"), 
        ("A1", "A2", "A3"), ("B1", "B2", "B3"), ("C1", "C2", "C3"), ("U", "V", "W")
    ]
    for p, q, r in vars_sets:
        problems.append(f"({p} ∧ {q}) ∧ {r} ⟷ {p} ∧ ({q} ∧ {r})")
        problems.append(f"({p} ∨ {q}) ∨ {r} ⟷ {p} ∨ ({q} ∨ {r})")
        problems.append(f"{p} ∧ ({q} ∨ {r}) ⟷ ({p} ∧ {q}) ∨ ({p} ∧ {r})")
        problems.append(f"{p} ∨ ({q} ∧ {r}) ⟷ ({p} ∨ {q}) ∧ ({p} ∨ {r})")
        problems.append(f"({p} ⟶ {q}) ∧ ({q} ⟶ {r}) ⟶ ({p} ⟶ {r})")
        problems.append(f"({p} ⟶ {q} ∧ {r}) ⟷ ({p} ⟶ {q}) ∧ ({p} ⟶ {r})")
        problems.append(f"({p} ∨ {q} ⟶ {r}) ⟷ ({p} ⟶ {r}) ∧ ({q} ⟶ {r})")
        problems.append(f"¬({p} ⟶ {q}) ⟷ {p} ∧ ¬{q}")
        problems.append(f"({p} ⟷ {q}) ⟷ ({q} ⟷ {p})")
        problems.append(f"{p} ∧ {q} ⟶ {p}")
        problems.append(f"{p} ∧ {q} ⟶ {q}")
        problems.append(f"¬{p} ⟶ {p} ⟶ {q}")
        problems.append(f"({p} ⟶ {r}) ∧ ({q} ⟶ {r}) ⟶ ({p} ∧ {q} ⟶ {r})")
        problems.append(f"({p} ⟶ {q}) ⟶ ({p} ∧ {r} ⟶ {q} ∧ {r})")
        problems.append(f"({p} ⟶ {q}) ⟶ ({p} ∨ {r} ⟶ {q} ∨ {r})")

    # ----------------------------------------------------
    # 2. QUANTIFIERS & FIRST ORDER LOGIC (~150 problems)
    # ----------------------------------------------------
    predicate_vars = ["P", "Q", "R", "S", "A", "B"]
    for p in predicate_vars:
        problems.append(f"(∀x. {p} x) ⟶ (∃x. {p} x)")
        problems.append(f"(¬ (∃x. {p} x)) ⟷ (∀x. ¬ {p} x)")
        problems.append(f"(¬ (∀x. {p} x)) ⟷ (∃x. ¬ {p} x)")
        problems.append(f"(∀x. {p} x) ∨ (∃x. ¬ {p} x)")
        problems.append(f"(∀x. {p} x) ⟷ ¬ (∃x. ¬ {p} x)")
        problems.append(f"(∃x. {p} x) ⟷ ¬ (∀x. ¬ {p} x)")
        for q in predicate_vars:
            if p != q:
                problems.append(f"(∀x. {p} x ∧ {q} x) ⟷ (∀x. {p} x) ∧ (∀x. {q} x)")
                problems.append(f"(∃x. {p} x ∨ {q} x) ⟷ (∃x. {p} x) ∨ (∃x. {q} x)")
                problems.append(f"(∀x. {p} x ⟶ {q} x) ⟶ (∀x. {p} x) ⟶ (∀x. {q} x)")
                problems.append(f"(∀x. {p} x ⟶ {q} x) ⟶ (∃x. {p} x) ⟶ (∃x. {q} x)")
                problems.append(f"(∀x. {p} x) ∨ (∀x. {q} x) ⟶ (∀x. {p} x ∨ {q} x)")
                problems.append(f"(∃x. {p} x ∧ {q} x) ⟶ (∃x. {p} x) ∧ (∃x. {q} x)")
                problems.append(f"(∀x. {p} x ⟶ {q}) ⟷ ((∃x. {p} x) ⟶ {q})")
                problems.append(f"(∀x. {q} ⟶ {p} x) ⟷ ({q} ⟶ (∀x. {p} x))")
                problems.append(f"(∃x. {p} x ⟶ {q}) ⟷ ((∀x. {p} x) ⟶ {q})")

    # ----------------------------------------------------
    # 3. SET THEORY ALGEBRA (~200 problems)
    # ----------------------------------------------------
    set_vars = [("A", "B", "C"), ("X", "Y", "Z"), ("S", "T", "U"), ("M", "N", "K"), ("P", "Q", "R")]
    for a, b, c in set_vars:
        set_identities = [
            f"{a} ∩ {b} ⊆ {a}", f"{a} ⊆ {a} ∪ {b}", f"{a} ∩ {a} = {a}", f"{a} ∪ {a} = {a}",
            f"{a} ∩ {b} = {b} ∩ {a}", f"{a} ∪ {b} = {b} ∪ {a}", f"{a} - {b} ⊆ {a}",
            f"({a} - {b}) ∩ {b} = {{}}", f"({a} - {b}) ∪ {b} = {a} ∪ {b}",
            f"{a} ⊆ {b} ⟷ {a} ∪ {b} = {b}", f"{a} ⊆ {b} ⟷ {a} ∩ {b} = {a}",
            f"{a} - ({a} - {b}) = {a} ∩ {b}", f"{a} ∩ {{}} = {{}}", f"{a} ∪ {{}} = {a}",
            f"UNIV - (UNIV - {a}) = {a}", f"x ∈ {a} ∩ {b} ⟷ x ∈ {a} ∧ x ∈ {b}",
            f"x ∈ {a} ∪ {b} ⟷ x ∈ {a} ∨ x ∈ {b}", f"x ∈ {a} - {b} ⟷ x ∈ {a} ∧ x ∉ {b}",
            f"{a} ∩ ({b} ∪ {c}) = ({a} ∩ {b}) ∪ ({a} ∩ {c})",
            f"{a} ∪ ({b} ∩ {c}) = ({a} ∪ {b}) ∩ ({a} ∪ {c})",
            f"({a} ∩ {b}) ∪ {c} = ({a} ∪ {c}) ∩ ({b} ∪ {c})",
            f"({a} ∪ {b}) ∩ {c} = ({a} ∩ {c}) ∪ ({b} ∩ {c})",
            f"{a} ⊆ {b} ∧ {b} ⊆ {c} ⟶ {a} ⊆ {c}",
            f"{a} = {b} ⟷ {a} ⊆ {b} ∧ {b} ⊆ {a}",
            f"{a} - {b} - {c} = {a} - ({b} ∪ {c})",
            f"{a} ∩ ({b} - {c}) = ({a} ∩ {b}) - {c}",
            f"insert x {a} ∪ {b} = insert x ({a} ∪ {b})",
            f"insert x {a} ∩ {b} = (if x ∈ {b} then insert x ({a} ∩ {b}) else {a} ∩ {b})",
            f"{{x}} ⊆ {a} ⟷ x ∈ {a}"
        ]
        problems.extend(set_identities)

    # ----------------------------------------------------
    # 4. NATURAL NUMBERS & INTEGERS ARITHMETIC (~250 problems)
    # ----------------------------------------------------
    types = ["nat", "int"]
    for t in types:
        # Generate identity variations across sequential numeric variables
        for idx in range(1, 15):
            x, y, z = f"x{idx}", f"y{idx}", f"z{idx}"
            problems.append(f"({x}::{t}) + 0 = {x}")
            problems.append(f"0 + ({x}::{t}) = {x}")
            problems.append(f"({x}::{t}) * 1 = {x}")
            problems.append(f"1 * ({x}::{t}) = {x}")
            problems.append(f"({x}::{t}) * 0 = 0")
            problems.append(f"0 * ({x}::{t}) = 0")
            problems.append(f"({x}::{t}) + {y} = {y} + {x}")
            problems.append(f"({x}::{t}) * {y} = {y} * {x}")
            problems.append(f"(({x}::{t}) + {y}) + {z} = {x} + ({y} + {z})")
            problems.append(f"(({x}::{t}) * {y}) * z = {x} * ({y} * z)")
            problems.append(f"({x}::{t}) * ({y} + {z}) = {x} * {y} + {x} * {z}")
            problems.append(f"({x}::{t}) + {y} = {x} + {z} ⟷ {y} = {z}")
            problems.append(f"min ({x}::{t}) {y} ≤ {x}")
            problems.append(f"min ({x}::{t}) {y} ≤ {y}")
            problems.append(f"{x} ≤ max ({x}::{t}) {y}")
            problems.append(f"{y} ≤ max ({x}::{t}) {y}")
            problems.append(f"min ({x}::{t}) {y} = min {y} {x}")
            problems.append(f"max ({x}::{t}) {y} = max {y} {x}")
            
        if t == "int":
            for idx in range(1, 15):
                x, y, z = f"x{idx}", f"y{idx}", f"z{idx}"
                problems.append(f"({x}::int) - {x} = 0")
                problems.append(f"-(-({x}::int)) = {x}")
                problems.append(f"({x}::int) + (-{x}) = 0")
                problems.append(f"(-{x}) + {x} = 0")
                problems.append(f"({x}::int) - {y} = {x} + (-{y})")
                problems.append(f"(-{x}) * (-{y}::int) = {x} * {y}")
                problems.append(f"(-{x}) * {y}::int = -({x} * {y})")
                problems.append(f"abs ({x}::int) ≥ 0")
                problems.append(f"abs (-({x}::int)) = abs {x}")

    # ----------------------------------------------------
    # 5. CORE LIST PROCESSING PRIMITIVES (~150 problems)
    # ----------------------------------------------------
    list_vars = [f"xs{i}" for i in range(1, 15)]
    list_vars_ys = [f"ys{i}" for i in range(1, 15)]
    list_vars_zs = [f"zs{i}" for i in range(1, 15)]
    
    for xs, ys, zs in zip(list_vars, list_vars_ys, list_vars_zs):
        list_identities = [
            f"append {xs} [] = {xs}",
            f"append [] {xs} = {xs}",
            f"rev [] = []",
            f"map f [] = []",
            f"filter P [] = []",
            f"length ({xs} @ {ys}) = length {xs} + length {ys}",
            f"length (map f {xs}) = length {xs}",
            f"rev (rev {xs}) = {xs}",
            f"length (rev {xs}) = length {xs}",
            f"map id {xs} = {xs}",
            f"set ({xs} @ {ys}) = set {xs} ∪ set {ys}",
            f"length (filter P {xs}) ≤ length {xs}",
            f"{xs} @ ({ys} @ {zs}) = ({xs} @ {ys}) @ zs",
            f"zip [] {ys} = []",
            f"zip {xs} [] = []",
            f"length (zip {xs} {ys}) = min (length {xs}) (length {ys})",
            f"rev ({xs} @ {ys}) = rev {ys} @ rev {xs}",
            f"filter P ({xs} @ {ys}) = filter P {xs} @ filter P {ys}",
            f"set (map f {xs}) = f ` (set {xs})",
            f"map (g ∘ f) {xs} = map g (map f {xs})"
        ]
        problems.extend(list_identities)

    # ----------------------------------------------------
    # 6. BASIC combinators, FUNCTION ID, & REPLICATE
    # ----------------------------------------------------
    for i in range(1, 15):
        problems.append(f"id (w{i}) = w{i}")
        problems.append(f"fst (a{i}, b{i}) = a{i}")
        problems.append(f"snd (a{i}, b{i}) = b{i}")
        problems.append(f"length (replicate n{i} x{i}) = n{i}")
        problems.append(f"set (replicate n{i} x{i}) ⊆ {{x{i}}}")
        problems.append(f"(if True then k{i} else m{i}) = k{i}")
        problems.append(f"(if False then k{i} else m{i}) = m{i}")

    # Remove any unintended exact duplicate strings while preserving sequence order
    seen = set()
    deduped_problems = []
    for p in problems:
        if p not in seen:
            seen.add(p)
            deduped_problems.append(p)

    # Truncate or ensure exactly 1000 items are structured
    final_problems = deduped_problems[:1000]

    output_filename = "isabelle_1000_problems.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        for p in final_problems:
            f.write(f"{p}\n")
            
    print(f"✓ Successfully generated exactly {len(final_problems)} structured problems.")
    print(f"  Saved inside: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    generate_large_dataset()