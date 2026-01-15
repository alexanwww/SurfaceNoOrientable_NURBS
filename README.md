# SurfaceNoOrientable_NURBS
Este repositorio contiene el archivo **SuperficiesNoOrientables.ipynb** dedicado a la construcción y visualización de superficies no orientables, específicamente la banda de Möbius y la botella de Klein. Para ello se utilizan curvas y superficies NURBS, aprovechando su capacidad para representar geometría suave y controlable en computación gráfica. Por otro lado, tiene el archivo **SuperficiesNoOrientables.py**, que contiene todas las clases para construir y visualizar estas superficies. La importancia de este archivo es que se puede usar en otro importando lo que se necesita, sin necesidad de copiar todas las clases (fíjese en el archivo **EjemplosSuperficies.ipynb**).
Además, contiene una carpeta con algunas imágenes de estas superficies no orienatbles que se generó con las clases del archivo .ipynb

**Clases**   
✔️ Bases_curves: Construye las funciones base B-Spline.  
✔️ Nurbs_curbs: Construye la curva Nurbs.  
✔️ Construccion:   Construye pesos, nodos y puntos de control de una circunferencia.  
✔️ Nurbs_surface: Cosntruye la superficie Nurbs.  
✔️ Nurbs_NonOrientPy_graph: Permite visualizar las superficies no orientables.

**Caracteristicas**  
✔️ Modelado de superficies no orientables mediante Nurbs.  
✔️ Controla parámetros como si visualizar enmallado y especificar los rangos de u y v en la superficie no orientable Nurbs S(u,v).  
✔️ Renderizado en tiempo real con Plotly.

**Instalación**  
✔️ Descargue el archivo SuperficiesNoOrientables.py  
✔️ Cargue el archivo descargado en cualquier sesión de jupyter notebook o en google colab (mejor es montar con el drive para que no eliminen el archivo local).  
&nbsp;&nbsp;&nbsp;&nbsp;✔️ Primero crea una carpeta en el drive (ej. ArchivosPy), luego subes el archivo SuperficiesNoOrientables.py  
&nbsp;&nbsp;&nbsp;&nbsp;✔️ En el notebook donde se va a trabajar debes permitir que pueda montar el drive, luego se ejecuta estas lineas:  
&nbsp;&nbsp;&nbsp;&nbsp;Get[  
&nbsp;&nbsp;&nbsp;&nbsp;import sys  
&nbsp;&nbsp;&nbsp;&nbsp;ruta_carpeta = '/content/drive/MyDrive/ArchivosPy'  
&nbsp;&nbsp;&nbsp;&nbsp;if ruta_carpeta not in sys.path:  
&nbsp;&nbsp;&nbsp;&nbsp;sys.path.append(ruta_carpeta)  
&nbsp;&nbsp;&nbsp;&nbsp;]  
✔️ Finalmente se importa el archivo ejecutando esta línea: **from SuperficiesNoOrientable import Construccion, Nurbs_NonOrientPy_graph**
