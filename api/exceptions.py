from rest_framework.exceptions import APIException


class SyncFailed(APIException):
    status_code = 400
    default_detail = "Syncing of data from SWAPI has failed!"
    default_code = "sync_fail"