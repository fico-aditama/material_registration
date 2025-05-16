# Material Registration Odoo 14 Module

Modul ini digunakan untuk registrasi material yang akan dijual, sesuai kebutuhan client.

## Entity Relationship Diagram (ERD)

```
+-------------------------+         +-------------------+
| material.registration   |         |   res.partner     |
+-------------------------+         +-------------------+
| id (PK)                 |         | id (PK)           |
| material_code (unique)  |         | name              |
| name                    |         | ...               |
| material_type           |         +-------------------+
| buy_price               |
| supplier_id (FK) -------+-------->|
+-------------------------+
```

- **material.registration.supplier_id** adalah Foreign Key ke **res.partner.id** (Supplier).
- **material_type** adalah enum: Fabric, Jeans, Cotton.
- **buy_price** harus >= 100.

## Fitur
- CRUD Material (REST API)
- Filter by Material Type
- Validasi harga beli
- Relasi ke Supplier (res.partner)
- Unit test lengkap


## Contoh Request & Response

### Create Material (POST /api/materials)
Request:
```
{
  "material_code": "MAT001",
  "name": "Kain Katun",
  "material_type": "cotton",
  "buy_price": 150,
  "supplier_id": 5
}
```

Response:
```
{
  "status": "success",
  "id": 12,
  "message": "Material created successfully"
}
```

### Filter by Type (GET /api/materials?material_type=jeans)
Response:
```
{
  "status": "success",
  "data": [
    {
      "id": 13,
      "material_code": "MAT002",
      "name": "Celana Jeans",
      "material_type": "jeans",
      "buy_price": 200,
      "supplier_id": 5,
      "supplier_name": "PT Denim"
    }
  ]
}
```
