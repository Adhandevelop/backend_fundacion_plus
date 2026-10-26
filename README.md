# backend_fundacion_plus
repositorio dedicado al backend necesario para la plataforma de la fundacion Plus 

## Backend Django básico

### Instalación
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Endpoints API
- `POST /api/login/`  
  Recibe únicamente:
  ```json
  {
    "username": "usuario",
    "password": "clave"
  }
  ```
  Responde con token, usuario y rol (`cliente` o `administrativo`).

- `GET /api/clientes/me/`  
  Solo para usuarios autenticados de tipo cliente.

- `GET /api/administrativos/me/`  
  Solo para usuarios autenticados de tipo administrativo (`is_staff=True`).
