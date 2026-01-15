#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import copy
import plotly.graph_objects as go


# In[ ]:


class Bases_curves:
    def __init__(self, t=None):
        if t is None:
            t = [0, 1, 2, 3, 4]
        self.t = t

    def N_0(self, i, u):
        if i <= len(self.t) - 2:
            return (lambda u_val: 1 if ((u_val >= self.t[i]) & (u_val < self.t[i + 1])) else 0)(u)
        else:
            return 'El índice ha sobrepasado los límites'

    def N_p(self, i, u, p):
        if (p <= len(self.t) - 2) & (i <= len(self.t) - p - 2):
            if p == 0:
                return self.N_0(i, u)
            else:
                return ((lambda u_val: ((u_val - self.t[i]) / (self.t[i + p] - self.t[i]) * self.N_p(i, u, p - 1) 
                        if self.t[i + p] - self.t[i] != 0 else 0))(u) + 
                        (lambda u_val: ((self.t[i + p + 1] - u_val) / (self.t[i + p + 1] - self.t[i + 1]) * self.N_p(i + 1, u, p - 1) 
                        if self.t[i + p + 1] - self.t[i + 1] != 0 else 0))(u))
        else:
            return f'Ingrese valores de i=[0, {len(self.t) - p - 2}] y p=[0, {len(self.t) - 2}]'


# In[ ]:


class Nurbs_curbs():
    def __init__(self):
        pass

    def curva(self, pts, pes, nod, p, u):
        suma_den, suma_num = 0, [0 for k in range(len(pts[0]))]
        for i in range(len(pes)):
            suma_den = suma_den + (lambda i_val: (pes[i_val]*Bases_curves(nod).N_p(i=i_val, u=u, p=p)))(i)

            suma_num = [a + b for a,b in zip(suma_num, (lambda i_val: ([
                pes[i_val]*Bases_curves(nod).N_p(i=i_val, u=u, p=p)*psdr for psdr in pts[i_val]]))(i)) ]

        return [psdr/suma_den for psdr in suma_num]

    def curva1(self, pts, pes, nod, p, u):
        if isinstance(u, (int, float)):  
            instancia = self.curva(pts, pes, nod, p, u)
            return instancia
        elif isinstance(u, (list, np.ndarray)):  
            instancias = [self.curva(pts, pes, nod, p, num) for num in u]
            return instancias
        else:
            raise ValueError("La entrada debe ser un número o un array de NumPy.")


# In[ ]:


class Construccion():
    def __init__(self, n, r):
        self.n, self.r = n, r

    def polygon(self):
        θ = 2*np.pi/self.n
        α = np.pi*(self.n-2)/(2*self.n)
        R = self.r/np.sin(α)
        Tabla, Lista=[[[self.r*np.cos(θ*k),self.r*np.sin(θ*k)],[R*np.cos(θ*(2*k+1)/2),R*np.sin(θ*(2*k+1)/2)]] for k in range(self.n)], []
        for cont in range(len(Tabla)):
            Lista.extend([Tabla[cont][0], Tabla[cont][1]])
        Lista.append(Tabla[0][0])
        return Lista

    def peso(self):
        θ = 2*np.pi/self.n
        Tabla, Lista = [[1, np.cos(θ/2)] for k in range(self.n)], []
        for cont in range(len(Tabla)):
            Lista.extend(Tabla[cont])
        Lista.append(Tabla[0][0])
        return Lista

    def open1(self):
        Tabla, Lista = [[k,k] for k in range(self.n+1)], []
        for cont in range(len(Tabla)):
            Lista.extend(Tabla[cont])
        Lista = [0] + Lista + [self.n]
        return Lista


# In[ ]:


class Nurbs_surface():
    def __init__(self, pts1, pts2, pts3, direction, pes1, pes2, nod1, nod2, p1, p2):
        self.pts1, self.pts2, self.pts3, self.pes1, self.pes2, self.nod1, self.nod2, self.p1, self.p2 = pts1, pts2, pts3, pes1, pes2, nod1, nod2, p1, p2
        self.direction = direction
        self.objeto1, self.objeto2 = Bases_curves(t=self.nod1), Bases_curves(t=self.nod2)

    def W_ij(self, i, j):
        w_ij = lambda i_val, j_val: (self.pes1[i_val]*self.pes2[j_val] if (i_val < len(self.pes1) and j_val < len(self.pes2))
                                       else 'índices sobrepasaron límites')
        return w_ij(i, j)

    def P_ij(self, i, j):
        p_ij = lambda i_val, j_val: ([self.direction[i_val][0]+self.pts2[j_val][0]*self.pts1[i_val][0]*self.pts3[i_val][0]-self.pts2[j_val][2]*self.pts1[i_val][0]*self.pts3[i_val][2],
                                      self.direction[i_val][1]+self.pts2[j_val][0]*self.pts1[i_val][1]*self.pts3[i_val][0]-self.pts2[j_val][2]*self.pts1[i_val][1]*self.pts3[i_val][2],
                                      self.pts2[j_val][0]*self.pts3[i_val][2]+self.pts2[j_val][2]*self.pts3[i_val][0]] 
                                     if (i_val < len(self.pts1) and j_val < len(self.pts2)) else 'índices sobrepasaron límites')
        return p_ij(i,j)

    def superficie(self, u, v):
        suma_den, suma_num = 0, [0 for k in range(len(self.pts1[0]))]
        for i1 in range(len(self.pes1)):
            for j1 in range(len(self.pes2)):
                suma_den = suma_den + (lambda i_val, j_val: (
                    self.objeto1.N_p(i=i_val, u=u, p=self.p1)*self.objeto2.N_p(i=j_val, u=v, p=self.p2)*self.W_ij(i_val, j_val)))(i1, j1)

                suma_num = [a + b for a,b in zip(suma_num, (lambda i_val, j_val: ([
                    self.objeto1.N_p(i=i_val, u=u, p=self.p1)*self.objeto2.N_p(i=j_val, u=v, p=self.p2)*self.W_ij(i_val, j_val)*psdr
                    for psdr in self.P_ij(i_val, j_val)]))(i1,j1)) ]
        return [psdr/suma_den for psdr in suma_num]

    def procesar(self, u, v):
        if (isinstance(u, (int, float))) & (isinstance(v, (int, float))):
            instancia = self.superficie(u, v)
            return instancia
        elif (isinstance(u, (np.ndarray))) & (isinstance(v, (np.ndarray))):
            if u.shape != v.shape:
                return 'Ingrese vectores con mismas dimensiones'
            else:
                fila, columna = u.shape
                lista_alm = [[] for k in range( len(self.superficie(u[0][0], v[0][0]))  )]
                for i in range(fila):
                    for j in range(columna):
                        B = self.superficie(u[i][j], v[i][j])
                        for k in range(len(B)):
                            lista_alm[k].append(B[k])
                C = [np.array(psdr).reshape(fila, columna) for psdr in lista_alm]
                return C
        else:
            raise ValueError("La entrada debe ser un número o un array de NumPy.")


# In[ ]:


class Nurbs_NonOrientPy_graph:
    def __init__(self, pts1, pts2, pts3, direction, pes1, pes2, nod1, nod2, p1, p2, ranu, ranv):
        self.pts1, self.pts2, self.pts3, self.pes1, self.pes2, self.nod1, self.nod2, self.p1, self.p2 = pts1, pts2, pts3, pes1, pes2, nod1, nod2, p1, p2
        self.direction = direction
        self.u = np.linspace(ranu[0], ranu[1]-10**(-10), 50)
        self.v = np.linspace(ranv[0], ranv[1]-10**(-10), 50)
        self.U, self.V = np.meshgrid(self.u, self.v)
        self.objeto = Nurbs_surface(self.pts1, self.pts2, self.pts3, self.direction, self.pes1, self.pes2, self.nod1, self.nod2, self.p1, self.p2)
        self.objeto1 = Nurbs_curbs()

    def grafica(self, pdir=True, pgen=True, c_pdir= True, c_pgen=True, enmaller=True, pts_ctrl=True, superficie=True):
        if superficie is True:    #datos para la superficie
            my_surface = self.objeto.procesar(u=self.U, v=self.V)
            X = my_surface[0]
            Y = my_surface[1]
            Z = my_surface[2]

        if enmaller is True:     #datos para el enmallado
            Data = []
            for i in range(len(self.pts1)):
                l_dat = []
                for j in range(len(self.pts2)):
                    l_dat.append(self.objeto.P_ij(i, j))      #data_ctrlpts(i, j, pgen1=pgen, pdir1=pdir)
                Data.append(l_dat)
            Data = np.array(Data)

        def funci(lista):
            mi_lista = [[] for k in range(len(lista[0]))]
            for i in range(len(mi_lista)):
                mi_lista[i].append(np.array([k[i] for k in lista]))
            mi_lista = np.concatenate(np.array(mi_lista), axis=0)
            return mi_lista

        def funci1(matrix):
            columna = matrix.shape[1]
            lista_alm1 = [[] for k in range(columna)]
            for i in range(len(lista_alm1)):
                lista_alm1[i].append(matrix[: ,i])
            lista_alm1 = np.concatenate(np.array(lista_alm1), axis=0)
            return lista_alm1

        def grafica_maller(matrix):
            mi_lista1 = funci1(matrix)
            mi_lista2 = []
            for i in range(len(mi_lista1)):
                mi_lista2.append(funci(mi_lista1[i]))
            return mi_lista2

        if pts_ctrl is True:    #para puntos de control
            mi_puntos = funci(np.concatenate(Data, axis=0))

        if pdir is True:    #datos para puntos de curvas directriz y generatriz
            x_pdir = np.array([k[0] for k in self.direction]) #pts1
            y_pdir = np.array([k[1] for k in self.direction])
            z_pdir = np.array([k[2] for k in self.direction])
        if pgen is True:  
            x_pgen = np.array([k[0] for k in self.pts2])
            y_pgen = np.array([k[1] for k in self.pts2])
            z_pgen = np.array([k[2] for k in self.pts2])

        if c_pdir is True:   #para las curvas directriz y generatriz
            C_c1 = self.objeto1.curva1(pts=self.direction, pes=self.pes1, nod=self.nod1, p=self.p1, u=self.u)
            my_c1 = funci(C_c1)
        if c_pgen is True:
            C_c2 = self.objeto1.curva1(pts=self.pts2, pes=self.pes2, nod=self.nod2, p=self.p2, u=self.v)
            my_c2 = funci(C_c2)

        fig = go.Figure()
        if pdir is True:
            fig.add_trace(go.Scatter3d(x=x_pdir, y=y_pdir, z=z_pdir, mode='lines', line=dict(color='black',width=6), showlegend=False))
        if pgen is True:
            fig.add_trace(go.Scatter3d(x=x_pgen, y=y_pgen, z=z_pgen, mode='lines', line=dict(color='black',width=6), showlegend=False))
        if c_pdir is True:
            fig.add_trace(go.Scatter3d(x=my_c1[0], y=my_c1[1], z=my_c1[2], mode='lines', line=dict(color='#FFD700',width=8), showlegend=False))
        if c_pgen is True:
            fig.add_trace(go.Scatter3d(x=my_c2[0], y=my_c2[1], z=my_c2[2], mode='lines', line=dict(color='#FFD700',width=8), showlegend=False))


        if enmaller is True:
            lista_graf = grafica_maller(Data)
            lista_graf1 = []
            for i in range(Data.shape[0]):
                lista_graf1.append(funci(Data[i, :]))
            for i in range(len(lista_graf)):
                fig.add_trace(go.Scatter3d(x=lista_graf[i][0], y=lista_graf[i][1], z=lista_graf[i][2], mode='lines', line=dict(color='blue'), showlegend=False))
            for i in range(len(lista_graf1)):
                fig.add_trace(go.Scatter3d(x=lista_graf1[i][0], y=lista_graf1[i][1], z=lista_graf1[i][2], mode='lines', line=dict(color='blue'), showlegend=False))
        if pts_ctrl is True:
            fig.add_trace(go.Scatter3d(x=mi_puntos[0], y=mi_puntos[1], z=mi_puntos[2], mode='markers', marker=dict(color='orange',size=5), showlegend=False))
        if superficie is True:
            fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='viridis', showscale=False, opacity=1,
                                            contours=dict(
                                            x=dict(show=False, color="black"),  # Líneas en X
                                            y=dict(show=False, color="black"),  # Líneas en Y
                                            z=dict(show=False, color="black"),  # Líneas en Z  
                                            )  ))

            #lines = []
            for i in range(X.shape[0]):
                fig.add_trace(go.Scatter3d(x=X[i], y=Y[i], z=Z[i],
                                          mode='lines',
                                          line=dict(color='black', width=1),
                                          showlegend=False))
            for j in range(X.shape[1]):
                fig.add_trace(go.Scatter3d(x=X[:,j], y=Y[:,j], z=Z[:,j],
                                          mode='lines',
                                          line=dict(color='black', width=1),
                                          showlegend=False))

        fig.update_layout(
            scene=dict(
                xaxis=dict(showbackground=False, showgrid=False, showline=False, visible=False),
                yaxis=dict(showbackground=False, showgrid=False, showline=False, visible=False),
                zaxis=dict(showbackground=False, showgrid=False, showline=False, visible=False),
                aspectmode='data',
            ),
            width=800,
            height=800
        )
        return fig 


# In[ ]:



