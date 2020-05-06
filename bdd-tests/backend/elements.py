"""Dom elements."""

from typing import TYPE_CHECKING, Tuple

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

if TYPE_CHECKING:
    from pages import BasePage
    from selenium import webdriver

Locator = Tuple[str, str]


class InputElement:
    """Text Input Element class."""

    def __init__(
        self, locator: Locator, timeout: int = 2, send_backspace: bool = False
    ):
        """
        locator: tuple (By.<kind_of_search>, <search value>)
        timeout: waiting time in second for the given element
        send_backspace: send backspace to clear previous value
        """
        self.locator = locator
        self.timeout = timeout
        self.send_backspace = send_backspace

    def __set__(self, obj: "BasePage", value: str):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        element.clear()
        # using input-number, while clearing set to 1 so value is add the
        # the first character, select all
        if self.send_backspace:
            # wondering why this doesn't works on export-name element
            # from selenium.webdriver.common.action_chains import ActionChains
            # ActionChains(a_search.driver).key_down(Keys.CONTROL)
            # .send_keys("a").key_up(Keys.CONTROL).perform()
            for _ in range(0, len(element.get_attribute("value"))):
                driver.find_element(*self.locator).send_keys(Keys.BACKSPACE)
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj: "BasePage", owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")


class LinkUrlElement:
    def __init__(self, locator: Locator, timeout: int = 2):
        """
        locator: tuple (By.<kind_of_search>, <search value>)
        timeout: waiting time in second for the given element
        """
        self.locator = locator
        self.timeout = timeout

    def __set__(self, obj: "BasePage", value: str):
        """Sets the text to the value supplied"""
        raise NotImplementedError()

    def __get__(self, obj: "BasePage", owner):
        """Gets the href of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("href")


class SelectElement:
    """Select form input Element class."""

    def __init__(self, locator: Locator, timeout: int = 2):
        """
        locator: tuple (By.<kind_of_search>, <search value>)
        timeout: waiting time in second for the given element
        """
        self.locator = locator
        self.timeout = timeout

    def __set__(self, obj: "BasePage", value: str):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_element(*self.locator)
        )
        Select(driver.find_element(*self.locator)).select_by_visible_text(value)

    def __get__(self, obj: "BasePage", owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")


class CheckboxElement:
    """CheckboxElement form input Element class."""

    def __init__(
        self, locator: Locator, click_locator: Locator = None, timeout: int = 2
    ):
        """
        locator: tuple (By.<kind_of_search>, <search value>)
        click_locator tuple (By.<kind_of_search>, <search value>) using buefy we can't
        directly click on the input element, event is managed by an overlap span element
        if none this class will use the locator
        timeout: waiting time in second for the given element
        """
        self.locator = locator
        self.click_locator = click_locator if click_locator else locator
        self.timeout = timeout

    def __set__(self, obj: "BasePage", checked: bool):
        """Click on the checkbox if necessary to obtain the desired state
        """
        if self.__get__(obj, None) != checked:
            driver = obj.driver
            WebDriverWait(driver, self.timeout).until(
                lambda driver: driver.find_element(*self.click_locator)
            )
            click_el = driver.find_element(*self.click_locator)
            click_el.click()

    def __get__(self, obj: "BasePage", owner):
        """Gets if the input text is"""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.is_selected()


class SnackBarElement:
    """Snackbar Element class.

    Represents popup with callback messages used to inform clients what's happen on the
    server side. It makes sure it has the ``expected_class`` (default: ``is-success``)
    and clicks the button to close the snackbar.
    """

    def __init__(
        self,
        locator: Tuple[str, str],
        timeout: int = 10,
        expected_class: str = "is-success",
    ):
        """
        locator: tuple (By.<kind_of_search>, <search value>)
        timeout: waiting time in second for the given element
        """
        self.locator = locator
        self.timeout = timeout
        self.expected_class = expected_class

    def __get__(self, obj: "BasePage", owner) -> Tuple[bool, str]:
        """Returns a tuple (``expected_class`` found ?, and the whole innerHTML)."""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        res = (
            self.expected_class in element.get_attribute("class"),
            element.get_attribute("innerHTML"),
        )
        element.find_element_by_css_selector("button").click()
        return res


class TextElement:
    """Text zone that display results from backend, waiting the result from
    callback.

    At the moment this element assume the element is not present in the
    page before callback.
    """

    def __init__(self, locator: Locator, timeout: int = 10):
        """
        locator: tuple (By.<kind_of_search>, <search value>)
        timeout: waiting time in second for the given element
        """
        self.locator = locator
        self.timeout = timeout

    def __get__(self, obj: "BasePage", owner):
        """Returns the innerHTML."""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("innerHTML")


class TableElement:
    """Html table rows to introspect table values, given a css selector to
    html rows (<tr>) this will construct a list of list where each values
    is the `.text` of the cell (<td>) element.

    usage::

        table_data = TableElement("CSS SELECTOR TO ROWS (<tr> tags)")
        for row in table_data:
            for cell in row:
                print (cell)
    """

    def __init__(self, locator: Locator, timeout: int = 10):
        self.locator = locator
        self.timeout = timeout

    def __get__(self, obj: "BasePage", owner):
        """Returns the innerHTML."""
        driver = obj.driver
        WebDriverWait(driver, self.timeout).until(
            lambda driver: driver.find_elements(*self.locator)
        )
        results = []
        rows = driver.find_elements(*self.locator)
        for row in rows:
            results.append(
                [cell.text.strip() for cell in row.find_elements_by_tag_name("td")]
            )
        return results


class ClickElement(EC.element_to_be_clickable):
    """Try to click on an element until it works.

    This extend EC.element_to_be_clickable by catching ElementClickInterceptedException
    to make sure that there is no overlay stoping the click event propagation.

    usage:

    WebDriverWait(self.driver, timeout).until(
        ClickElement(A_LOCATOR)
    )
    """

    def __call__(self, driver: "webdriver"):
        element = super(ClickElement, self).__call__(driver)
        if element:
            try:
                element.click()
                return True
            except ElementClickInterceptedException:
                # we ignore if any overlay stop the event propagation
                return False
        return element


class TextToBeDifferentInElement:
    def __init__(self, locator: Locator, value: str):
        self.locator = locator
        self.value = value

    def __call__(self, driver: "webdriver"):
        element = driver.find_element(*self.locator)
        if not element:
            return False
        return element.text != self.value
