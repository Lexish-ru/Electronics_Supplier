import pytest
from network.models import NetworkNode

pytestmark = pytest.mark.django_db


def test_clear_debt_sets_zero():
    """clear_debt обнуляет долг."""
    f = NetworkNode.objects.create(
        name="F", kind="factory",
        email="f@f", country="RU", city="M", street="s", house_number="1",
        debt_to_supplier="123.45"
    )
    f.clear_debt()
    f.refresh_from_db()
    assert str(f.debt_to_supplier) == "0.00"


def test_level_breaks_on_cycle():
    """level корректно работает при цикле."""
    a = NetworkNode.objects.create(
        name="A", kind="factory",
        email="a@a", country="RU", city="M", street="s", house_number="1"
    )
    b = NetworkNode.objects.create(
        name="B", kind="retail",
        email="b@b", country="RU", city="M", street="s", house_number="2", supplier=a
    )
    a.supplier = b
    a.save()
    assert isinstance(a.level, int)


def test_str_returns_name():
    """__str__ возвращает имя узла."""
    f = NetworkNode.objects.create(
        name="FactoryX", kind="factory",
        email="fx@fx", country="RU", city="M", street="s", house_number="1"
    )
    assert str(f) == "FactoryX"
