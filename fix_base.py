import os

path = 'templates/base.html'
if not os.path.exists(path):
    print(f"File not found: {path}")
    exit(1)

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target string without spaces (what the error reported)
bad_syntax_1 = 'LANGUAGE_CODE|slice:":2"=="en"'
good_syntax_1 = 'LANGUAGE_CODE|slice:":2" == "en"'
bad_syntax_2 = 'LANGUAGE_CODE=="ar"'
good_syntax_2 = 'LANGUAGE_CODE == "ar"'

if bad_syntax_1 in content:
    print(f"Found incorrect syntax 1: '{bad_syntax_1}'")
    content = content.replace(bad_syntax_1, good_syntax_1)

if bad_syntax_2 in content:
    print(f"Found incorrect syntax 2: '{bad_syntax_2}'")
    content = content.replace(bad_syntax_2, good_syntax_2)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully updated base.html.")

