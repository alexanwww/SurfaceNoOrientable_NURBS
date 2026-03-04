# SurfaceNoOrientable_NURBS

This repository contains the **SuperficieNoOrientable.ipynb** notebook, dedicated to generating control data and visualizing **non-orientable surfaces**. It includes an analysis of verification and error of the generated data for the Möbius strip and Klein bottle. Additional examples are provided to demonstrate that the **generation_data** class is general and can handle any non-orientable surface defined topologically as a curve that is simultaneously rotated and twisted.  

The repository also includes a folder with sample images of these non-orientable surfaces, generated using the classes from the notebook.

##  Classes
| Class | Description |
|-------|-------------|
| **Bases_curves** | Constructs B-Spline basis functions. |
| **Nurbs_curves** | Builds NURBS curves. |
| **Construccion** | Generates weights, knots, and control points for a circle of radius *a*. |
| **Nurbs_surface** | Evaluates the NURBS surface from the control data. |
| **Nurbs_surface3D_graph** | Visualizes NURBS surfaces using the control data. |
| **generation_data** | Core class: constructs control data for non-orientable surfaces. This data can be used with `Nurbs_surface3D_graph` or any other library, such as `geomdl`. |

##  Features
- Modeling of non-orientable surfaces using NURBS.  
- Control over visualization parameters, including mesh display and *u*/*v* ranges for the NURBS surface S(u,v).  
- Real-time 3D rendering powered by Plotly.  
- Verification and error analysis for Möbius strip and Klein bottle.  

##  Installation & Usage
1. Download the **SuperficieNoOrientable.ipynb** file.  
2. Open it in **Jupyter Notebook** or **Google Colab** (mount Google Drive to avoid accidental deletion of local files).  
3. Run the notebook to generate and visualize non-orientable surfaces.  

##  Folder Contents
- `SuperficieNoOrientable.ipynb` – Main notebook.  
- `images/` – Sample images of generated surfaces.
