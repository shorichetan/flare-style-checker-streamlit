import re

# A starter set of MSTP-inspired rules. Extend as needed.
MSTP_RULES = [
    {
        "id": "MSTP.001",
        "desc": "Use 'select' instead of 'click on' for UI actions.",
        "pattern": re.compile(r"\bclick on\b", re.IGNORECASE),
        "repl": "select",
    },
    {
        "id": "MSTP.002",
        "desc": "Prefer 'sign in' over 'login' when used as a verb.",
        "pattern": re.compile(r"\blog ?in\b", re.IGNORECASE),
        "repl": "sign in",
    },
    {
        "id": "MSTP.003",
        "desc": "Use 'email' (one word).",
        "pattern": re.compile(r"\be-?mail\b", re.IGNORECASE),
        "repl": "email",
    },
    {
        "id": "MSTP.004",
        "desc": "Replace 'OK' dialog guidance with 'Select OK'.",
        "pattern": re.compile(r"\bclick\s+OK\b", re.IGNORECASE),
        "repl": "Select OK",
    },
    {
        "id": "MSTP.005",
        "desc": "Avoid Latin abbreviations: replace 'e.g.' with 'for example'.",
        "pattern": re.compile(r"\be\.g\.\b", re.IGNORECASE),
        "repl": "for example",
    },
    {
        "id": "MSTP.006",
        "desc": "Avoid Latin abbreviations: replace 'i.e.' with 'that is'.",
        "pattern": re.compile(r"\bi\.e\.\b", re.IGNORECASE),
        "repl": "that is",
    },
    {
        "id": "MSTP.007",
        "desc": "Sentence case for button names: 'Save As' -> 'Save as' (simple heuristic).",
        "pattern": re.compile(r"\b(Save) (As)\b"),
        "repl": r"\1 as",
    },
    {
        "id": "MSTP.008",
        "desc": "Use 'choose' instead of 'pick'.",
        "pattern": re.compile(r"\bpick\b", re.IGNORECASE),
        "repl": "choose",
    },
]
