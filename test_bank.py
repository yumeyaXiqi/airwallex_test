import pytest
import requests, json, re, logging, argparse, random, string
from enum import Enum

"""
Usage:
    pytest -o log_cli=true --url="bank_url" # show logging info
"""

LOGFORMAT = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOGFORMAT)

class BankCountry(Enum):
    US = "US"
    AU = "AU"
    CN = "CN"

class PaymentMethod(Enum):
    LOCAL = "LOCAL"
    SWIFT = "SWIFT"

class Illegal(Enum):
    BLANK = ""
    ILLEGAL = "ILLEGAL"


def get_right(from_int, to_int):
    if from_int > to_int:
        logging.error("{} must largger or equal than {}".format(to_int, from_int))
        return "0"
    digits = random.randint(from_int, to_int)
    ret_string = ""
    for _ in range(digits):
        ret_string += random.choice(string.printable + " ")
    return ret_string

#input bcc object of Enum BankCountry
def get_swift_code(bcc):
    swift_code = get_right(8,11)
    bcc = bcc.value
    return swift_code[0:4] + bcc + swift_code[6:]


def check_pass(r):
    assert(r.status_code == 200)
    assert("success" in r.json().keys())
    assert(r.json()["success"] == "Bank details saved")

class Test_Bank_Positive(object):

    def test_local_us(self, bank_url):
        data = {
            "payment_method":PaymentMethod.LOCAL.value,
            "bank_country_code": BankCountry.US.value,
            "account_name": get_right(2, 10),
            "account_number": get_right(1, 17),
            "aba": get_right(9,9)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        check_pass(r)
    
    def test_local_au(self, bank_url):
        data = {
            "payment_method":PaymentMethod.LOCAL.value,
            "bank_country_code": BankCountry.AU.value,
            "account_name": get_right(2, 10),
            "account_number": get_right(6, 9),
            "bsb": get_right(6,6)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        check_pass(r)
    
    def test_local_cn(self, bank_url):
        data = {
            "payment_method":PaymentMethod.LOCAL.value,
            "bank_country_code": BankCountry.CN.value,
            "account_name": get_right(2, 10),
            "account_number": get_right(8, 20)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        check_pass(r)
    

    def test_swift_us(self, bank_url):
        country = BankCountry.US
        data = {
            "payment_method":PaymentMethod.SWIFT.value,
            "bank_country_code": country.value,
            "swift_code": get_swift_code(country),
            "account_name": get_right(2, 10),
            "account_number": get_right(1, 17),
            "aba": get_right(9,9)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        check_pass(r)
    
    def test_swift_au(self, bank_url):
        country = BankCountry.AU
        data = {
            "payment_method":PaymentMethod.SWIFT.value,
            "bank_country_code": country.value,
            "swift_code": get_swift_code(country),
            "account_name": get_right(2, 10),
            "account_number": get_right(6, 9),
            "bsb": get_right(6,6)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        check_pass(r)
    
    def test_swift_cn(self, bank_url):
        country = BankCountry.CN
        data = {
            "payment_method":PaymentMethod.SWIFT.value,
            "bank_country_code": country.value,
            "swift_code": get_swift_code(country),
            "account_name": get_right(2, 10),
            "account_number": get_right(8, 20)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        check_pass(r)

class Test_Bank_Negative(object):
    def test_need_account_number(self, bank_url):
        data = {
            "payment_method":PaymentMethod.LOCAL.value,
            "bank_country_code": BankCountry.US.value,
            "account_name": get_right(2, 10),
            "aba": get_right(9,9)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        assert(r.status_code == 400)
        assert('error' in r.json())
        assert(r.json()['error'] == "'account_number' is required")
    
    def test_wrong_account_number(self, bank_url):
        country = BankCountry.US
        data = {
            "payment_method":PaymentMethod.SWIFT.value,
            "bank_country_code": country.value,
            "swift_code": get_swift_code(country),
            "account_name": get_right(2, 10),
            "account_number": get_right(19, 27),
            "aba": get_right(9,9)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        assert(r.status_code == 400)
        assert('error' in r.json())
        
        #other cn need fill
    
    def test_swift_code(self, bank_url):
        country = BankCountry.US
        data = {
            "payment_method":PaymentMethod.SWIFT.value,
            "bank_country_code": country.value,
            "swift_code": get_right(8, 11),
            "account_name": get_right(2, 10),
            "account_number": get_right(1, 17),
            "aba": get_right(9,9)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        assert(r.status_code == 400)
        assert('error' in r.json())
        
        #other cn need fill
    
    def test_wrong_swift_code_length(self, bank_url):
        country = BankCountry.US
        data = {
            "payment_method":PaymentMethod.SWIFT.value,
            "bank_country_code": country.value,
            "swift_code": get_right(12, 20),
            "account_name": get_right(2, 10),
            "account_number": get_right(1, 17),
            "aba": get_right(9,9)
        }
        logging.info(data)
        r = requests.post(url=bank_url, json = data)
        assert(r.status_code == 400)
        assert('error' in r.json())
        assert(r.json()['error'] == "Length of 'swift_code' should be either 8 or 11")
        
        #other cn need fill

if __name__ == '__main__':
    pytest.main()


