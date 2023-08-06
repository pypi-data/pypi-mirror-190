# Laboratorio 2 - Inteligencia Artificial

Este laboratorio es una implementacion de las redes bayesianas en python. La librerí, con nombre fcaBayesian utiliza 
la libería de pgmpy para poder hacer todos los análisis de las redes bayesianas.


Los métodos que se encuentran en esta librería son:

- `build_model()`: utiliza los valores obtenidos en los parametros del constructor y crea el modelo de la red bayesiana.

- `enumeracion(variables, evidence)`:  obtiene la variable de forma ['variable'] y la evidencia de la forma {'variable_de_evidencia': evidencia}.

    Un ejemplo de esta llamada es: `bayes.enumeracion(['R'], {'M': 1,})` siendo bayes una instancia de la red bayesiana.

    El valor de retorno es un array con los valores resultantes del metodo de pgmpy `self.inference.query(variables=variables, evidence=evidence)`
           
```python
+------+----------+
| R    |   phi(R) |
+======+==========+
| R(0) |   0.2131 | -> El primer valor en el arreglo del return
+------+----------+
| R(1) |   0.7869 | -> El segundo valor en el arreglo del return
+------+----------+
```

- `obtener_factores`: obtine las dependencias independientes del modelo bayesiano utiliza la funcion get_independecies del objeto model


```python
(U ⟂ M, B)
(U ⟂ B | M)
(U ⟂ M | B)
(U ⟂ S | B, R)
(U ⟂ S | M, B, R)
(M ⟂ U, B)
(M ⟂ B | U)
(M ⟂ U | B)
(M ⟂ S | B, R)
(M ⟂ S | U, B, R)
(S ⟂ U, M | B, R)
(S ⟂ M | U, B, R)
(S ⟂ U | M, B, R)
(B ⟂ U, M)
(B ⟂ M | U)
(B ⟂ U | M) 
```
    

- `representacion_compacta`: utiliza la funcion de la libreria pgmpy `get_cpds()` para obtener todos los cpds y los escribe en un string que lo regresa de la siguiente manera: 

```python
+------+------+
| M(0) | 0.95 |
+------+------+
| M(1) | 0.05 |
+------+------++------+------+
| U(0) | 0.85 |
+------+------+
| U(1) | 0.15 |
+------+------++------+-----+
| B(0) | 0.9 |
+------+-----+
| B(1) | 0.1 |
+------+-----++------+------+------+------+------+
| R    | R(0) | R(0) | R(1) | R(1) |
+------+------+------+------+------+
| B    | B(0) | B(1) | B(0) | B(1) |
+------+------+------+------+------+
| S(0) | 0.98 | 0.88 | 0.95 | 0.6  |
+------+------+------+------+------+
| S(1) | 0.02 | 0.12 | 0.05 | 0.4  |
+------+------+------+------+------++------+------+------+------+------+------+------+------+------+
| M    | M(0) | M(0) | M(0) | M(0) | M(1) | M(1) | M(1) | M(1) |
+------+------+------+------+------+------+------+------+------+
| B    | B(0) | B(0) | B(1) | B(1) | B(0) | B(0) | B(1) | B(1) |
+------+------+------+------+------+------+------+------+------+
| U    | U(0) | U(1) | U(0) | U(1) | U(0) | U(1) | U(0) | U(1) |
+------+------+------+------+------+------+------+------+------+
| R(0) | 0.96 | 0.86 | 0.94 | 0.82 | 0.24 | 0.15 | 0.1  | 0.05 |
+------+------+------+------+------+------+------+------+------+
| R(1) | 0.04 | 0.14 | 0.06 | 0.18 | 0.76 | 0.85 | 0.9  | 0.95 |
+------+------+------+------+------+------+------+------+------+
```

- `completamente_descrita`: Esta funcion devuelve el resultado booleano (true/false) de la comprobacion de si el modelo esta correctamente definido. Utiliza la funcion de pgmpy `check_model()`.



Para crear una instancia del modelo bayesiano se debe de crear un diccionario de la siguiente forma: 

```python
{
    'nodos' : ...
    'edge' : ...
    'probabilidad' : [[nodo, [probabilidades], [evidencia], [evidence_card]]]
}
```

Un ejemplo de esta implementación es lo siguiente:
```python
parametros = {
    'nodos': ['M', 'U', 'R', 'B', 'S'],
    'edge': [['M','R'], ['U','R'], ['B','R'], ['B','S'], ['R','S']],
    'probabilidad':     [['M', [[0.95], [0.05]],[], []], ['U', [[0.85], [0.15]],[], []], ['B', [[0.90], [0.10]],[], []], ['S', [[0.98, .88, .95, .6], [.02, .12, .05, .40]],['R','B'], [2,2]],
        ['R', [[0.96, .86, .94, .82, .24, .15, .10, .05], [.04, .14, .06, .18, .76, .85, .90, .95]],['M','B', 'U'], [2,2,2]]],

}

```

Luego ese diccionario se envia como parametro a la funcion `BayesModel` de la siguiente manera: ```bayes = fca.BayesModel(parametros)```. Luego de esto se puede hacer uso de las funciones explicadas anteriormente.
