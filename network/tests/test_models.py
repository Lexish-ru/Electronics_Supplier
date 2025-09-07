"""Тесты валидации модели NetworkNode."""

import pytest
from django.core.exceptions import ValidationError
from network.models import NetworkNode

pytestmark = pytest.mark.django_db


def make_node(name="X", kind="factory", supplier=None) -> NetworkNode:
    """Быстро создаёт узел без сохранения."""
    return NetworkNode(
        name=name,
        kind=kind,
        email=f"{name.lower()}@test.com",
        country="RU",
        city="Moscow",
        street="s",
        house_number="1",
        supplier=supplier,
    )


def test_cycle_not_allowed():
    """Циклические связи запрещены (A→B→A)."""
    a = make_node(name="A")
    a.save()
    b = make_node(name="B", kind="retail", supplier=a)
    b.save()
    a.supplier = b
    with pytest.raises(ValidationError):
        a.clean()


def test_depth_more_than_three_not_allowed():
    """Глубина > 2 (уровень 3) вызывает ValidationError."""
    f = make_node(name="F", kind="factory")
    f.save()
    r = make_node(name="R", kind="retail", supplier=f)
    r.save()
    s = make_node(name="S", kind="sole", supplier=r)
    s.save()
    too_deep = make_node(name="X", kind="sole", supplier=s)
    with pytest.raises(ValidationError):
        too_deep.clean()


def test_depth_exactly_three_ok():
    """Три уровня (0→1→2) допустимы."""
    f = make_node(name="F", kind="factory")
    f.save()
    r = make_node(name="R", kind="retail", supplier=f)
    r.save()
    s = make_node(name="S", kind="sole", supplier=r)
    s.save()
    assert f.level == 0 and r.level == 1 and s.level == 2
