from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


def demo(request):
    return HttpResponse('Admin Panel is working')

class PaymentVerifyViewSet(viewsets.ViewSet):
    @action(methods=["PUT"], url_path='verify', detail=False, permission_classes=[IsAdminUser])
    def payments_verify(self, request):
        pass
        # data = request.data
        # razorpay_order_id = data.get("razorpay_order_id")
        # razorpay_payment_id = data.get("razorpay_payment_id")
        # razorpay_signature = data.get("razorpay_signature")
        #
        # try:
        #     params_dict = {
        #         "razorpay_order_id": razorpay_order_id,
        #         "razorpay_payment_id": razorpay_payment_id,
        #         "razorpay_signature": razorpay_signature,
        #     }
        #     result = razorpay_client.utility.verify_payment_signature(params_dict)
        #
        #     if result:
        #         # Update payment record
        #         payment = Payment.objects.get(order_id=razorpay_order_id)
        #         payment.payment_id = razorpay_payment_id
        #         payment.status = "Completed"
        #         payment.signature = razorpay_signature
        #         payment.updated_at = now()
        #         payment.save()
        #
        #         return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
        #     else:
        #         return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)
        #
        # except Payment.DoesNotExist:
        #     return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        #
        # except:
        #     return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)



class PaymentConfirmViewSet(viewsets.ViewSet):
    @action(methods='POST', url_path='payment_confirm/email', detail=False, permission_classes=[IsAdminUser])
    def payment_confirm_email(self, request):
        pass

    @action(methods='POST', url_path='payment_confirm/phone', detail=False, permission_classes=[IsAdminUser])
    def payment_confirm_phone(self, request):
        pass

class OfferCodeViewSet(viewsets.ViewSet):
    @action(methods='POST', url_path='add', detail=False, permission_classes=[IsAdminUser])
    def admin_panel_offer_code_add(self, request):
        pass

    @action(methods='PUT', url_path='update', detail=False, permission_classes=[IsAdminUser])
    def admin_panel_offer_code_update(self, request):
        pass

    @action(methods='DELETE', url_path='delete', detail=False, permission_classes=[IsAdminUser])
    def admin_panel_offer_code_delete(self, request):
        pass


    @action(methods='GET', url_path='check-valid', detail=False, permission_classes=[AllowAny])
    def admin_panel_offer_code_valid(self, request):
        pass