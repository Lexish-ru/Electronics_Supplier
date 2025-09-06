# Electronics Network

Иерархическая сеть продаж электроники (завод → розница → ИП).

## Технологии
Python 3.11+, Django 3.2+, DRF 3.10+, PostgreSQL 15, django-filter.

## Запуск (Docker)
```bash
docker compose build
docker compose up -d
docker exec -it electronics_web python manage.py createsuperuser
```
- Admin: http://localhost:8000/admin/
- Health: http://localhost:8000/health
- API:
  - `GET /api/nodes/?country=Russia`
  - `POST/PUT/PATCH/DELETE /api/nodes/`
  - `POST/PUT/PATCH/DELETE /api/products/`

### Доступ к API
Только для пользователей `is_active=True` и `is_staff=True` (Session/BasicAuth).

### Требования ТЗ
- Иерархия из 3 уровней (уровень считается по цепочке `supplier`).
- У каждого узла — один поставщик (`ForeignKey(self)`).
- Админка: ссылка на поставщика, фильтр по городу, admin action “очистить долг”.
- DRF CRUD для поставщиков (узлов), запрет менять `debt_to_supplier` через API.
- Фильтрация по стране (django-filter).
- Права доступа: только активные сотрудники.
