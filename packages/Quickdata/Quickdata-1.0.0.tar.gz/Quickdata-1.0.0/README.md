# Quickdata Librery

* * *

### Optimiza tu tiempo como Data Scientist

_Por Diego Alejandro Ramírez Araujo - [Github](https://github.com/Diegoramirez1999)_

Librería que te permitirá **automatizar** y **simplificar** tus labores cotidianas como científico/analista de datos.

Actualmente, su función principal se enfoca en optimizar el análisis univariado de variables categóricas/cualitativas, mediante la visualización automatizada de manera **ponderada** y **sin ponderar** de la variable en cuestión.

Para utilizarlo simplemente necesitas incluir como primer argumento el data frame y como segundo argumento una lista con la/las variables a graficar (los argumentos de personalización son opcionales). La función devolverá una gráfica sin ponderar y ponderada por cada variable.

> 📝 **Note:** Actualmente se están desarrollando otras funciones de automatización de gráficos combinados y detección/tratamiento/manejo de outliers.

<p align="center">
<img src="https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green">
</p>

* * *

### Prerequisitos 🎬 

1. [Python](https://www.python.org/downloads/)
    
    + [Numpy](https://numpy.org/install/)
    
    + [Pandas](https://pandas.pydata.org/getting_started.html)
    
    + [Matplotlib](https://matplotlib.org/stable/users/getting_started/)
    
    + [Seaborn](https://seaborn.pydata.org/installing.html)
    


* * *

### Funcionalidades del proyecto 🛠️

```Python
pip install Quickdata

from Quickdata import complot
```

- `Funcionalidad simple`: Obtener a través de menos de una línea de código una gráfica sin poderar y ponderada de una variable de tu DataFrame (configuración de axes, figure, títulos, labels y efectos visuales automatizados).

```Python
complot(example,["sexo"])
```

<p align="center">
<img src="complot_s.PNG">
</p>

- `Funcionalidad avanzada`: Introduce múltiple variables de tu DataFrame dentro de la función. Cada variable obtendrá dos gráficos (sin ponderar y ponderado). La función múltiple ordena de manera individual cada variable en el eje x o en y (para múltiples categorías se recomienda utilizar el eje y), agrupa de forma predeterminada las categorías con poca frecuencia para introcucirlas en el gráfico de pie como una sola (mejor visualización) y ordena de forma automática cada variable dependiendo de el tipo de su tipo de dato correspondiete: nominales (ordenados de mayor a menor según la frecuencia) y ordinales (ordinados de menor a mayor según la etiqueta).

```Python
complot(ejemplo,['Rango de edad', 'Familiares vinculados', 'Motivo de estancia'], 
        chart_type="donut", count_labels=False)
```

<p align="center">
<img src="complot_m.PNG">
</p>

> 📝 **Note:** <br>1. El orden de los datos en el gráfico no ponderado varia dependiendo del tipo de categoría.<br>2. El gráfico ponderado de "Familiares vinculados" se encuentra agrupado por default.</b>


- `Otras funcionalidades`: Exportar, guardar y personalizar la configuración interna de los gráficos (paleta de colores, tamaño de figuras, establecer o no segmentación automática, limite de variables a introducir en el eje x, entre otros).

```Python
complot(ejemplo,['Rango de edad', 'Familiares vinculados', 'Motivo de estancia'], 
        chart_type="donut", count_labels=False, count_x_limit=5, palette="inferno", 
        figsize=(15,15), save=True)
```

<p align="center">
<img src="complot_mp.PNG">
</p>

> 📝 **Note:** Entre las nuevas funcionalidades que se están desarrollando, se incluye en una de ellas otorgar libertar absoluta al usuario para configurar cada gráfico de manera individual bajo los mismos atributos que se emplearían en las librerías principales (seaborn y matplotlib).</b>


* * *

### Parámetros ❔

**data**: *pd.DataFrame*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Dataset a graficar.

**var**: *list*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Lista con una o múltiples variables a graficar.

**figsize**: *tuple (optional)*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ancho y alto de la figura en la cual se graficará.

**Palette**: *palette name or list (optional)*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Colores a utilizar en los gráficos.

**Chart_type**: *'donut' o 'pie' (optional)*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tipo de gráfico ponderado.

**Segmentation**: *Bool (optional)*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Agrupación de categorías con poca representación en las variables al momento de crear el pie/donut chart.

**Segmentation_minimum**: *float (optional)*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;En caso de incluir segmentación, ponderación mínima por categoría antes de ser segmentada.

**count_labels**: *Bool (optional)*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Activa o desactiva las etiquetas de datos del gráfico sin ponderar.

**count_x_limit**: *int (optional)*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Número de variables máximas permitidas en el eje x del gráfico no ponderado (en caso de superarse se graficará en el eje y).

**save**: *Bool (optional)*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Guarda automáticamente en formato .png los gráficos creados.

* * *

## Autor 👽

<div>
<img align="left" src="firma_digital.png"/ width="800">
</div>