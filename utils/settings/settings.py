import os
from utils.settings.platform_browser_settings import get_platform, get_driver_by_platform_name_and_browser, get_browser
from utils.settings.local_settings import IMPLICITLY_WAIT, USER_PRODUCTION_URL, USER_STAGING_URL, USER_DEV_URL

# required
PRODUCTION_URL = os.environ.get('PRODUCTION_URL', USER_PRODUCTION_URL)
STAGING_URL = os.environ.get('STAGING_URL', USER_STAGING_URL)
DEV_URL = os.environ.get('DEV_URL', USER_DEV_URL)
PRODUCTION_NETLOC = os.environ.get('PRODUCTION_NETLOC', '')
STAGING_NETLOC = os.environ.get('STAGING_NETLOC', '')
DEV_NETLOC = os.environ.get('DEV_NETLOC', '')
TESTS_ENVIRONMENT = os.environ.get('TESTS_ENVIRONMENT', '')
SYSTEM = os.environ.get('SYSTEM', get_platform())
BROWSER = os.environ.get('BROWSER', get_browser())
DRIVER = os.environ.get('DRIVER', get_driver_by_platform_name_and_browser(SYSTEM, BROWSER))
IMPLICITLY_WAIT = IMPLICITLY_WAIT

# other const
PATH_TO_PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

