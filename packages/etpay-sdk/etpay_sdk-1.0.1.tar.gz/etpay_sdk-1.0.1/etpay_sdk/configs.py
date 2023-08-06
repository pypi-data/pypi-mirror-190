
class Configs:
    def __init__(self, merchant_code: str, merchant_api_token: str, api_url: str):
        self.__merchant_code = merchant_code
        self.__merchant_api_token = merchant_api_token
        self.__api_url = api_url

    # Setters
    def set_merchant_code(self, new_merchant_code: str):
        """
        Set a new value to merchant code.
        :param new_merchant_code: str with the new merchant code
        """
        self.__merchant_code = new_merchant_code

    def set_merchant_api_token(self, new_merchant_api_token: str):
        """
        Set a new value to merchant api token.
        :param new_merchant_api_token: str with the new merchant api token
        :return: JSON
        """
        self.__merchant_api_token = new_merchant_api_token

    def set_api_url(self, new_api_url: str):
        """
        Set a new value to api url.
        :param new_api_url: str with the new api url
        :return: JSON
        """
        self.__api_url = new_api_url


    # Getter
    def get_merchant_code(self) -> str:
        """
        Get the value to merchant code.
        :return: STR
        """
        return self.__merchant_code

    def get_merchant_api_token(self) -> str:
        """
        Get the value to merchant api token.
        :return: STR
        """
        return self.__merchant_api_token

    def get_api_url(self) -> str:
        """
        Get the value to api url.
        :return: STR
        """
        return self.__api_url