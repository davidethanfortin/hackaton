# Query Generator API

A FastAPI application for generating SQL queries.

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API docs available at `http://localhost:8000/docs`

## Usage Examples

### SELECT Query
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "table": "users",
    "operation": "select",
    "columns": ["id", "name", "email"],
    "conditions": {"status": "active"}
  }'
```

### INSERT Query
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "table": "users",
    "operation": "insert",
    "values": {"name": "John Doe", "email": "john@example.com"}
  }'
```

### UPDATE Query
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "table": "users",
    "operation": "update",
    "values": {"status": "inactive"},
    "conditions": {"id": "1"}
  }'
```

### DELETE Query
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "table": "users",
    "operation": "delete",
    "conditions": {"id": "1"}
  }'
```
