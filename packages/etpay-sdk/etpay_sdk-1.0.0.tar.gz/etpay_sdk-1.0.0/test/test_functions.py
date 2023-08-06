import etpay_sdk as Etpay

# Test of Configs object getters
def test_configs_getters():
    merchantcode= "merchant_code"
    merchantapitoken= "merchant_api_token"
    apiurl= "api_url"
    
    configure = Etpay.Configs(merchantcode, merchantapitoken, apiurl)

    assert configure.get_api_url() == apiurl
    assert configure.get_merchant_api_token() == merchantapitoken
    assert configure.get_merchant_code() == merchantcode

# Test of Configs object setters
def test_configs_setters():
    merchantcode= "merchant_code"
    merchantapitoken= "merchant_api_token"
    apiurl= "api_url"

    configure = Etpay.Configs(merchantcode, merchantapitoken, apiurl)
    configure.set_api_url("qwerty")
    configure.set_merchant_api_token("1234567")
    configure.set_merchant_code("7654321")

    assert configure.get_api_url() == "qwerty"
    assert configure.get_merchant_api_token() == "1234567"
    assert configure.get_merchant_code() == "7654321"

# Test of UserBankCodes values
def test_bank_codes():
    codes = Etpay.UserBankCodes
    assert codes.CL_BCH.value == 'CL_BCH'
    assert codes.CL_BCI.value == 'CL_BCI'
    assert codes.CL_ESTADO.value == 'CL_ESTADO'
    assert codes.CL_FALABELLA.value == 'CL_FALABELLA'
    assert codes.CL_ITAU.value == 'CL_ITAU'
    assert codes.CL_SANTANDER.value == 'CL_SANTANDER'
    assert codes.CL_SCOTIABANK.value == 'CL_SCOTIABANK'
    assert codes.CL_TEST.value == 'CL_TEST'

    assert codes.MX_AZTECA.value == 'MX_AZTECA'
    assert codes.MX_BANAMEX.value == 'MX_BANAMEX'
    assert codes.MX_BANORTE.value == 'MX_BANORTE'
    assert codes.MX_BANREGIO.value == 'MX_BANREGIO'
    assert codes.MX_BBVA.value == 'MX_BBVA'
    assert codes.MX_SANTANDER.value == 'MX_SANTANDER'
    assert codes.MX_SCOTIABANK.value == 'MX_SCOTIABANK'
    assert codes.MX_TEST.value == 'MX_TEST'

# Test of Api Constants values
def test_api_constants():
    api_const = Etpay.ApiConstants
    assert api_const.INITIALIZE_ENDPOINT.value == '/session/initialize'
    assert api_const.SESSION_ENDPOINT.value == '/session'
    assert api_const.STATUS_ENDPOINT.value == '/merchant/check_payment_status'

# Test of Metadata Object, TransactionParams Object and Transaction Object
def test_transaction_correct():

    #Definition of client data
    merchantcode= "MERCHANT_CODE"
    merchantapitoken= "MERCHANT_API_TOKEN"
    apiurl= "API_URL"

    # Creation of Metadata Object. Usefull in TransactionParams Object to create JSON for '/session/initialize' consult
    metadata = Etpay.Metadata([
        {
            "name":"NAME", 
            "value": "VALUE", 
            "show": True
        },
    ])
    

    # Creation of TransactionParams. Work for containt the parameters for '/session/initialize' JSON
    transaction_param = Etpay.TransactionParams(order_amount=1, 
                                                merchant_order_id="merchant_order_id", 
                                                customer_email="example@example.com",
                                                payment_completed_url="https://www.google.com",
                                                payment_cancellation_url="https://www.google.com",
                                                metadata=metadata)

    # Creation of Configs. Contain configurations parameters of Client
    configure = Etpay.Configs(merchantcode, merchantapitoken, apiurl)

    # Creation of Transactions Object. Contain configurations and parameters for consult methods
    transaction = Etpay.Transactions(configure, transaction_param)

    # Method to make de '/session/initialize' consult and obtain the correct JSON
    create_response = transaction.create()

    assert create_response.status_code == 200
    assert create_response.json()['token']
    assert create_response.json()['signature_token']
    
    
    # Method to make de '/merchant/check_payment_status' consult and obtain the correct JSON
    status_response = transaction.status(merchant_order_id="MERCHANT_ORDER_ID")
    assert status_response.status_code == 200
    assert status_response.json()[0]['payment_token']
    assert status_response.json()[0]['payment_status']

    # Method to verify a JWT using the signature token as a key
    jwt_decode = transaction.verify("eyJhb[...]W668QA", 
                                    "VLlYY[...]l1gLV")