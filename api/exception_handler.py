from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        return Response({
            'message': 'One or more fields in the request data are invalid!',
            'errors': response.data
        }, status=response.status_code)

    message = "An unexpected error occurred!"

    if response and hasattr(response, 'data') and 'detail' in response.data:
        message = response.data['detail']

    if response is None:
        return Response({
            'message': "An unexpected server error occurred!",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'message': message,
    }, status=response.status_code)
