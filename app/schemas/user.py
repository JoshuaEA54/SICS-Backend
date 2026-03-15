# Validación de datos que entran y salen por la API
# Son clases Pydantic que definen qué datos acepta un endpoint y 
# qué datos devuelve. No tienen nada que ver con la BD directamente.

# Pydantic es una librería de Python que se encarga de validar y 
# transformar datos automáticamente.
# La idea central es simple: vos definís una clase que describe la 
# forma que deben tener tus datos, y Pydantic se asegura de que lo que 
# llegue cumpla con esa forma. Si no cumple, lanza un error automáticamente.