#%%
import pandas as pd
import seaborn as sns
# %%
"""
Trabajo 2 - Introducción al 
Análisis de Datos con Python

José Enrique García Ramos

"""

"""
Importamos la base de datos que 
vamos a utilizar"""

base =  pd.read_csv("synergy_logistics_database.csv")
base["date"] = pd.to_datetime(base["date"])
base['mes'] = base['date'].dt.strftime('%m')
base['anio'] = base['date'].dt.strftime('%Y')
base.head()



# %%
"""

Opción 1) Rutas de importación y exportación.
¿Ccuáles son esas 10 rutas? 
¿Le conviene implementar esa estrategia? ¿Porqué?

Generamos las 10 rutas con mayor número de servicios
de exportacion considerando cualquier medio de 
transporte
"""

dff = base.groupby(by=['origin','destination'], as_index=False).count()
dff = dff.filter(['origin','destination','register_id'])
dff = dff.set_axis(['origen','destino','total'], axis=1)
dff = dff.sort_values(by='total', ascending=False).head(10)
dff["Origen_Destino"] = dff["origen"]+"-"+dff["destino"]
dff = dff.filter(['Origen_Destino','total'])
#dff = dff.filter([['Origen_Destino','total', 'year'] == 2015])

""" 
Generamos las 10 rutas con mayor
número de servicios de exportación
"""

tipos_transporte=base['transport_mode'].unique()
"""
Obtenemos las exportaciones considerando solamente
un medio de transporte
"""
exportunmod=base.groupby(['direction','origin','destination','transport_mode']).count().sort_values('register_id',ascending=False )['register_id'].head(10)
"""
Generamos las 10 rutas de comercio más relevantes
a nivel mundial"""
rutas_mundial = pd.DataFrame(exportunmod).reset_index()


#%%
"""
Generamos las importaciones con un sólo medio
de transporte
"""
imports=base.groupby(['direction','destination','origin','transport_mode']).count().sort_values('register_id',ascending=False )['register_id']
imports1 = pd.DataFrame(imports).reset_index()
importunmod = imports1.query('direction == "Imports"').sort_values('register_id',ascending=False ).head(10)



#%%
""""
------------------------------------------
Opción 2) Medio de transporte utilizado.
------------------------------------------

¿Cuáles son los 3 medios de transporte más importantes para Synergy logistics considerando el valor de las importaciones y exportaciones?
¿Cuál es medio de transporte que podrían reducir?

"""

"""
Rutas de ordenadas por ingresos
"""
agrupar=base.groupby(['direction','origin','destination','product','transport_mode']).sum().sort_values('total_value',ascending=False )['total_value']#.head(10)
global_routess = pd.DataFrame(agrupar).reset_index()

"""
Posteriormente ordenamos las rutas obtenidas acumuladas por el tipo de transporte
que utilizan, de esta forma podemos determinar el ingreso que genera
cada uno de ellos y su media.
"""

# Numero de rutas por tipo de transporte
med_obs = base.groupby(['transport_mode']).count()['register_id'].sort_values(ascending=False).to_frame().reset_index()
med_obs_vent = base.groupby(['transport_mode']).sum()['total_value'].sort_values(ascending=False).to_frame().reset_index()
med_obs_prom = base.groupby(['transport_mode']).mean()['total_value'].sort_values(ascending=False).to_frame().reset_index()


"""
Así obtenemos los datos en terminos generales"""

med_obs_vent
med_obs_prom

"""
Posteriormente desglasamos los datos para observarlos de forma 
particular y poder oberservar su tendencia en los últimos años"""

#Ordenamos el número de registros de acuerdo con los servicios realizados
grl_obs = base.groupby(['year','transport_mode']).count()['register_id'].sort_values(ascending=False)
grl_obs1 = pd.DataFrame(grl_obs).reset_index()
grl_obs_vent = base.groupby(['year','transport_mode']).sum()['total_value'].sort_values(ascending=True)
grl_obs_vent1 = pd.DataFrame(grl_obs_vent).reset_index()
grl_obs_prom = base.groupby(['year','transport_mode']).mean()['total_value'].sort_values(ascending=False)
grl_obs_prom1 = pd.DataFrame(grl_obs_prom).reset_index()


""""
Ordenamos el número de registros de acuerdo con los servicios realizados
Consideramos el número de transporte realizados por año desde 2015
Así como los ingresos provocados por estos para poder obtener una conclusión eficiente.
"""
grl_obs_vent1
grl_obs_prom1



# %%

"""
-------------------------------------------
Opción 3) Valor total de importaciones y exportaciones.


¿En qué grupo de países debería enfocar sus esfuerzos?

-------------------------------------------
"""


"""
En primera instancia identificamos y separamos las exportaciones de las
importaciones, obtenemos el número servicio según corresponda.
En segunda instancia obtenemos el número de ingresos consecuencia de
los servicios ya obtenidos, tanto aquellos de tipo exógenos como endógenos.
"""
# Identificamos la Exportaciones(X) e Importaciones (M) 
comerciox = base[(base.direction == "Exports")]
# Servicios
com_x_count = comerciox.groupby(['direction']).count()['register_id']
com_x_sum = comerciox.groupby(['direction']).sum()['total_value']
#Rutas de paises
com_x_p = comerciox.groupby(['origin']).count()['register_id'].sort_values(ascending=False).to_frame().reset_index()
com_x_p["Porcentaje_apoyo"] = round((com_x_p.register_id/com_x_count[0])*100,3)
#Ingresos
com_x_vent = comerciox.groupby(['origin']).sum()['total_value'].sort_values(ascending=False).to_frame().reset_index()
com_x_vent["Porcentaje_apoyo_sales"] = round((com_x_vent.total_value/com_x_sum[0])*100,3)
com_x_vent["Promedio"] = com_x_vent['Porcentaje_apoyo_sales'].cumsum()
#Promedio acumulado
com_x_vent=com_x_vent[com_x_vent['Promedio'] < 81]




#%%
#M
comerciom = base[(base.direction == "Imports")]

# Servicios M
com_m_count = comerciom.groupby(['direction']).count()['register_id']
com_m_sum = comerciom.groupby(['direction']).sum()['total_value']
# Rutas M
com_m_p = comerciom.groupby(['origin']).count()['register_id'].sort_values(ascending=False).to_frame().reset_index()
com_m_p["Porcentaje_apoyo"] = round((com_m_p.register_id/com_m_count[0])*100,3)

# Ingreso M
com_m_vent = comerciom.groupby(['origin']).sum()['total_value'].sort_values(ascending=False).to_frame().reset_index()
com_m_vent["Porcentaje_apoyo_sales"] = round((com_m_vent.total_value/com_m_sum[0])*100,3)
com_m_vent["Promedio"] = com_m_vent['Porcentaje_apoyo_sales'].cumsum()
#  Promedio Acumulado M
prom_acumulado_bol = com_m_vent['Promedio'] < 82
com_m_vent=com_m_vent[prom_acumulado_bol]


"""
Por último, señalamos aquellos paises que por consecuencia de su actividad económica
generan mayor intercambio comercial hacia el interior y el exterior de su territorio, 
en especifico aquellos que generan el 80% del comercio exterior.
"""
# %%
