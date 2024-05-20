import os

APP_NAME = 'cp-ds-cbo-summarizer'
CONFIG_INI = 'configs/config.ini'
STAGE = os.environ.get('ENV', 'staging_local')
if 'prod' in STAGE.lower():
    ENV = 'production'
elif 'stag' in STAGE.lower():
    ENV = 'staging'
MAX_TOKENS = 250
WORKFLOW_MAX_TOKENS = 3200
DOCS_FOR_RETRIEVAL = 5
LAST_EVENTS_FOR_ACTION = 3
NO_ACTION_ID = 0
NO_ACTION_TEXT = "kein Handlungsbedarf"
CUSTOM_MAIL_ID = 1
CUSTOM_MAIL_TEXT = "kundenspezifische E-Mail erforderlich"

#EMAIL_API = "http://localhost:33070"

EMAIL_API = "http://mail-feed-app-svc.bb-mail-feed:80"
LLAMA_URL = "https://ollama-prod.carparts.tools.ch24.de/api/generate"
