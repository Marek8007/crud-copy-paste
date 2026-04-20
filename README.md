# crud-copy-paste
Utilidad de bandeja construida con PySide6 para gestionar fragmentos de texto reutilizables con persistencia local y copia con un solo clic.
--------------------------------------------------------------------------------------------------------------------------------------------
Tray utility built with PySide6 for managing reusable text snippets with local persistence and one-click copy.

A nivel de sistema, esta app tiene estas limitaciones:

- Está pensada para Linux con entorno gráfico.
- Está hecha con PySide6/Qt, así que necesita tener Python y las dependencias instaladas.
- Depende de que haya bandeja del sistema; si la sesión no la soporta bien, el icono puede no funcionar como esperas.
- La persistencia es local: guarda los textos en un JSON junto a la app, no en la nube.
- No tiene cifrado ni protección especial de los textos guardados.
- No está pensada para ejecutar en segundo plano como servicio del sistema; es una app de usuario normal.
- Está optimizada para KDE/Plasma, así que en otros escritorios puede verse o comportarse distinto.
- El portapapeles funciona con el portapapeles normal del sistema, pero no hace historial ni sincronización entre dispositivos.

  <img width="559" height="623" alt="image" src="https://github.com/user-attachments/assets/21481c4c-7887-4e74-84bd-36db9e238572" />
