"""API-тесты: CRUD, фильтры, запреты, health."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from network.models import NetworkNode

pytestmark = pytest.mark.django_db


def make_staff() -> APIClient:
    """Создаёт staff-пользователя и возвращает авторизованный клиент."""
    User = get_user_model()
    User.objects.create_user(
        username="staff", password="pass", is_staff=True, is_active=True
    )
    client = APIClient()
    assert client.login(username="staff", password="pass")
    return client


def test_health_endpoint(client):
    """Возвращает 200 и JSON со статусом ok."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_nodes_filter_by_country():
    """Фильтрация узлов по стране работает."""
    NetworkNode.objects.create(
        name="Factory1",
        kind="factory",
        email="f1@test.com",
        country="RU",
        city="Moscow",
        street="s",
        house_number="1",
    )
    NetworkNode.objects.create(
        name="Factory2",
        kind="factory",
        email="f2@test.com",
        country="DE",
        city="Berlin",
        street="s",
        house_number="1",
    )
    c = make_staff()
    resp = c.get("/api/nodes/?country=RU")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1 and data[0]["country"] == "RU"


def test_cannot_update_debt_via_api():
    """Поле задолженности недоступно для изменения через API."""
    f = NetworkNode.objects.create(
        name="Factory",
        kind="factory",
        email="f@test.com",
        country="RU",
        city="Moscow",
        street="s",
        house_number="1",
    )
    n = NetworkNode.objects.create(
        name="Retail",
        kind="retail",
        email="r@test.com",
        country="RU",
        city="Moscow",
        street="s",
        house_number="2",
        supplier=f,
    )
    c = make_staff()
    resp = c.patch(f"/api/nodes/{n.id}/", {"debt_to_supplier": "999.99"}, format="json")
    assert resp.status_code == 200
    n.refresh_from_db()
    assert str(n.debt_to_supplier) == "0.00"


def test_level_property_three_tiers():
    """Уровни 0-1-2 считаются корректно."""
    f = NetworkNode.objects.create(
        name="F",
        kind="factory",
        email="f@f",
        country="RU",
        city="M",
        street="s",
        house_number="1",
    )
    r = NetworkNode.objects.create(
        name="R",
        kind="retail",
        email="r@r",
        country="RU",
        city="M",
        street="s",
        house_number="2",
        supplier=f,
    )
    s = NetworkNode.objects.create(
        name="S",
        kind="sole",
        email="s@s",
        country="RU",
        city="M",
        street="s",
        house_number="3",
        supplier=r,
    )
    assert f.level == 0 and r.level == 1 and s.level == 2
