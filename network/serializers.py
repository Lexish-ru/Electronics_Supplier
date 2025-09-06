from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product."""

    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели NetworkNode (узел сети)."""

    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), required=False
    )
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id", "name", "kind",
            "email", "country", "city", "street", "house_number",
            "products",
            "supplier", "debt_to_supplier",
            "created_at", "level",
        ]
        read_only_fields = ["created_at", "level"]

    def update(self, instance, validated_data):
        """При обновлении исключает изменение поля задолженности."""
        validated_data.pop("debt_to_supplier", None)
        return super().update(instance, validated_data)
