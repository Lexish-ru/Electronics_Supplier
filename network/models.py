from django.core.exceptions import ValidationError
from django.db import models
from decimal import Decimal


class Product(models.Model):
    """Модель продукта с названием, моделью и датой выхода."""

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    class Meta:
        ordering = ["name", "model"]

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    """Модель узла сети (завод, розничная сеть или ИП)."""

    KIND_CHOICES = [
        ("factory", "Завод"),
        ("retail", "Розничная сеть"),
        ("sole", "ИП"),
    ]

    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)

    email = models.EmailField()
    country = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    street = models.CharField(max_length=150)
    house_number = models.CharField(max_length=30)

    products = models.ManyToManyField(Product, blank=True, related_name="nodes")

    supplier = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="clients"
    )

    debt_to_supplier = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["country", "city"]),
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    def level(self) -> int:
        """Вычисляет уровень узла по цепочке поставщиков."""
        lvl = 0
        node = self
        visited = set()
        while node.supplier is not None:
            if node.pk in visited:
                break
            visited.add(node.pk)
            lvl += 1
            node = node.supplier
        return lvl

    def clean(self):
        """Валидирует отсутствие циклов и ограничение глубины цепочки."""
        seen = set()
        current = self.supplier
        while current is not None:
            if current == self:
                raise ValidationError("Цикл в иерархии поставщиков недопустим.")
            if current.pk in seen:
                raise ValidationError("Обнаружен цикл в иерархии поставщиков.")
            seen.add(current.pk)
            current = current.supplier

        depth = 0
        current = self
        while current.supplier is not None:
            depth += 1
            current = current.supplier
        if depth > 2:
            raise ValidationError(
                "Глубина иерархии не может превышать 3 уровня (0, 1, 2)."
            )

    def clear_debt(self):
        """Обнуляет задолженность перед поставщиком."""
        self.debt_to_supplier = Decimal("0.00")
        self.save(update_fields=["debt_to_supplier"])
