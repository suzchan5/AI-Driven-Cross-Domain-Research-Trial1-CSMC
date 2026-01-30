import base64
import re
import os

# --- Configuration ---
import os

# Get the absolute path to the project root (assuming script is in project/paper/)
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)  # Go up one level to project root
images_abs_dir = os.path.join(base_dir, "docs/images")

# Input/Output pairs
targets = [
    {
        "source": os.path.join(base_dir, "paper/draft_jp.md"),
        "print_md": os.path.join(base_dir, "paper/draft_jp_final_print.md")
    },
    {
        "source": os.path.join(base_dir, "paper/draft_en.md"),
        "print_md": os.path.join(base_dir, "paper/draft_en_final_print.md")
    }
]

# Frontmatter for PDF generation
frontmatter = """---
pdf_options:
  format: A4
  margin: 20mm
  printBackground: true
script:
  - content: |
      window.MathJax = { tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] } };
  - url: https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
stylesheet: https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css
body_class: markdown-body
---

"""

# Helper function: Encode image to Base64
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        ext = os.path.splitext(image_path)[1].lower().replace('.', '')
        if ext == 'jpg': ext = 'jpeg'
        return f"data:image/{ext};base64,{encoded_string}"
    except Exception as e:
        print(f"Error encoding {image_path}: {e}")
        return ""

# Helper function: Replace markdown image with Base64 HTML
def base64_repl_factory(source_file_path):
    def repl(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        
        # Resolve absolute path
        # Check if it points to docs/images
        if "docs/images" in rel_path:
            filename = os.path.basename(rel_path)
            abs_path = os.path.join(images_abs_dir, filename)
        else:
            # Fallback: relative to markdown file
            abs_path = os.path.abspath(os.path.join(os.path.dirname(source_file_path), rel_path))
        
        if os.path.exists(abs_path):
            b64_data = encode_image(abs_path)
            if b64_data:
                # Use max-width to ensure it fits on page
                return f'<div align="center"><img src="{b64_data}" alt="{alt_text}" style="max-width:100%; max-height: 800px;"></div>'
        
        print(f"Warning: Image not found at {abs_path}")
        return match.group(0) # Keep original if fail
    return repl

# --- Main Processing Loop ---
for target in targets:
    src = target["source"]
    dest = target["print_md"]
    
    print(f"Processing {src}...")
    
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply Image Embedding
    final_content = re.sub(r'!\[(.*?)\]\((.*?)\)', base64_repl_factory(src), content)
    
    # Prepend Frontmatter
    final_content = frontmatter + final_content
    
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Created {dest}")

print("All files prepared suitable for md-to-pdf.")
