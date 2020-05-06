from backend.main_page import BasePage
from backend.elements import TableElement
from selenium.webdriver.common.by import By


class ContainerListPageLocators:
    PAGE_SELECTOR = (By.ID, "container-list-page")
    TABLE_CONTAINERS_ROWS = (
        By.CSS_SELECTOR,
        "#container-list > div > table > tbody > tr",
    )


class ContainerListPage(BasePage):
    containers_el = TableElement(ContainerListPageLocators.TABLE_CONTAINERS_ROWS)
