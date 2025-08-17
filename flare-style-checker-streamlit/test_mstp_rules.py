from mstp_rules import MSTP_RULES

# Sample text containing multiple MSTP issues
sample_text = """
Click on the button to send an e-mail.
Please setup the device and choose the option which you want.
Use Chrome, Firefox, etc.
Save & Exit.
The file which you opened is on the internet.
“Click OK” to continue.
ok button is displayed in windows office.
"""

def apply_mstp_rules(text):
    """Apply all MSTP rules to the text and print each change."""
    for rule in MSTP_RULES:
        pattern = rule["pattern"]
        repl = rule["repl"]
        matches = list(pattern.finditer(text))
        if matches:
            print(f"\nRule: {rule['id']}")
            print(f"Description: {rule['desc']}")
            for match in matches:
                print(f"  Found: '{match.group(0)}' at position {match.start()}-{match.end()}")
            text = pattern.sub(repl, text)
    return text

print("=== Original Text ===")
print(sample_text)

cleaned_text = apply_mstp_rules(sample_text)

print("\n=== Cleaned Text ===")
print(cleaned_text)
