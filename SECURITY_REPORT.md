# Informe confidencial para Google VRP

## Resumen

Este informe describe un posible escape del sandbox de V8 mediante corrupción de
metadatos internos de WebAssembly. El repositorio contiene un PoC que usa APIs
disponibles únicamente en `d8` con `--sandbox-testing` y termina construyendo
primitivas de lectura y escritura de 64 bits en memoria de V8.

El hallazgo debe enviarse de forma privada a Google VRP. No se debe publicar ni
ejecutar el PoC contra productos, servicios o infraestructura de terceros.

## Producto afectado

- Componente: V8, especialmente WebAssembly y el sandbox de V8.
- Entorno indicado por el PoC: shell `d8` con `--sandbox-testing`.
- Versión exacta: pendiente de determinar.
- Plataforma: pendiente de determinar.
- Commit del repositorio: `1bb28860cbca49445756ca32ee188fdc4bd065df`.

La versión afectada no puede inferirse de forma fiable solo a partir de este
repositorio. Debe probarse únicamente contra builds oficiales o de laboratorio
autorizadas por Google.

## Impacto potencial

Si el comportamiento es reproducible en una build afectada, un atacante podría
superar las garantías del sandbox de V8 y leer o escribir memoria fuera de los
objetos que normalmente controla JavaScript/WebAssembly. Dependiendo de las
protecciones restantes del proceso, esto podría permitir corrupción de memoria,
alteración de estructuras confiables y una escalada posterior dentro del
proceso embebedor.

El impacto final, la explotabilidad en productos de Google y la elegibilidad
para recompensa requieren confirmación por parte del equipo de Google VRP.

## Análisis técnico

El PoC realiza, en orden, estas operaciones relevantes:

1. Crea una vista sobre `Sandbox.MemoryView` y define funciones basadas en
   `Sandbox.getAddressOf` y `Sandbox.getObjectAt`.
2. Lee el campo interno de la tabla WebAssembly asociado a
   `TrustedDispatchTable` y calcula un desplazamiento entre handles.
3. Sustituye el handle de una tabla por otro y fuerza un crecimiento de la
   tabla, intentando provocar una liberación y reutilización de una entrada
   interna de WebAssembly.
4. Reutiliza esa entrada con una función WebAssembly compatible y modifica la
   representación de una `CanonicalSig`.
5. Obtiene funciones `read64` y `write64`; el archivo finaliza con una escritura
   de prueba a una dirección elegida por el autor.

Referencias dentro del PoC:

- `Sandbox.MemoryView`, `getAddressOf` y `getObjectAt`: `poc.js`, sección
  `main exploit`.
- Sustitución de `TrustedDispatchTable` y crecimiento de la tabla: `poc.js`,
  bloque `transplant table to grow`.
- Reutilización de `WasmCPT` y modificación de `CanonicalSig`: `poc.js`,
  bloque `reclaim WasmCPT`.
- Primitivas `read64` y `write64`: `poc.js`, bloque `builder2`.

## Reproducción controlada

No se ha ejecutado el PoC en este entorno y este informe no afirma una
reproducción independiente. Para la validación de VRP, adjuntar el archivo
original de forma privada y proporcionar únicamente:

- hash SHA-256 del archivo adjunto;
- versión exacta de V8/d8 y sistema operativo;
- salida de consola y crash log obtenidos en una máquina desechable;
- si la prueba fue solo un crash o si confirmó lectura/escritura fuera del
  sandbox;
- cualquier mitigación o cambio de build que altere el resultado.

No incluir secretos, datos de usuarios ni pruebas contra servicios en
producción.

## Estado de verificación

- Revisión estática del código: completada.
- Ejecución independiente: no realizada.
- Confirmación de versión afectada: pendiente.
- Confirmación de impacto en productos de Google: pendiente.
- CVE o issue upstream: pendiente.

## Solicitud al equipo VRP

Solicito que Google confirme:

1. si el comportamiento alcanza una frontera de seguridad cubierta por Google
   VRP;
2. las versiones y productos afectados;
3. la severidad y elegibilidad del informe;
4. el canal seguro para compartir el PoC completo y artefactos adicionales.

## Divulgación responsable

Enviar este informe y el PoC completo mediante el portal oficial de Google VRP,
mantener los artefactos privados durante la investigación y esperar autorización
antes de cualquier divulgación pública.