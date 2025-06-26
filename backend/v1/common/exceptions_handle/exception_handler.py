from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call REST framework's default handler first
    response = exception_handler(exc, context)

    # If exception is handled by DRF
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': response.data.get('detail') if 'detail' in response.data else 'An error occurred.',
            'error': {
                'code': exc.__class__.__name__.upper()
            },
            'data': None
        }
        return Response(custom_response_data, status=response.status_code)

    # If not handled (e.g., non-DRF exceptions), return generic error
    return Response({
        'success': False,
        'message': 'Internal server error.',
        'error': {
            'code': 'INTERNAL_SERVER_ERROR'
        },
        'data': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)