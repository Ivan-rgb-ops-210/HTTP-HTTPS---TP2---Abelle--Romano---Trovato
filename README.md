## Introducción a la investigación

La investigación detrás de este proyecto se centra en entender los fundamentos del protocolo HTTP y cómo un servidor puede manejar peticiones desde un navegador. Además, explora cómo un juego clásico como el ajedrez se puede modelar en Python mediante notación FEN y movimientos válidos, y cómo la lógica del juego puede comunicarse con una interfaz web.

## Qué contiene la implementación

- `server.py`: servidor HTTP en Python que atiende solicitudes entrantes.
- `templates/index.html`: página principal del juego.
- `templates/style.css`: estilos para la interfaz de usuario.
- `static/script.js`: lógica del frontend para conectarse con el servidor y mover piezas.

El servidor maneja:

- `GET /` para servir la página HTML.
- `GET /join` para unir jugadores y asignar rol (`white`, `black` o espectador).
- `GET /board` para devolver el estado actual del tablero.
- `POST /move` para recibir movimientos en formato UCI y validar reglas de ajedrez.

## Requisitos previos

Antes de correr el proyecto, debes tener instalado:

- Python 3.8 o superior
- `pip` (administrador de paquetes de Python)

También necesitas instalar la dependencia de Python usada en el servidor:

```bash
pip install chess
```

## Cómo ejecutar el código

1. Abre una terminal.
2. Navega a la carpeta del servidor:

```bash
cd "Http Ajedrez Abelle-Romano-Trovato\Http Ajedrez Abelle-Romano-Trovato\ajedrez-http"
```

3. Ejecuta el servidor:

```bash
python server.py
```

4. El servidor imprimirá una dirección como `http://<tu-ip>:5000` y abrirá automáticamente el navegador.
5. Si el navegador no se abre, copia la dirección mostrada e intenta acceder desde tu navegador.

## Notas importantes

- El servidor abre el navegador con la URL local según la IP de tu equipo.
- Solo dos jugadores pueden unirse como blancas y negras. Los visitantes adicionales serán espectadores.
- El código usa un servidor HTTP básico construido con `socket`, por lo que no es adecuado para producción.

## Estructura del proyecto

```text
Http Ajedrez Abelle-Romano-Trovato/
  Http Ajedrez Abelle-Romano-Trovato/
    ajedrez-http/
      server.py
      static/
        script.js
      templates/
        index.html
        style.css
```

## Advertencias

- No se han incluido mecanismos avanzados de seguridad.
- El servidor no maneja HTTPS ni múltiples sesiones independientes.
- Está diseñado para un entorno local de prueba y demostración.
