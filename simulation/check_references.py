import re
import sys
import os

def check_tex_integrity(tex_file, log_file):
    if not os.path.exists(tex_file):
        print(f"Error: {tex_file} not found.")
        return
    if not os.path.exists(log_file):
        print(f"Error: {log_file} not found.")
        return

    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        log_content = f.read()

    print("=== 1. Reference Integrity Check ===")
    # Extract defined labels
    labels = set(re.findall(r'\\label\{([^}]+)\}', content))
    # Extract referenced labels
    refs = set(re.findall(r'\\ref\{([^}]+)\}', content))
    
    missing_refs = refs - labels
    if missing_refs:
        print(f"❌ CRITICAL: Undefined references found: {missing_refs}")
    else:
        print("✅ All \\ref targets are defined.")

    # Check for undefined citations
    cites = set()
    for m in re.finditer(r'\\cite\{([^}]+)\}', content):
        # Handle multiple citations like \cite{a,b}
        for c in m.group(1).split(','):
            cites.add(c.strip())

    # Simple bibitem extraction
    bibitems = set(re.findall(r'\\bibitem\{([^}]+)\}', content))
    
    missing_cites = cites - bibitems
    if missing_cites:
        print(f"❌ CRITICAL: Undefined citations found: {missing_cites}")
    else:
        print("✅ All \\cite targets are defined.")

    print("\n=== 2. LaTeX Log Warning Check ===")
    warnings = re.findall(r'(Warning:.*)', log_content)
    undefined_warns = [w for w in warnings if "undefined" in w or "??" in w or "Reference" in w]
    if undefined_warns:
        print(f"⚠️ LaTeX Warnings Found: {len(undefined_warns)}")
        for w in undefined_warns:
            print(f"  - {w}")
    else:
        print("✅ No 'undefined' warnings in log.")

    print("\n=== 3. Syntax & Typos Check ===")
    # Check "et al" format (should have period)
    # Find 'et al' followed by something that is NOT a period
    et_al_matches = re.finditer(r'et al([^.])', content)
    errors = []
    for m in et_al_matches:
        # Ignore if it is at the end of line or specific cases, but usually et al. is correct
        # context = content[max(0, m.start()-10):min(len(content), m.end()+10)]
        errors.append(m.group(0))
    
    if errors:
        print(f"⚠️ Potential 'et al.' formatting errors (missing period?): {errors}")
    else:
        print("✅ 'et al.' formatting seems correct.")
   
    # Check Figure reference consistency
    fig_refs = re.findall(r'(図|Figure|Fig\.)\\ref', content)
    print(f"ℹ️ Figure reference styles found: {set(fig_refs)} (Should be consistent)")

    # Check for double words (e.g., "the the") - simplistic check for Japanese context
    double_words = re.findall(r'([^\x00-\x7F]+)\1', content)
    # Filter out valid ones like "人人", "数数" etc if any, but "を行うを行う" is bad.
    # checking for long repeats > 2 chars
    long_doubles = [w for w in double_words if len(w) > 1]
    if long_doubles:
         print(f"⚠️ Potential duplicated words found: {long_doubles}")

if __name__ == "__main__":
    check_tex_integrity("paper/sice_submission/sice_paper.tex", "paper/sice_submission/sice_paper.log")
