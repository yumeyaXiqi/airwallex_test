import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--bank_url",
        action="store",
        default='http://preview.airwallex.com:30001/bank',
        help="bank url",
    )

@pytest.fixture()
def bank_url(request):
    return request.config.getoption("--bank_url")
