from selenium.webdriver.remote.webelement import WebElement

from utils.base_page import BasePage
from utils.custom_element import CustomElement


class MainHeader(BasePage):
    main_banner = "//img[@class='img-responsive']"
    phone_icon = "//span[@class='shop-phone']//i[@class='icon-phone']"
    phone_on_top = "//span[@class='shop-phone']//strong"
    contact_us_button = "//div[@id='contact-link']//a"
    sign_in_button = "//a[@class='login']"
    main_logo = "//img[@class='logo img-responsive']"
    search_banner = "//input[@id='search_query_top']"
    search_icon = "//button[@name='submit_search']"
    cart_button = "/div[@class='shopping_cart']/a"
    cart_sign = "//div[@class='shopping_cart']//a//b"
    main_bannner = "//img[@class='img-responsive']"
    sing_in_button = "//a[@class='login']"
    cart_amount_empty = "//span[@class='ajax_cart_no_product']"
    cart_one_product = "//span[@class='ajax_cart_product_txt unvisible']"
    cart_few_products = "//span[@class='ajax_cart_product_txt_s unvisible']"
    cart_all_products_quantity = "//div[@class='shopping_cart']//span[@class='ajax_cart_quantity unvisible']"
    account_button = "//a[@class='account']" #Visible only when logged
    shipping_label = "//div[@class='cart-prices-line first-line']//span[2]"
    shipping_amount = "//span[@class='price cart_block_shipping_cost ajax_cart_shipping_cost']"
    total_label = "//div[@class='cart-prices-line last-line']//span[2]"
    total_amount = "//span[@class='price cart_block_total ajax_block_cart_total']"
    check_out_button = "//a[@id='button_order_cart']//span"
    women_button = "//ul[@class='sf-menu clearfix menu-content sf-js-enabled sf-arrows']/li[1]/a"
    dresses_button = "//*[@id='block_top_menu']/ul/li[2]/a"
    tshirt_button = "//body[@id='category']/div[@id='page']/div[@class='header-container']/header[" \
                    "@id='header']/div/div[@class='container']/div[@class='row']/div[@id='block_top_menu']/ul[" \
                    "@class='sf-menu clearfix menu-content sf-js-enabled sf-arrows']/li[3]/a[1]"
    women_tops_button = "//li[@class='sfHover']//a[@href='http://automationpractice.com/index.php?id_category=4" \
                        "&controller=category']"
    women_dresses_button = "//ul[contains(@class, 'submenu-container clearfix')]//li[@class='sfHover']/a"
    cart_box_items_list = "//dt"
    cart_box_item_price = "//span[@class='price']"
    cart_box_item_img = "//img"
    cart_box_item_quantity = "//span[@class='quantity']"
    cart_box_item_name = "//a[@class='cart_block_product_name']"
    cart_box_item_details = "//div[@class='product-atributes']//a"
    cart_box_item_remove_button = "//a[@class='ajax_cart_block_remove_link']"

    def get_main_banner(self):
        return self.get_element(self.main_banner)

    def click_contact_us(self):
        return self.get_element(self.contact_us_button).click()

    def click_sign_in(self):
        return self.get_element(self.sign_in_button).click()

    def click_main_logo(self):
        return self.get_element(self.main_logo).click()

    def click_main_banner(self):
        return self.get_element(self.main_banner).click()

    def type_search(self, keys: str):
        return self.get_element(self.search_banner, keys).click()

    def click_search_button(self):
        return self.get_element(self.search_icon).click()

    def click_on_cart(self):
        return self.get_element(self.cart_button).click()

    def click_on_check_out(self):
        return self.get_element(self.check_out_button).click()

    def click_on_women_button(self):
        return self.get_element(self.women_button).click()

    def click_on_dresses_button(self):
        return self.get_element(self.dresses_button).click()

    def click_on_tshirt_button(self):
        return self.get_element(self.tshirt_button).click()

    def hover_on_cart_button(self):
        return self.get_element(self.cart_button).click()

    def hover_on_women_button(self):
        return self.get_element(self.women_button).click()

    def hover_on_dresses_button(self):
        return self.get_element(self.dresses_button).click()
