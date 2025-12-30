import os
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        def replacer(match):
            # Replace all newlines and multiple spaces with a single space
            cleaned = re.sub(r'\s*\n\s*', ' ', match.group(0))
            return cleaned

        # Match Django tags {{ ... }} or {% ... %}
        # We use consistent non-greedy matching
        new_content = re.sub(r'({{|{%)(.*?)(}}|%})', replacer, content, flags=re.DOTALL)
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {filepath}")
        else:
            print(f"No changes needed: {filepath}")
            
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

if __name__ == "__main__":
    base_dir = r"c:\Users\hp\.gemini\antigravity\scratch\baby_store"
    files_to_fix = [
        r"core\templates\core\dashboard.html",
        r"orders\templates\orders\cart_detail.html",
        r"orders\templates\orders\checkout.html",
        r"orders\templates\orders\track_order.html",
        r"templates\base.html",
        r"store\templates\store\product_detail.html"
    ]
    
    for relative_path in files_to_fix:
        full_path = os.path.join(base_dir, relative_path)
        if os.path.exists(full_path):
            fix_file(full_path)
        else:
            print(f"File not found: {full_path}")
