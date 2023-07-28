# ***********************************************************************************
# File Name: ret_code.py
# Author: Dimitar
# Created: 2020-02-21
# Description: Result Codes Constants For AutoserviceDashboard
# -----------------------------------------------------------------------------------

# --------------- Constants For User Authentication --------------- #
AUTH_UNKOWN_ERROR                = -101
AUTH_SUCCESS                     = 0
AUTH_USER_NOT_FOUND              = 101
AUTH_PHONE_NUMBER_DUPLICATED     = 102
AUTH_WRONG_PWD                   = 103
AUTH_ACCOUNT_DISABLED            = 104


# --------------- Constants For User Registration --------------- #
REG_UNKOWN_ERROR                = -101
REG_SUCCESS                     = 0
REG_EXISTING_EMAIL              = 101
REG_EXISTING_PHONE_NUMBER       = 102
REG_INCORRECT_PHONE_NUMBER      = 103
REG_TOO_MANY_REQUESTS           = 104
REG_RISK                        = 105