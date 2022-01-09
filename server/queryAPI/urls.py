from rest_framework import routers

from .views import FilterViewSet

router = routers.DefaultRouter()

router.register(r'filter', FilterViewSet, basename='filter')

urlpatterns = router.urls
