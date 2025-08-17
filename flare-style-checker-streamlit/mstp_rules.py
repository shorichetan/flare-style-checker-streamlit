import re

MSTP_RULES = [
    # --- Terminology (existing rules) ---
    {
        "id": "avoid-click-on",
        "desc": "Use 'click' instead of 'click on'.",
        "pattern": re.compile(r"\bclick on\b", re.IGNORECASE),
        "repl": "click"
    },
    {
        "id": "use-email",
        "desc": "Use 'email' instead of 'e-mail'.",
        "pattern": re.compile(r"\be-mail\b", re.IGNORECASE),
        "repl": "email"
    },
    {
        "id": "use-sign-in",
        "desc": "Use 'sign in' instead of 'log in' (verb).",
        "pattern": re.compile(r"\blog in\b", re.IGNORECASE),
        "repl": "sign in"
    },
    {
        "id": "use-sign-in-noun",
        "desc": "Use 'sign-in' instead of 'login' (noun/adj).",
        "pattern": re.compile(r"\blogin\b", re.IGNORECASE),
        "repl": "sign-in"
    },
    {
        "id": "use-internet",
        "desc": "Always capitalize 'Internet'.",
        "pattern": re.compile(r"\binternet\b"),
        "repl": "Internet"
    },
    {
        "id": "use-web-lower",
        "desc": "Use lowercase 'web'.",
        "pattern": re.compile(r"\bWeb\b"),
        "repl": "web"
    },
    {
        "id": "use-ok",
        "desc": "Use 'OK' instead of 'Okay'.",
        "pattern": re.compile(r"\bOkay\b", re.IGNORECASE),
        "repl": "OK"
    },

    # --- Style / Grammar (existing) ---
    {
        "id": "avoid-etc",
        "desc": "Avoid 'etc.' in technical docs.",
        "pattern": re.compile(r"\betc\.", re.IGNORECASE),
        "repl": ""
    },
    {
        "id": "setup-vs-set-up",
        "desc": "Use 'set up' (verb), not 'setup'.",
        "pattern": re.compile(r"\bsetup\b", re.IGNORECASE),
        "repl": "set up"
    },
    {
        "id": "use-select",
        "desc": "Use 'select' instead of 'choose'.",
        "pattern": re.compile(r"\bchoose\b", re.IGNORECASE),
        "repl": "select"
    },
    {
        "id": "use-that",
        "desc": "Prefer 'that' over 'which' for restrictive clauses.",
        "pattern": re.compile(r"\bwhich\b", re.IGNORECASE),
        "repl": "that"
    },

    # --- Punctuation / Formatting (existing) ---
    {
        "id": "no-ampersand",
        "desc": "Use 'and' instead of '&'.",
        "pattern": re.compile(r"&"),
        "repl": "and"
    },
    {
        "id": "serial-comma",
        "desc": "Add Oxford comma in lists (A, B, and C).",
        "pattern": re.compile(r"(\w+,\s\w+)\sand\s(\w+)"),
        "repl": r"\1, and \2"
    },
    {
        "id": "use-quotation-marks",
        "desc": "Use straight quotes, not smart quotes.",
        "pattern": re.compile(r"[“”]"),
        "repl": "\""
    },
    {
        "id": "use-apostrophe",
        "desc": "Use straight apostrophes, not smart ones.",
        "pattern": re.compile(r"[‘’]"),
        "repl": "'"
    },

    # --- Consistency (existing) ---
    {
        "id": "use-uppercase-ui",
        "desc": "Capitalize UI elements (OK, Cancel, Save).",
        "pattern": re.compile(r"\bok\b", re.IGNORECASE),
        "repl": "OK"
    },
    {
        "id": "use-uppercase-windows",
        "desc": "Capitalize 'Windows'.",
        "pattern": re.compile(r"\bwindows\b"),
        "repl": "Windows"
    },
    {
        "id": "use-uppercase-office",
        "desc": "Capitalize 'Office'.",
        "pattern": re.compile(r"\boffice\b"),
        "repl": "Office"
    },

    # --- Additional MSTP Style Rules ---
    {
        "id": "avoid-passive",
        "desc": "Prefer active voice instead of passive voice.",
        "pattern": re.compile(r"\b(is|was|were|be|been|being)\s+\w+ed\b", re.IGNORECASE),
        "repl": ""  # Optional: user can review manually
    },
    {
        "id": "avoid-redundant-words",
        "desc": "Avoid redundant words like 'actually', 'really', 'very'.",
        "pattern": re.compile(r"\b(actual(ly)?|really|very)\b", re.IGNORECASE),
        "repl": ""
    },
    {
        "id": "short-sentences",
        "desc": "Prefer short, clear sentences.",
        "pattern": re.compile(r"(.{120,}?)\.", re.IGNORECASE),
        "repl": ""  # Suggest manually
    },
    {
        "id": "numbers-as-digits",
        "desc": "Use digits for numbers 10 and above.",
        "pattern": re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\b", re.IGNORECASE),
        "repl": lambda m: str({"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}[m.group(0).lower()])
    },
    {
        "id": "avoid-jargon",
        "desc": "Avoid technical jargon where possible.",
        "pattern": re.compile(r"\b(utilize|leverage|synergy)\b", re.IGNORECASE),
        "repl": lambda m: {"utilize":"use","leverage":"use","synergy":"collaboration"}[m.group(0).lower()]
    },
]
