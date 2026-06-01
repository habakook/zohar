# Zohar

A Django web app for browsing and searching the Zohar — a foundational Kabbalistic text — in Russian translation.

Deployed at: https://habakook.pythonanywhere.com

## What it does

- Browse the full Zohar split by Torah portion (parasha)
- Full-text search across all books with multiple filter modes (substring, exclusion, case-sensitive, whole-word)
- Hebrew text rendered with proper RTL styling
- Footnotes hyperlinked within each book
- Visit tracking with country lookup (ip-api.com)
- Secret stats page at `/mySecretStats8472/`

## Library

Two editions of the text are included:

- `zohar/lib1/` — primary library, numbered files
- `zohar/lib2/` — alternate edition
- `zohar/lib-spare/` — spare copies

## Stack

- Python 3.10
- Django 4.0
- SQLite
- Hosted on PythonAnywhere

## Setup

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

## Known issues / areas for improvement

- Search reads all files from disk on every request — should be cached in memory
- `DEBUG = False` in production; make sure `ALLOWED_HOSTS` is set correctly
- No `requirements.txt` yet
- Stats page shows bots alongside real visitors
- No pagination on search results
