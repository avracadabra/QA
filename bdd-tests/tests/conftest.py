from pytest_bdd import given


@given("I open the backend")
def backend(anonymous_session):
    """An alias to anonymous_session."""
    return anonymous_session
