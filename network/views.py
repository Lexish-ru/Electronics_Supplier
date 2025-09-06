from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, ProductSerializer
from .permissions import IsActiveStaff


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    CRUD для звена сети (оно же поставщик для нижестоящих).
    Фильтрация по стране.
    """

    queryset = (
        NetworkNode.objects.select_related("supplier")
        .prefetch_related("products")
        .all()
    )
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]


class ProductViewSet(viewsets.ModelViewSet):
    """
    Вьюсет продуктов
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveStaff]
