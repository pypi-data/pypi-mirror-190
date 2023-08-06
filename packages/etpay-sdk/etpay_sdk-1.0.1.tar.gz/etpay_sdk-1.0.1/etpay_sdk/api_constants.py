from enum import Enum

class ApiConstants(Enum):
  INITIALIZE_ENDPOINT = '/session/initialize'
  SESSION_ENDPOINT    = '/session'
  STATUS_ENDPOINT     = '/merchant/check_payment_status' 