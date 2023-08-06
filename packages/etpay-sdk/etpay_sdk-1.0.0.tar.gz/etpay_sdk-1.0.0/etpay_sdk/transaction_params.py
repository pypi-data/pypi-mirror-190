from etpay_sdk import Metadata
from etpay_sdk import Configs
import json

class TransactionParams():
    def __init__(self,  
                merchant_order_id: str = None, 
                order_amount: int = None,
                customer_email: str = None, 
                payment_completed_url: str = None,
                payment_cancellation_url: str = None, 
                user_bank_code: str = None,
                user_rut: str = None,
                is_rut_block: str = None, 
                concat: str = None,
                metadata:Metadata = None):

        # Id used by the merchant to identify the transaction.
        self.merchant_order_id = merchant_order_id
        # Transaction amount.
        self.order_amount = order_amount
        # Customer email.
        self.customer_email = customer_email
        # URL to which the API will redirect in the event of a successful payment.
        self.payment_completed_url = payment_completed_url
        # URL to which the API will redirect in the event that the payer explicitly cancels the payment, or an unforeseen error occurs.
        self.payment_cancellation_url = payment_cancellation_url
        # If this field is sent, the session starts with the bank already selected.
        self.user_bank_code = user_bank_code
        # If this field is sent, the session starts with the client's RUT already entered in the respective field.
        self.user_rut = user_rut
        # If this field is sent, the session starts with the client's RUT field already blocked. Important to consider sending `user_rut` together wit this attribute.
        self.is_rut_block = is_rut_block
        # When merchants have URLs that vary based on different inputs, this value is what ETpay uses to recognize the character/symbol that concatenates those inputs.
        self.concat = concat
        # Data showing on transaction process
        self.metadata = metadata

    def authentication_data_create(self, configuration: Configs) -> json:
        """
        Create JSON with all the data required to create transaction.
        :param configuration: Configs object with base data
        :return: JSON
        """
        data ={}

        data["merchant_code"] = configuration.get_merchant_code()
        data["merchant_api_token"] = configuration.get_merchant_api_token()

        if(self.merchant_order_id != None):
            data["merchant_order_id"] = self.merchant_order_id
        if(self.order_amount != None):
            data["order_amount"] = self.order_amount
        if(self.customer_email != None):
            data["customer_email"] = self.customer_email
        if(self.payment_completed_url != None):
            data["payment_completed_url"] = self.payment_completed_url
        if(self.payment_cancellation_url != None):
            data["payment_cancellation_url"] = self.payment_cancellation_url
        if(self.user_bank_code != None):
            data["user_bank_code"] = self.user_bank_code
        if(self.user_rut != None):
            data["user_rut"] = self.user_rut
        if(self.is_rut_block != None):
            data["is_rut_block"] = self.is_rut_block
        if(self.concat != None):
            data["concat"] = self.concat
        if(self.metadata != None):
            data["metadata"] = self.metadata.get_data()

        return data