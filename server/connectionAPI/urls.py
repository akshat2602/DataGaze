from rest_framework import routers

from .views import ConnectionViewSet

router = routers.DefaultRouter()

router.register(r'connection', ConnectionViewSet, basename='connection')


urlpatterns = router.urls