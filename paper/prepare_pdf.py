import os
import re

# Paths
import os

# Get the absolute path to the project root (assuming script is in project/paper/)
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)  # Go up one level to project root
source_file = os.path.join(base_dir, "paper/draft_jp.md")
target_file = os.path.join(base_dir, "paper/draft_jp_print.md")
images_abs_dir = os.path.join(base_dir, "docs/images")

# MathJax Frontmatter for md-to-pdf
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

# Read Content
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

import base64

# ... (Previous code)

# Function to encode image to base64
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"
    except Exception as e:
        print(f"Error encoding {image_path}: {e}")
        return ""

# 1. Replace relative image paths with Base64 embedded images
# Regex to find ![alt](../docs/images/filename.png) or similar patterns
# We look for markdown image syntax: ![...](path)
def base64_repl(match):
    alt_text = match.group(1)
    rel_path = match.group(2)
    
    # Resolve absolute path
    # Assuming relative path is relative to the paper directory (where md file is)
    # The current draft uses "../docs/images/..."
    # We need to correctly map this to explicit absolute path
    
    if "docs/images" in rel_path:
        filename = os.path.basename(rel_path)
        abs_path = os.path.join(images_abs_dir, filename)
    else:
        # Fallback or other paths
        abs_path = os.path.abspath(os.path.join(os.path.dirname(source_file), rel_path))
    
    if os.path.exists(abs_path):
        b64_data = encode_image(abs_path)
        if b64_data:
            return f'<img src="{b64_data}" alt="{alt_text}" style="max-width:100%;">'
    
    print(f"Warning: Image not found at {abs_path}")
    return match.group(0) # Return original if fail

# Replace markdown images: ![alt](path)
# Note: This regex is simple and assumes standard markdown image syntax
new_content = re.sub(r'!\[(.*?)\]\((.*?)\)', base64_repl, content)

# 2. Add Frontmatter
final_content = frontmatter + new_content

# 3. Write to temporary print file
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"Created {target_file} with embedded images for PDF generation.")
