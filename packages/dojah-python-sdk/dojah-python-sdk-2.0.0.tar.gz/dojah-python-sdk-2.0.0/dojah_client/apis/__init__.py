
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from dojah_client.api.aml_api import AMLApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from dojah_client.api.aml_api import AMLApi
from dojah_client.api.authentication_api import AuthenticationApi
from dojah_client.api.financial_api import FinancialApi
from dojah_client.api.ghkyc_api import GHKYCApi
from dojah_client.api.general_api import GeneralApi
from dojah_client.api.kekyc_api import KEKYCApi
from dojah_client.api.kyb_api import KYBApi
from dojah_client.api.kyc_api import KYCApi
from dojah_client.api.ml_api import MLApi
from dojah_client.api.services_api import ServicesApi
from dojah_client.api.ugkyc_api import UGKYCApi
from dojah_client.api.wallet_api import WalletApi
from dojah_client.api.web_hooks_api import WebHooksApi
