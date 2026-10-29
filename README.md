# Tellonym Dataset Scraper 
A Python script to scrape public questions ("tells") and answers from Tellonym profiles and export them into JSON Lines (`.jsonl`) format for machine learning dataset preparation.

---

## Features

- **Automated Pagination:** Automatically paginates through a user's answer history to collect available public data.
- **Clean JSONL Export:** Filters and structures data into standard input-output training pairs suitable for fine-tuning language models.
- **Robust Error Handling:** Validates HTTP responses, manages missing users gracefully, and includes rate-limiting delays to prevent request flooding.
  
---

## Requirements

- Python 3.6 or higher
- `requests` library

---

## Installation

1. Clone the repository or download the script:
   ```bash
   git clone https://github.com/sudo6t6/tellonym-cli.git
   cd tellonym-cli
   ```
2. Installing dependencies:
  ```
  pip install requests
  ```
3. Run the script from the command line by passing the target Tellonym username as an argument:
  ```
  python tellonym-cli.py <username>
  ```
4. If you do not provide a username as an argument, the script will prompt you to enter one interactively:
  ```
  python tellonym-cli.py
  ```
**OUTPUT:**
- Upon successful completion, the script generates a dataset file in the working directory named `<username>_dataset.jsonl`. Each line contains a JSON object with the following structure:
```
  {"tell": "Example question received", "answer": "Example answer given"}
```
## **_Disclaimer_:**
This software is written for educational and legitimate dataset-collection purposes. If you use it to harass, stalk, dox, or otherwise degrade human beings created in the image of God, you are a glowing glowie, a degenerate, and a parasite upon the digital ecosystem. 
I wrote code; I did not write your morals. Do not flood APIs like an undisciplined brute, respect rate limits, and do not use this program for malice.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IF IT BREAKS YOUR MACHINE OR GETS YOUR IP BANNED, THAT IS BETWEEN YOU AND YOUR COMPUTING CHOICES.
