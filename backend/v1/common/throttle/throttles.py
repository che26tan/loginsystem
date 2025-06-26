from rest_framework.throttling import SimpleRateThrottle
from productdetails.models import VisitingLogs
from admin_panel.models import SubscriptionDetails
from productdetails.serializers import get_client_ip

class CustomThrottle(SimpleRateThrottle):

    def get_cache_key(self, request, view):
        self.request = request
        self.ip = get_client_ip(request)
        if request.user.is_authenticated:
            return f"throttle_user_{request.user.pk}"
        return f"throttle_{self.ip}"

    def get_rate(self):
        if self._is_authenticated():
            profile = getattr(self.request.user, 'profile', None)
            if profile:
                throttle = SubscriptionDetails.get_throttle_limit(profile)
                return throttle if throttle else None  # None = unlimited
        return '25/day'  # Default for outsiders

    def _is_authenticated(self):
        try:
            return self.request.user and self.request.user.is_authenticated
        except:
            return False
