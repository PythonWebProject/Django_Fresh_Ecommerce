from alipay import AliPay
from urllib.parse import urlparse, parse_qs

# 沙箱环境应用私钥
app_private_key_string = open('../trade/keys/app_private.txt').read()
# 支付宝公钥
alipay_public_key_string = open( '../trade/keys/ali_public.txt').read()

def get_alipay_url():
    alipay = AliPay(
        appid="2021000116666333",
        app_notify_url='http://127.0.0.1:8000/alipay/return/',
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=True,
    )
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="2020073117084113410",
        total_amount='0.01',
        subject="测试支付宝付款",
        return_url='http://127.0.0.1:8000/alipay/return/',
        notify_url='http://127.0.0.1:8000/alipay/return/'
    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    print(pay_url)


def query_pay():
    alipay = AliPay(
        appid="2021000116666333",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=True,
    )
    trade_query = alipay.api_alipay_trade_query(
        out_trade_no=2020073117084113308,
        trade_no=None
    )

    print(trade_query)

def verify_query(return_url):
    alipay = AliPay(
        appid="2021000116666333",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=True,
    )

    o = urlparse(return_url)
    print(o)
    query = parse_qs(o.query)
    print(query)
    processed_query = {}
    ali_sign = query.pop("sign")[0]
    for key, value in query.items():
        processed_query[key] = value[0]

    print(alipay.verify(processed_query, ali_sign))

if __name__ == '__main__':
    get_alipay_url()
    query_pay()
    # verify_query('https://openapi.alipaydev.com/gateway.do?app_id=2021000116666333&biz_content=%7B%22subject%22%3A%22%5Cu6d4b%5Cu8bd5%5Cu652f%5Cu4ed8%5Cu5b9d%5Cu4ed8%5Cu6b3e%22%2C%22out_trade_no%22%3A%222020073117084113330%22%2C%22total_amount%22%3A%2210.01%22%2C%22product_code%22%3A%22FAST_INSTANT_TRADE_PAY%22%7D&charset=utf-8&method=alipay.trade.page.pay&notify_url=http%3A%2F%2F127.0.0.1%3A8000%2Fxadmin%2Falipay%2Freturn%2F&return_url=http%3A%2F%2F127.0.0.1%3A8000%2Fxadmin%2Falipay%2Freturn%2F&sign_type=RSA2&timestamp=2020-08-02+07%3A50%3A04&version=1.0&sign=CFSWoXxxE2Xs6P63H0QlErY0LM77KwlGzFyhB4eHD4bQW6EEaQbsnIXWf2Ihinw1YXicsAeBPVSH8tUbVVsbAVRUnHFC%2BPs%2Fk1RfOW2sCrcOm17%2B7FChlcrC78lZQcgMSSCYl4UBsqJkQMeGMeD6LbL555oSI9WAwqGN0q0K8Xxq9b7T6TUefDWRDECzJeRrlrA8coo6Y3R1SsFr0woUeQLquzbMQC2zM%2BhB1rPCWECj91xMu%2BzK2PV2EbJad7YT1DypslUStxmlx3N0xHsZYTOEuKJCqlyVT1MzskKnwQj7MQOMQvQtx7xy2NmGmITz2xyQvyng9lHrcYjQuH9PYA%3D%3D')