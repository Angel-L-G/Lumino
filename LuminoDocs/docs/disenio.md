## Diseño del Sistema

### Arquitectura del sistema

El sistema sigue una arquitectura Modelo, Vista, Plantilla (MVT) con una base de datos relacional. Los módulos principales incluyen autenticación, gestión académica y más.

### Modelo de datos

El esquema de la base de datos incluye tablas para usuarios, materias y lecciones, con relaciones bien definidas.

![Esquema de ddbb](http://localhost:8000/img/ddbb.png)

### Diagramas

- **Diagrama de clases**: Representación de las entidades del sistema.
- **Diagrama de secuencia**: Flujo de interacción entre componentes.
- **Diagrama de actividades**: Descripción de los procesos clave.

### Decisiones de diseño

Se ha optado por una arquitectura MVT para facilitar la integración con otras plataformas y una base de datos relacional por su consistencia y escalabilidad.
