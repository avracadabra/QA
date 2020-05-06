"""Page objects pattern as advised from
https://selenium-python.readthedocs.io/page-objects.html
"""
import re
from collections import Counter
from typing import Optional, Tuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from backend.elements import ClickElement
Locator = Tuple[str, str]


class BasePage:
    """Base class to initialize the base page that will be called from all pages"""

    _page_selector: Optional[Locator] = None

    def __init__(self, driver: webdriver):
        self.driver = driver
        if self._page_selector:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self._page_selector)
            )

    def click(self, by_locator: Locator, timeout: int = 10):
        """Wait for the element to be clickable, then click.

        First we wait for an eventual loading overlay to disappear then we check if the
        element is visible & active before clicking it.
        """
        WebDriverWait(self.driver, timeout).until(ClickElement(by_locator))

    def click_menu_home(self) -> "MainPage":
        """Go (click) to the home page and return a MainPage object"""
        self.click(MainPageLocators.MENU_HOME)
        return MainPage(self.driver)

    def click_menu_container_list(self) -> "SearchPage":
        """Go (click) to the search page and return a SearchPage object"""
        self.click(MainPageLocators.MENU_CONTAINER_LIST)
        from backend.container_page import ContainerListPage

        return ContainerListPage(self.driver)


class MainPageLocators:
    """A class for main page locators. All main page locators should come here"""

    PAGE_SELECTOR = (By.ID, "home-page")
    MENU_HOME = (By.CSS_SELECTOR, "a[href='/']")
    MENU_CONTAINER_LIST = (By.CSS_SELECTOR, "a[href='/containers/list']")


class MainPage(BasePage):
    """Home page action come here."""

    _page_selector = MainPageLocators.PAGE_SELECTOR
