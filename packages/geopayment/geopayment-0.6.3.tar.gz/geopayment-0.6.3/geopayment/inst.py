import time
from decimal import Decimal

from geopayment.providers import TBCInstallmentProvider


class MySmartTbcInstallmentProvider(TBCInstallmentProvider):
    @property
    def merchant_key(self):
        return 'MerchantIntegrationTesting'

    @property
    def campaign_id(self):
        return "204"

    @property
    def key(self):
        return "ibO35FpiEs3NlXuAvv6L28niKRBfBoet"

    @property
    def secret(self):
        return "WStif1GSfGRK7dBM"

    @property
    def service_url(self) -> str:
        return "https://test-api.tbcbank.ge"


if __name__ == "__main__":
    tbc_installment = MySmartTbcInstallmentProvider()
    print(tbc_installment)
    a = tbc_installment.auth()
    print("aa: ", a)
    print(tbc_installment.auth)
    invoice_id = int(time.time())
    products = [{"name": "მაცივარი", "price": Decimal(150.33), "quantity": 1}]
    print('Invoice id: ', invoice_id)
    res = tbc_installment.create(products=products, invoice_id=invoice_id)
    print("sess: ", tbc_installment.session_id)
    print("rul: ", tbc_installment.redirect_url)
    print("Res: ", res)
    # ic = tbc_installment.confirm()
    # print("Confirm: ", ic)
    # st = tbc_installment.status()
    # print("Status: ", st)
    # sts = tbc_installment.statuses()
    # print("STSTS: ", sts)
    # c = tbc_installment.cancel()
    # print('Cancel: ', c)
    # st = tbc_installment.status()
    # print('Status: ', st)


    # https://test-api.tbcbank.ge/v1/online-installments/applications/{{sessionId}}/confirm
    # https://test-api.tbcbank.ge/v1/online-installments/applications/1809d86a-5ab0-4b72-8e19-3ff0b0a963b5/confirm