# Template de ejercicio complejo

Este directorio no se carga desde `catalog.py`.

Usalo como referencia para ejercicios grandes, por ejemplo un juego isometrico con assets:

```text
mi_proyecto_complejo/
  __init__.py
  manifest.py
  assets/
    sprites/
    tiles/
    audio/
  domain/
  services/
  systems/
  ui/
```

La aplicacion principal solo debe conocer `manifest.py`. Mantener el resto encapsulado permite que el proyecto crezca sin afectar el selector ni otros ejercicios.

