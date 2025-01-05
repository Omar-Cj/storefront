from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views


router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls
