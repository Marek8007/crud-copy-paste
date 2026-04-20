# Applety

Mini utilidad de bandeja para KDE Plasma.

## Uso

1. Edita `applet.py` y cambia los textos de `TEXT_ITEMS`.
2. Ejecuta `./run.sh`.

## Notas

- La ventana se abre cerca del cursor para que quede accesible al hacer clic en el icono.
- Si quieres que se abra exactamente en otra posición, se puede ajustar luego.
- El icono que usa la app sale del tema de iconos de KDE si existe el SVG local; en Plasma normalmente ese tema es `Breeze`.
- Para probar iconos del tema, en KDE suelen servir nombres como `edit-copy`, `edit-paste`, `document-new`, `view-pdu`, `dialog-information`, `folder`, `starred`, `favorites`, `emblem-favorite`.
