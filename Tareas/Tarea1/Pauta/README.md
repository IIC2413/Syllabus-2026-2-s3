# Cómo se revisaron los test cases en la Parte 3

Cada función se probó con los 15 test cases de Tarea1_test_cases_P3.json.

## Ejecución
- Se extrajo la función del Jupyter Notebook, sin ejecutar el resto de las celdas.
- Cada caso se ejecutó de forma aislada, con un límite de 60 segundos.
- Las funciones recibieron como "db_path" una copia de la base de datos de la solución, no la generada por el estudiante. Así se evitan errores de arrastre.

## Comparación con la solución
- Se compara el contenido completo del resultado: las mismas filas con los mismos valores que la solución, incluidas las filas repetidas.
- El orden de las filas y de las columnas no importa.
- Se acepta cualquier tipo de retorno razonable.