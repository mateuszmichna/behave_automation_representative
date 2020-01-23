from behave.runner import Context

from pages.main_header import MainHeader
from utils.base_page import BasePage
from utils.browsers.browser_selector import browser
from utils.fake_persons.fake_client import FakeClient


def start_driver():
    driver = browser().driver
    return driver


def before_all(context):
    context.stuff = Stuff(context)
    context.client = context.stuff.client()


def before_scenario(context, scenario):
    context.driver = start_driver()
    context.environment = Environment(context, context.driver)
    pages = context.environment._origin
    behave = ("feature", "text", "table", "stdout_capture", "stderr_capture", "log_capture", "fail_on_cleanup_errors")
    for behave_item in behave:
        pages.pop(behave_item, None)
    for page in pages:
        setattr(context, page, getattr(context.environment, page))


def after_scenario(context, scenario):
    context.driver.close()


def after_step(context, step):
    if step.status == 'failed':
        step_str = step.name
        context.driver.save_screenshot(f"{step_str}.png")


class Environment(Context):

    def __init__(self, runner, driver):
        super().__init__(runner)
        self.base = BasePage(driver)
        self.main_header = MainHeader(driver)


class Stuff(Context):

    def __init__(self, runner):
        super().__init__(runner)
        self.client = FakeClient
