import pytest

@pytest.mark.usefixtures("capture_screenshot_on_failure","page")
class BaseTest:

    pass