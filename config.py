import os

class Config(object):
    # Telegram API credentials
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    # Heroku configuration
    APP_NAME = os.environ.get("APP_NAME", "")
    API_KEY = os.environ.get("API_KEY", "")
    
    # Owner/User configuration
    OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
    
    # FR Token
    FR_TOKEN = os.environ.get("FR_TOKEN", "f4f0e3047723385244d3aae0068d60ec09f79345")
    
    # Credits
    CREDITS = os.environ.get("credits", "")
    
    # Group IDs (space-separated string of IDs)
    GROUP_IDS_STR = os.environ.get("GROUP_IDS", "")
    GROUP_IDS = [int(x) for x in GROUP_IDS_STR.split() if x.strip().isdigit()] if GROUP_IDS_STR else []
