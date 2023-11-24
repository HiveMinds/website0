from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import requests
from _typeshed import Incomplete

from .error import RequestError as RequestError
from .error import RequestSetupError as RequestSetupError
from .resources import Balances as Balances
from .resources import Chargebacks as Chargebacks
from .resources import Clients as Clients
from .resources import Customers as Customers
from .resources import Invoices as Invoices
from .resources import Methods as Methods
from .resources import Onboarding as Onboarding
from .resources import Orders as Orders
from .resources import Organizations as Organizations
from .resources import PaymentLinks as PaymentLinks
from .resources import Payments as Payments
from .resources import Permissions as Permissions
from .resources import Profiles as Profiles
from .resources import Refunds as Refunds
from .resources import Settlements as Settlements
from .resources import Subscriptions as Subscriptions
from .version import VERSION as VERSION

class Client:
    CLIENT_VERSION: str
    API_ENDPOINT: str
    API_VERSION: str
    UNAME: str
    OAUTH_AUTHORIZATION_URL: str
    OAUTH_AUTO_REFRESH_URL: str
    OAUTH_TOKEN_URL: str
    api_endpoint: str
    api_version: str
    timeout: Union[int, Tuple[int, int]]
    retry: int
    api_key: str
    access_token: str
    user_agent_components: Dict[str, str]
    client_id: str
    client_secret: str
    set_token: Callable[[dict], None]
    testmode: bool
    @staticmethod
    def validate_api_endpoint(api_endpoint: str) -> str: ...
    @staticmethod
    def validate_api_key(api_key: str) -> str: ...
    @staticmethod
    def validate_access_token(access_token: str) -> str: ...
    payments: Incomplete
    payment_links: Incomplete
    profiles: Incomplete
    methods: Incomplete
    refunds: Incomplete
    chargebacks: Incomplete
    clients: Incomplete
    customers: Incomplete
    orders: Incomplete
    organizations: Incomplete
    invoices: Incomplete
    permissions: Incomplete
    onboarding: Incomplete
    settlements: Incomplete
    subscriptions: Incomplete
    balances: Incomplete
    def __init__(self, api_endpoint: str = ..., timeout: Union[int, Tuple[int, int]] = ..., retry: int = ...) -> None: ...
    def set_api_endpoint(self, api_endpoint: str) -> None: ...
    def set_api_key(self, api_key: str) -> None: ...
    def set_access_token(self, access_token: str) -> None: ...
    def set_timeout(self, timeout: Union[int, Tuple[int, int]]) -> None: ...
    def set_testmode(self, testmode: bool) -> None: ...
    def set_user_agent_component(self, key: str, value: str, sanitize: bool = ...) -> None: ...
    @property
    def user_agent(self) -> str: ...
    def perform_http_call(self, http_method: str, path: str, data: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., idempotency_key: str = ...) -> requests.Response: ...
    def setup_oauth(self, client_id: str, client_secret: str, redirect_uri: str, scope: List[str], token: str, set_token: Callable[[dict], None]) -> Tuple[bool, Optional[str]]: ...
    def setup_oauth_authorization_response(self, authorization_response: str) -> None: ...

def generate_querystring(params: Optional[Dict[str, Any]]) -> Optional[str]: ...
