import attr
import os
import pytest
import tempfile
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_configurator.configurator import Configurator

SELENIUM_CONFIG_FILE = os.environ.get("SELENIUM_CONFIG_FILE", "selenium.yaml")


@attr.s
class Site(object):
    host = attr.ib()
    port = attr.ib()
    scheme = attr.ib()
    path = attr.ib(default="")  # don't forget to add a leading /

    @property
    def url(self):
        return f"{self.scheme}://{self.host}:{self.port}{self.path}"


@pytest.fixture(scope="session")
def backend_site():
    return Site(host="127.0.0.1", port="8080", scheme="http")


@pytest.fixture()
def anonymous_session(webdriver, backend_site):
    webdriver.get(backend_site.url)
    return webdriver

def get_webdrivers():
    selenium_conf = Configurator.from_file(SELENIUM_CONFIG_FILE)
    drivers = selenium_conf.get_drivers()
    params = []
    for driver in drivers:
        params.append(pytest.param(driver, id=driver.name))
    return params


@pytest.fixture(params=get_webdrivers())
def selenium(request):
    return request.param


@pytest.fixture()
def webdriver(selenium):
    try:
        yield selenium.selenium
    finally:
        selenium.quit()


def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    """Called when step function failed to execute."""
    take_screenshot_if_possible(request, step_func_args)


def pytest_bdd_step_validation_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    """Called when step failed to validate."""
    take_screenshot_if_possible(request, step_func_args)


def take_screenshot_if_possible(request, func_args):
    webdriver = get_webdriver(func_args)
    if webdriver:
        screenshot_path = construct_screenshot_path(request)
        try:
            webdriver.save_screenshot(screenshot_path + ".png")
            print("Screenshot saved ", screenshot_path + ".png")
            with open(screenshot_path + ".html", "w") as html:
                html.write(webdriver.page_source)
                print("Html saved ", screenshot_path + ".html")
        except Exception as ex:
            print("Unable to take a screenshot, following exception occur: ", ex)


def construct_screenshot_path(request):
    directory = os.getenv("SCREENSHOT_DIR", tempfile.gettempdir())
    try:
        return os.path.join(directory, request._pyfuncitem.name)
    except Exception:
        return os.path.join(directory, str(request))


def get_webdriver(func_args):
    """parse func_args if a selenium webdriver is present return it otherwise
    return None
    """
    for _, arg in func_args.items():
        # in case using BasePage class webdriver is in driver attribute
        if hasattr(arg, "driver"):
            arg = arg.driver
        if isinstance(arg, WebDriver):
            return arg
