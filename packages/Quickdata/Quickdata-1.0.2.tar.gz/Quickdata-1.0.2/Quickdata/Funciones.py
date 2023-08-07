import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

def complot(data, var, figsize = None, palette = "PuBu", chart_type = "pie", segmentation = True,
                    segmentation_minimum = 0.015, count_labels = True, count_x_limit = 4, save = False):
    
    """"Grafica una o múltiples variables de un Data Frame de manera sin ponderar (countplot) o ponderada
    (pie o donut chart).
        
        Args:
        
           data: pd.DataFrame
               Dataset a graficar.
           
           var: list
               Lista con una o múltiples variables a graficar.
           
           figsize: tuple (optional)
               Ancho y alto de la figura en la cual se graficará.
               
            Palette: palette name or list (optional)
                Colores a utilizar en el/los gráficos.
                
            Chart_type: 'donut' o 'pie' (optional)
                Tipo de gráfico ponderado.
                
            Segmentation: Bool (optional)
                Agrupación de categorías con poca representación en las variables al momento de crear el pie/donut chart.
                
            Segmentation_minimum: float (optional)
                En caso de incluir segmentación, ponderación mínima por categoría antes de ser segmentada.
                
            count_labels: Bool (optional)
                Activa o desactiva las etiquetas de datos del gráfico sin ponderar.
                
            count_x_limit: int (optional)
                Número de variables máximas permitidas en el eje x del gráfico no ponderado (en caso de superarse se graficará
                en el eje y).
                
            save: Bool (optional)
                Guarda automáticamente en formato .png los gráficos creados."""
    
    
    # Manejo de excepciones
    
    if type(data) != pd.core.frame.DataFrame:
        
        raise ValueError("Unsupported Data Frame format: " + str(type(data)).split(" ")[1][1:-2] + 
                         " (Data Frame must be 'pd.DataFrame')")
    
    
    if type(var) != list:
        
        raise ValueError("Unsupported variable list: " + str(type(var)).split(" ")[1][1:-2] +
                         " (variable list must be a list)")
    
    for x in var:
        
        if type(x) != str:
            
            raise ValueError("Unsupported format for variable '" + str(x) + "'. (Variables must be strings)")
        
        elif x not in list(data.columns):
            
            raise ValueError("Variable '" + str(x) + "' is not found in the DataFrame.")
        
        
    if figsize != None and type(figsize) != tuple:
        
        raise ValueError("Unsupported figsize format: " + str(type(figsize)).split(" ")[1][1:-2] +
                        " (figsize must be a tuple)")
        
    elif figsize != None and len(figsize) != 2:
        
        raise ValueError("Unsupported figsize format: " + str(len(figsize)) + 
                         ". (figsize must be compound by two numbers: width and height)")
    
    
    if type(chart_type) != str:
        
        raise ValueError("Unsupported chart type format: " + str(type(chart_type)).split(" ")[1][1:-2] +
                         " (Chart type must be a string)") 
        
    elif chart_type != "pie" and chart_type != "donut":
        
        raise ValueError("Unsupported chart type: " + str(chart_type) + " (Chart type must be 'donut' or 'pie')")
    
    
    if type(segmentation) != bool:
        
        raise ValueError("Unsupported segmentation format: " + str(type(segmentation)).split(" ")[1][1:-2] +
                         
                         ". (segmentation must be a bool)")
        
    if type(segmentation_minimum) != float:
        
        raise ValueError("Unsupported segmentation_minimum format: " + str(type(segmentation_minimum)).split(" ")[1][1:-2] +
                         
                         ". (segmentation_minimum must be a float between 0.5 and 0.0001)")
    
    elif segmentation_minimum >= 0.5:
        
        raise ValueError("Unsupported segmentation_minimum format: " + str(segmentation_minimum) + 
                         
                         ". (segmentation_minimum must be a float between 0.5 and 0.0001)")
        
    if type(count_labels) != bool:
        
        raise ValueError("Unsupported count_labels format: " + str(type(count_labels)).split(" ")[1][1:-2] +
                         
                         ". (count_labels must be a bool)")
        
        
    if type(count_x_limit) != int or count_x_limit <= 2:
        
        raise ValueError("Unsupported count_x_limit format: " + str(type(segmentation_minimum)).split(" ")[1][1:-2] +
                         
                         ". (count_x_limit must be a int greater than 2)")
    
        
    if type(save) != bool:
        
        raise ValueError("Unsupported save format: " + str(type(save)).split(" ")[1][1:-2] +
                         
                         ". (save must be a bool)")
    
    
    # Características base de los gráficos

    texto_drop = dict(size = 12.5)
    
    dpi=100
    
    wp = {"linewidth": 1, "edgecolor": "black"}
    
    label_type="edge"
    
    edgecolor = "black"
    
    saturation = 1
    
    pctdistance=1.135
    
    labeldistance=1.295
    
    linewidth=1
    
    cols = 2 
    
    rows = len(var) # Número de variables a graficar
    
    subtitle = "Distribución de Variables Sin Ponderar y Ponderadas"
    
    save_name= "complot.png"
    
    plt.style.use(["bmh"])
    
    
    # Características variables de los gráficos
    
    if figsize == None: # Figura de los gráficos
        
        final_figsize = (16, 4 + (rows * 5))
            
    else:
        
        final_figsize = figsize
        
    if rows == 1: # Ubicación del título principal
        
        y_loc = 1.05
        
    elif rows < 10:
        
        y_loc = 1.02
        
    elif rows < 25:
        
        y_loc = 1.01
        
        
    try:
        
        color_palette_count = list(sns.color_palette(palette).as_hex())[
            round(len(list(sns.color_palette(palette).as_hex())) / 2)] # Color único para el countplot
        
    except:
        
        raise ValueError("Unsupported palette name: '" + str(palette)
                         + "'. palette name must be a supported seaborn palette name or a list of colors.")
    
    
    # Configuración previa a graficar 
    
    fig, axes = plt.subplots(figsize=final_figsize, nrows=rows, ncols=cols) 
    
    grafo_count = -1 # Contabilizará el número de gráfico tipo countplot
    
    grafo_pie = 0 # Contabilizará el número de gráfico tipo pie
    
    
    # Creación de bucle de los gráficos
    
    for i in var:
        
        num_var = len(list(data[i].value_counts().index)) # Número de categorías
        
        # Cuenta de los gráficos en el bucle
        
        grafo_count += 2 
        
        grafo_pie += 2
        
        
        # Agregamos un título general
        
        fig.suptitle(subtitle, size = 20, y = y_loc)
        
        # Agregamos títulos personalizados y configuramos los ejes
        
        title_sin_ponderar = str(var[var.index(i)]).capitalize() 
         
        
        if rows != 1: # múltiples filas
                
            axes[var.index(i),0].set_title(title_sin_ponderar, size = 17, loc="center")
            
            # Removemos x, y Ticks
            axes[var.index(i), 0].xaxis.set_ticks_position('none')
            
            axes[var.index(i), 0].yaxis.set_ticks_position('none')
            
            # Espacio entre axes and labels
            axes[var.index(i), 0].xaxis.set_tick_params(pad = 5)
            
            axes[var.index(i), 0].yaxis.set_tick_params(pad = 10)
                
        else: # Única fila
                
            axes[0].set_title(title_sin_ponderar, size = 17, loc="center")
            
            # Removemos x, y Ticks
            axes[0].xaxis.set_ticks_position('none')
            
            axes[0].yaxis.set_ticks_position('none')
            
            # Espacio entre axes and labels
            axes[0].xaxis.set_tick_params(pad = 5)
            
            axes[0].yaxis.set_tick_params(pad = 10)
        
        
        # Creación y ordenado de etiquetas
        
        tipo = ["numero" if x[0] in [str(y) for y in range(0,10)] else "no numero" for x in 
                [str(x) for x in list(data[i].value_counts().index)]] # Detecta el tipo de categoría de las variables
    

        if tipo.count("no numero") > 1: # En algunos casos las variables se conforman con categorías ordinales y
                                        #  alguna nominal tipo "prefer not to say"
            
            labels_pie_sorted = list(data[i].value_counts().index) # Categorías nominales las ordenamos por ponderación
            
            data_pie = data[i].value_counts()
    
        else: 
            
            labels_pie_sorted = list(data.sort_values(by=i, ascending=False) # Las variables con números las ordenamos según
                                     [i].value_counts(sort=False).index)         # sus etiquetas.
            
            data_pie = data.sort_values(by=i, ascending=False)[i].value_counts(sort=False)
            
            
        # Etiquetas de eje
        
        eje_vacio = ""
        
            
        ## GRÁFICO SIN PONDERAR
        
        plt.subplot(rows, cols, grafo_count) 
        
        if num_var <= count_x_limit: # Gráfico sin ponderar eje x
        
            count = sns.countplot(data = data, x= var[var.index(i)], color = color_palette_count, linewidth=linewidth, 
                                  edgecolor= edgecolor, saturation=saturation, order=labels_pie_sorted)  
        
            plt.ylabel(eje_vacio) 
        
            plt.xlabel(eje_vacio) 

                
        else:  # Gráfico sin ponderar eje y
            
            count = sns.countplot(data = data, y= var[var.index(i)], color = color_palette_count, linewidth=linewidth, 
                                  edgecolor= edgecolor, saturation=saturation, order=labels_pie_sorted) 
         
            plt.ylabel(eje_vacio) 
         
            plt.xlabel(eje_vacio) 
            
            
        # Personalizamos las etiquetas de los gráficos
        
        if count_labels == True:
                
            plt.bar_label(count.containers[0], size = 12.5, label_type=label_type) # Colocamos etiquetas 
            
            miles_translator = str.maketrans(".,", ",.")
            
            for t in count.texts: t.set_text("{:,}".format(int(t.get_text())).translate(miles_translator)) # modificamos
                
        
        ## GRÁFICO PONDERADO
        
        plt.subplot(rows, cols, grafo_pie)

        
        # Detección de variables con poca ponderación
        
        variable_others = ["Otros" if x < segmentation_minimum else
                           str(data[i].value_counts(normalize=True).round(5)
                               [data[i].value_counts(normalize=True).round(5) == x].index[0]) 
                           for x in [round(x,5) for x in list(data[i].value_counts(normalize=True))]]
        
        
        if segmentation == True and "Otros" in variable_others:  # Gráfico ponderado con segmentación
            
            data_pie_nueva = data.apply(lambda x: x[i] if (str(x[i]) in [x for x in variable_others if x != "Otros"]) 
                                                  else "Otros", axis=1).value_counts() # Nuevo data frame 
            
            labels_pie_nuevo = list(data_pie_nueva.index)
            
            color_palette_segmentation = list(sns.color_palette(palette, n_colors=len(labels_pie_nuevo)).as_hex())
            
            
            if chart_type == "donut": 
                
                explode_donut_nuevo = tuple([0.05 for x in labels_pie_nuevo])
                
                pie = plt.pie(data_pie_nueva, shadow=False, autopct= '%1.1f%%', startangle=0,
                              colors=color_palette_segmentation, labels= labels_pie_nuevo, textprops=texto_drop, 
                              explode=explode_donut_nuevo,pctdistance=pctdistance, labeldistance=labeldistance)
                
                
                # Creamos efecto de círculo
                
                centre_circle = plt.Circle((0,0),0.70,fc='white') 
    
                fig = plt.gcf() 
                
                fig.gca().add_artist(centre_circle)
            
                if rows != 1: # Aseguramos que el pie se dibuje como circulo
                
                    axes[var.index(i),1].axis('equal') 
                
                else:
                
                    axes[1].axis('equal')
            
                   
            elif chart_type == "pie": 
                
                explode_pie_nuevo = tuple([0.1 for x in labels_pie_nuevo])
         
                pie = plt.pie(data_pie_nueva, shadow=True, autopct= '%1.1f%%',startangle=0,
                            colors=color_palette_segmentation, labels= labels_pie_nuevo, wedgeprops=wp,textprops=texto_drop,
                            explode=explode_pie_nuevo, pctdistance=pctdistance, labeldistance=labeldistance)
  
            
        else: # Gráfico ponderado sin segmentación
            
            color_palette_nosegmentation = list(sns.color_palette(palette, n_colors=len(labels_pie_sorted)).as_hex())
            
            if chart_type == "donut": 
                
                explode_donut = tuple([0.05 for x in labels_pie_sorted])
                
                pie = plt.pie(data_pie, shadow=False, autopct= '%1.1f%%',startangle=0,
                              colors=color_palette_nosegmentation, labels= labels_pie_sorted, textprops=texto_drop,
                              explode=explode_donut, pctdistance=pctdistance, labeldistance=labeldistance)
                
                # Creamos efecto de círculo
                centre_circle = plt.Circle((0,0),0.70,fc='white') 
    
                fig = plt.gcf() 
                
                fig.gca().add_artist(centre_circle)
            
                # Asegura que el pie se dibuje como circulo
                if rows != 1:
                
                    axes[var.index(i),1].axis('equal') # Múltiples axes
                    
                else:
                
                    axes[1].axis('equal') # único axes
                    
            elif chart_type == "pie": 
                
                explode_pie = tuple([0.1 for x in labels_pie_sorted])
         
                pie = plt.pie(data_pie, shadow=True, autopct= '%1.1f%%',startangle=0,
                              colors = color_palette_nosegmentation,
                              labels= labels_pie_sorted, wedgeprops=wp,textprops=texto_drop,explode=explode_pie,
                              pctdistance=pctdistance, labeldistance=labeldistance)

        
    fig.execute_constrained_layout() # Configuramos la figura para evitar superposiciones
    
    if save != False: 
        
        plt.savefig(save_name, dpi=100, bbox_inches="tight") # Configuración del salvado 
    
    fig.canvas.draw()