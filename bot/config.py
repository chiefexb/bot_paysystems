import os
from pathlib import Path

from dotenv import load_dotenv
local_env_path = Path(__file__).parent.parent / '.local.env'
env_path = Path(__file__).parent.parent / '.env'
if not os.getenv('IS_DOCKER'):
    load_dotenv(local_env_path, override=True)
else:
    load_dotenv(env_path)

DB_PASS = os.getenv('MYSQL_ROOT_PASSWORD')
DB_NAME = os.getenv('MYSQL_DATABASE')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')

SITE_URL=os.getenv('SITE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')

STRIPE_PUBLIC_KEY=os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY=os.getenv('STRIPE_SECRET_KEY')


PORT = os.getenv('DB_PORT')
REDIS_HOST = os.getenv('REDIS_HOST')
# ADVERT_CHANNEL = os.getenv('ADVERT_CHANNEL')
# AUCTION_CHANNEL = os.getenv('AUCTION_CHANNEL')
REDIS_PASS = os.getenv('REDIS_PASSWORD')
GALLERY_CHANNEL = os.getenv('GALLERY_CHANNEL')
PARTNER_ID = os.getenv('PARTNER_ID')
DEV_ID = os.getenv('DEV_ID')
OWNER_PARTNER_ID = os.getenv('OWNER_PARTNER_ID')
USERNAME_BOT = os.getenv('USERNAME_BOT')
WORKDIR = Path(__file__).parent.parent
