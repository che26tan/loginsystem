from rest_framework.response import Response
from rest_framework import status


def standard_response(success, message, data=None, error=None, code=status.HTTP_200_OK):
    return Response({
        'success': success,
        'message': message,
        'data': data,
        'error': error
    }, status=code)
