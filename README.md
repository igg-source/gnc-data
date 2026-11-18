# ADR-000 - Decisiones de Diseño del Dataset v1

Estado: Aprobado
Fecha: 2026-11-17

Contexto
La aplicación Estaciones GNC consume información procedente de los servicios REST del Ministerio para generar un dataset consolidado publicado en GitHub Pages y consumido posteriormente por la aplicación Android y Android Auto.

Decisiones principales
- Dataset versionado mediante campo raíz version
- Consumo de los endpoints oficiales 18 (GNC) y 31 (BGNC)
- Consolidación de estaciones por IDEESS
- Merge incremental sobre el datos.json existente
- Conservación de estaciones desaparecidas temporalmente
- Conservación de combustibles desaparecidos temporalmente
- GNC y BGNC se almacenan como combustibles independientes
- Cada combustible mantiene su propio precio y fecha de actualización
- Una estación puede tener simultáneamente GNC y BGNC
- Los combustibles se identifican por clave (18, 31)
- El tipo de combustible se guarda como campo tipo
- Los datos maestros son únicos por estación
- Actualización automática de datos maestros cuando reaparece una estación
- Corrección automática de dirección y coordenadas cuando el Ministerio las modifica
- fechaActualizacion representa la última fecha recibida desde el Ministerio
- fechaActualizacion no representa la última modificación del precio
- Si un combustible aparece hoy, siempre se actualiza su fechaActualizacion
- Si el precio recibido es igual al anterior, sigue considerándose actualizado
- null en precio ⇒ 0.0
- Cadena vacía en precio ⇒ 0.0
- Valor no numérico en precio ⇒ 0.0
- Precio "0" ⇒ 0.0
- Un precio 0.0 se considera un dato válido recibido del Ministerio
- Latitud y longitud utilizan reglas distintas a las del precio
- Coordenadas null no sobrescriben coordenadas válidas existentes
- Coordenadas vacías no sobrescriben coordenadas válidas existentes
- Coordenadas 0 no sobrescriben coordenadas válidas existentes
- Coordenadas erróneas no sobrescriben coordenadas válidas existentes
- Los textos válidos nunca se sobrescriben con null
- Los textos válidos nunca se sobrescriben con cadenas vacías
- Gestión defensiva frente a respuestas parciales del Ministerio
- Manejo de errores de red sin perder el dataset existente
- Manejo de excepciones por endpoint independiente
- Un fallo en un endpoint no impide procesar el resto
- Eliminación automática de combustibles sin actualizar durante más de 90 días
- Eliminación automática de estaciones que se quedan sin combustibles
- Limpieza automática del dataset durante la generación
- Uso de la zona horaria Europe/Madrid
- Campo raíz fechaDataset para indicar la fecha lógica del dataset
- Campo raíz ultimaGeneracion para auditoría técnica de generación
- Campo raíz numeroEstaciones para control rápido de integridad
- Ordenación final por provincia, municipio y nombre
- Generación de JSON UTF-8 manteniendo caracteres españoles
- Preparado para futuras ampliaciones de combustibles sin romper compatibilidad
- Compatible con reglas de negocio ACTUAL / DESACTUALIZADO / CADUCADO
- Compatible con mostrar varias opciones por estación en la app (GNC y BGNC)
- Preparado para mostrar resultados ordenados por coste independientemente del combustible
- Optimizado para ejecución periódica mediante GitHub Actions
- Preparado para publicación en GitHub Pages como fuente de datos de la app Android

Beneficios
- Conservación de información ante incidencias temporales.
- Soporte para múltiples combustibles por estación.
- Evolución futura compatible mediante versionado.
- Adecuado para Android, Android Auto, GitHub Pages y GitHub Actions.
