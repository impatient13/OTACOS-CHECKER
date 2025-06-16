# O'Tacos Checker

O'Tacos Checker is a Python tool designed to verify O'Tacos accounts from a list of combos (email:password). It uses the official API to attempt authentication and detect valid accounts.

---

## Features

- Checks combos (email:password) against the O'Tacos API.
- Color-coded console output for valid, invalid, and error results.
- Handles errors and rate limiting gracefully.
- Automatically saves valid combos to a `valids.txt` file.
- Randomizes User-Agent headers to mimic different clients.
- Simple console menu interface.

SCREEN: 

<img width="860" alt="image" src="https://github.com/user-attachments/assets/8918c8a0-818f-4e0c-ade0-d0de38976aab" />

---

## Requirements

- Python 3.6 or higher
- Python packages:
  - `requests`
  - `colorama`

Install dependencies with:

```bash
pip install requests colorama

