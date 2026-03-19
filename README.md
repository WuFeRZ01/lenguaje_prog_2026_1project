# Tool Lending CLI

Aplicación de terminal (CLI) para gestionar préstamos de herramientas.
Permite administrar herramientas y miembros, y registrar préstamos/devoluciones aplicando reglas de negocio.

## Propósito y alcance
- CRUD básico de herramientas (crear/listar/actualizar/eliminar)
- CRUD básico de miembros (crear/listar)
- Préstamos y devoluciones con reglas:
  - No prestar si no hay stock
  - No permitir doble préstamo activo del mismo tool por el mismo miembro
  - No devolver préstamos inexistentes o ya devueltos

Arquitectura por capas:
- `models.py`: dataclasses (solo datos)
- `storage.py`: lectura/escritura JSON (única capa autorizada)
- `services.py`: lógica de negocio + CRUD
- `exceptions.py`: excepciones personalizadas
- `main.py`: interacción CLI (Typer + Rich)

 Instalación (uv)
1. Instalar uv (si no lo tienes):
   - `pip install uv`

2. Instalar dependencias:
   - `uv sync`

## Uso de la CLI
Ejemplos:

- Crear herramienta:
  - `uv run python main.py add-tool --name "Taladro" --category "Electricas" --stock 2`

- Listar herramientas:
  - `uv run python main.py list-tools`

- Crear miembro:
  - `uv run python main.py add-member --name "Samu"`

- Listar miembros:
  - `uv run python main.py list-members`
- Prestar herramienta:
  - `uv run python main.py loan --member-id 1 --tool-id 1`

- Listar préstamos:
  - `uv run python main.py list-loans`
  - `uv run python main.py list-loans --active-only`

- Devolver préstamo:
  - `uv run python main.py return-loan --loan-id 1`

## Testing
- Ejecutar pruebas:
  - `uv run pytest`

## Lint
- Ejecutar ruff:
  - `uv run ruff check .`
