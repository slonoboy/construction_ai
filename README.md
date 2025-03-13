

## AI-Powered Construction Task Manager

## Setup

Create .env file in the source folder with the following contens
```
GEMINI_API_KEY="API_KEY"
GEMINI_MODEL="gemini-2.0-flash"
```
Locate the source folder, active the environment and run these commands:
```
pip install -r requirements.txt
fastapi run app
```


## Disclaimer
This project doesn't meet production standards. It needs better error handling, logging, and proper management of transactions and database sessions. There’s no retry logic for the Google Gemini API, and user input is accepted as plain text without extra checks. The token usage of Gemini API could be optimized further. Project and task status handling could be improved with enums. It's missing some production essentials like CORS and rate limiting. Also tests and migrations (with Alembic) are definitely needed.