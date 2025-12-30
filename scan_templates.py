import os
import re

def scan_templates(root_dir):
    django_tag_pattern = re.compile(r'({{|{%)(.*?)(}}|%})', re.DOTALL)
    
    issues = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                matches = django_tag_pattern.finditer(content)
                for match in matches:
                    tag_content = match.group(0)
                    if '\n' in tag_content:
                        # Exclude blocktrans as it often spans lines legitimately
                        if 'blocktrans' in tag_content:
                            continue
                        
                        start_line = content[:match.start()].count('\n') + 1
                        # end_line = content[:match.end()].count('\n') + 1
                        issues.append(f"{filepath}:{start_line}")
                        print(f"Found issue in {filepath} at line {start_line}:\n{tag_content!r}\n")

    return issues

if __name__ == "__main__":
    root = r"c:\Users\hp\.gemini\antigravity\scratch\baby_store"
    issues = scan_templates(root)
    if issues:
        print(f"Found {len(issues)} split tags.")
        for i in issues:
            print(i)
    else:
        print("No split tags found.")
