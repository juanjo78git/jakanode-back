# jakanode-back

## Run
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Generate secret key
```python
import secrets

secret_key = secrets.token_hex(32)  # Genera una clave de 64 caracteres (256 bits)
print(secret_key)
```

