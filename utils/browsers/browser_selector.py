from utils.browsers.chrome_browser import ChromeBrowser
from utils.browsers.edge_browser import EdgeBrowser
from utils.browsers.firefox_browser import FirefoxBrowser
from utils.settings.settings import BROWSER


def browser():
    browsers = {
        'chrome': ChromeBrowser,
        'firefox': FirefoxBrowser,
        'edge': EdgeBrowser,
    }
    return browsers[BROWSER]()
