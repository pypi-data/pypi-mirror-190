import requests
import json
from etpay_sdk import Configs
from etpay_sdk import TransactionParams
from etpay_sdk import ApiConstants
import jwt

class Transactions():
    def __init__(self, configure: Configs, transaction_params: TransactionParams):

        # Error Handler
        if(isinstance(configure, Configs) == False):
            raise TypeError("Type use in 'configure' is incorrect")
        if(isinstance(transaction_params, TransactionParams) == False):
            raise TypeError("Type use in 'transaction_params' is incorrect")

        self.__configuration = configure
        self.__params = transaction_params


    def create(self) -> json:
        """
        Method to create transaction and get response with tokens.
        :return: REQUEST response
        """

        URL = self.__configuration.get_api_url() + ApiConstants.INITIALIZE_ENDPOINT.value

        try:
            auth_data = self.__params.authentication_data_create(self.__configuration)
            authentication_data = json.dumps(auth_data)

            response = requests.post(URL, authentication_data)
            return response
        except:
            print("Unexpected error.")
            raise

    def status(self, payment_token:str = None, merchant_order_id:str = None, session_token:str = None):
        """
        Method to consult payment status. Require at least one argument to work properly.
        :param payment_token: str for payment token
        :param merchant_order_id: str for merchant order id
        :param session_token: str for session token
        :return: JSON
        """
        
        if(payment_token == None and 
            merchant_order_id == None and 
            session_token == None):
            raise ValueError("The function requires at least one argument")

        #if(type(payment_token) != str or 
        #    type(merchant_order_id) != str or 
        #    type(session_token) != str):
        #    raise ValueError("All arguments are str")

        URL = self.__configuration.get_api_url() + ApiConstants.STATUS_ENDPOINT.value

        data ={}
        data["merchant_api_token"] = self.__configuration.get_merchant_api_token()

        if(payment_token != None):
            data["payment_token"] = payment_token
        if(merchant_order_id != None):
            data["merchant_order_id"] = merchant_order_id
        if(session_token != None):
            data["session_token"] = session_token

        try:
            json_data = json.dumps(data)
            response = requests.post(URL, json_data)

            return response
        except:
            print("Unexpected error.")
            raise


    def verify(self, token: str, signature_token: str) -> json:
        """
        Method to verify JWT returning the JSON inside.
        :param token: str for JWT
        :param signature_token: str for signature token
        :return: JSON
        """

        # Error Handler
        if(isinstance(token, str) == False):
            raise TypeError("Type use in 'token' is incorrect")
        if(isinstance(signature_token, str) == False):
            raise TypeError("Type use in 'signature_token' is incorrect")

        try:
            decode = jwt.decode(token, signature_token, ["HS256"])
            return decode
        except:
            raise
            
