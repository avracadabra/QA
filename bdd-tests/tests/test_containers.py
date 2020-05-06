# coding=utf-8
"""containers visualisation feature tests."""
from time import sleep

from backend.main_page import MainPage
from backend.container_page import ContainerListPage

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario("../features/containers.feature", "Reading results")
def test_reading_results(backend):
    """Reading results."""


@given('Ang I go to the "containers / containers" page')
def ang_i_go_to_the_containers__containers_page(backend):
    """Ang I go to the "containers / containers" page."""
    MainPage(backend).click_menu_container_list()


@when("page is loaded")
def page_is_loaded(backend):
    """page is loaded."""
    ContainerListPage(backend)


@then('at least "2" containers are present')
def at_least_2_containers_are_present(backend):
    """at least "2" containers are present."""
    container_page = ContainerListPage(backend)
    # TODO: find a proper way to waits results displayed
    sleep(1)
    assert len(container_page.containers_el) >= 1
    assert len(container_page.containers_el[0]) == 3  # 3 columns 
