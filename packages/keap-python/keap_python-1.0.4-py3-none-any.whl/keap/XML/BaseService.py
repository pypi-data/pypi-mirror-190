import json
from enum import Enum

from keap import Keap
from keap.exceptions import KeapUnauthorizedException, KeapException, KeapTokenExpiredException

try:
    from xmlrpclib import ServerProxy, Error
except ImportError:
    from xmlrpc.client import ServerProxy, Error


class FormField(Enum):
    CONTACT = -1
    REFERRAL_PARTNER = -3
    OPPORTUNITY = -4
    TASK = -5
    NOTE = -5
    APPOINTMENT = -5
    COMPANY = -6
    ORDER = -9


class BaseService:
    xmlrpc_url = 'https://api.infusionsoft.com/crm/xmlrpc/v1'
    _service = None
    client = None
    FORM_FIELDS = FormField

    custom_field_type_map = {
        1: {
            "Name": "Phone Number",
            "Has Options": "no"
        },
        2: {
            "Name": "Social Security Number",
            "Has Options": "no"
        },
        3: {
            "Name": "Currency",
            "Has Options": "no"
        },
        4: {
            "Name": "Percent",
            "Has Options": "no"
        },
        5: {
            "Name": "State",
            "Has Options": "no"
        },
        6: {
            "Name": "Yes/No",
            "Has Options": "no"
        },
        7: {
            "Name": "Year",
            "Has Options": "no"
        },
        8: {
            "Name": "Month",
            "Has Options": "no"
        },
        9: {
            "Name": "Day of Week",
            "Has Options": "no"
        },
        10: {
            "Name": "Name",
            "Has Options": "no"
        },
        11: {
            "Name": "Decimal Number",
            "Has Options": "no"
        },
        12: {
            "Name": "Whole Number",
            "Has Options": "no"
        },
        13: {
            "Name": "Date",
            "Has Options": "no"
        },
        14: {
            "Name": "Date/Time",
            "Has Options": "no"
        },
        15: {
            "Name": "Text",
            "Has Options": "no"
        },
        16: {
            "Name": "Text Area",
            "Has Options": "no"
        },
        17: {
            "Name": "List Box",
            "Has Options": "yes"
        },
        18: {
            "Name": "Website",
            "Has Options": "no"
        },
        19: {
            "Name": "Email",
            "Has Options": "no"
        },
        20: {
            "Name": "Radio",
            "Has Options": "yes"
        },
        21: {
            "Name": "Dropdown",
            "Has Options": "yes"
        },
        22: {
            "Name": "User",
            "Has Options": "yes"
        },
        23: {
            "Name": "Drilldown",
            "Has Options": "yes"
        }
    }

    def __init__(self, keap: Keap):
        self.keap = keap
        self.get_xmlrpc_client()

    def get_xmlrpc_client(self):
        if not self.keap.token.access_token:
            raise Exception(f"No token set for client {self.keap.app_name}")
        uri = f"{self.xmlrpc_url}?access_token={self.keap.token.access_token}"
        self.client = ServerProxy(uri, use_datetime=self.keap.api_settings.USE_DATETIME,
                                  allow_none=self.keap.api_settings.ALLOW_NONE)
        self.client.error = Error
        return self.client

    def __getattr__(self, method):
        def function(*args):
            return self.call(method, *args)

        return function

    @property
    def service(self):
        return self._service if self._service else self.__class__.__name__

    def call(self, method, *args):
        call = getattr(self.client, f"{self.service}.{method}")
        try:
            return call(self.keap.token.access_token, *args)
        except self.client.error as e:
            error_code = e.errcode
            error_message = e.errmsg
            headers = e.headers
            if error_code == 401:  # Unauthorized
                raise KeapUnauthorizedException(error_message)
            raise KeapException(error_message)

    def server(self):
        return self.client

    def get_table_field_definitions(self, table):
        try:
            with open(f"./tables/{table}.json") as f:
                return json.load(f)
        except Exception:
            pass
        return []
