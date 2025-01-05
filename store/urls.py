from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views


router = SimpleRouter()
router.register('products', views.ProductViewSet)

urlpatterns = router.urls
