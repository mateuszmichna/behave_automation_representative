from behave import given, when, then

from environment import Environment
from utils.settings.local_settings import USER_PRODUCTION_URL


class GeneralSteps(Environment):

    @when(u'The user opens up main page')
    def step_impl(context):
        context.base.get_page(USER_PRODUCTION_URL)

    @then(u'The user sees main logo')
    def step_impl(context):
        main_banner = context.main_header.get_main_banner()
        assert main_banner.is_displayed()
