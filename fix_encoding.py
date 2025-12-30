
import sys

def convert_encoding(filename):
    # Try reading as UTF-16 (PowerShell default)
    try:
        with open(filename, 'r', encoding='utf-16') as f:
            content = f.read()
        print("Read as UTF-16")
    except UnicodeError:
        try:
            # Try CP1252 (Windows default) or others if needed
            with open(filename, 'r', encoding='cp1252') as f:
                content = f.read()
            print("Read as CP1252")
        except:
             print("Could not decode file")
             sys.exit(1)

    # Write back as UTF-8
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Converted to UTF-8")

if __name__ == "__main__":
    convert_encoding('data_dump.json')
