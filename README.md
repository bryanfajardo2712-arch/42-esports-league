# Liga de videojuegos de 42 Barcelona

Aplicacion web pequena hecha con Python y Flask para registrar participantes de una liga.

## Ejecutar

```bash
cd 42-esports-league
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Abre <http://127.0.0.1:5000>.

## Datos guardados

La primera version guarda el usuario de 42 y el nombre visible en `league.db`, una base SQLite creada automaticamente.

Las fotos se cargan desde la CDN publica de 42 usando el nombre de usuario. Si una imagen no existe, se muestra un avatar local.

## Aprendizajes

- Flask maneja las rutas HTTP.
- Los formularios HTML envian datos con `POST`.
- SQLite guarda los jugadores aunque reinicies la aplicacion.
- Jinja genera el HTML usando datos de Python.
- Una relacion entre HTML, CSS y Python permite construir una interfaz completa.

## Próximos pasos

1. Agregar organizacion por torneos y partidas.
2. Crear llaves de eliminacion.
3. Conectar la API OAuth de 42 para obtener datos y fotos reales.
4. Agregar autenticacion para proteger altas y bajas.
