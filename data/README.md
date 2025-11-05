# Directorio de Datos

Este directorio contiene los datasets utilizados para entrenar los modelos de Machine Learning.

## Estructura

```
data/
├── raw/                    # Datos originales sin procesar
│   └── datos_retail_para_modelos.csv  # Dataset principal
└── processed/              # Datos procesados para entrenamiento
```

## Dataset Principal: datos_retail_para_modelos.csv

### Ubicación
Coloca tu archivo `datos_retail_para_modelos.csv` en el directorio `data/raw/`.

### Estructura del Dataset

El dataset debe contener las siguientes columnas:

| Columna | Descripción | Tipo | Ejemplo |
|---------|-------------|------|---------|
| `consumo_energia` | Consumo de energía en kWh | float | 53.2397 |
| `pies_cuadrados` | Área del edificio en pies cuadrados | float | 9045 |
| `ano_construccion` | Año de construcción del edificio | float | 2016.0 |
| `temperatura_aire` | Temperatura del aire en °C | float | 25.0 |
| `cobertura_nubes` | Cobertura de nubes (0-10) | float | 6.0 |
| `presion_nivel_mar` | Presión atmosférica a nivel del mar en hPa | float | 1019.7 |
| `velocidad_viento` | Velocidad del viento en m/s | float | 0.0 |
| `mes` | Mes del año (1-12) | int | 1 |
| `dia_del_ano` | Día del año (1-365) | int | 1 |
| `dia_de_la_semana` | Día de la semana (0-6, donde 0=Lunes) | int | 4 |
| `hora_del_dia` | Hora del día (0-23) | int | 0 |
| `es_fin_de_semana` | Indicador de fin de semana | bool | True |
| `medidor_electricidad` | Tipo de medidor de electricidad | bool | True |
| `medidor_agua_fria` | Tipo de medidor de agua fría | bool | False |

### Ejemplo de Primeras Filas

```csv
consumo_energia,pies_cuadrados,ano_construccion,temperatura_aire,cobertura_nubes,presion_nivel_mar,velocidad_viento,mes,dia_del_ano,dia_de_la_semana,hora_del_dia,es_fin_de_semana,medidor_electricidad,medidor_agua_fria
0.0,59071,1980.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
0.0,283,1985.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
0.0,15304,2016.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
53.2397,9045,2016.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
0.0,31666,2008.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
```

## Notas Importantes

1. **Formato**: El archivo debe estar en formato CSV con separador de coma (`,`)
2. **Encoding**: UTF-8
3. **Encabezados**: La primera fila debe contener los nombres de las columnas
4. **Valores Nulos**: Se recomienda mínimo de valores nulos; el sistema puede manejarlos pero afecta la calidad
5. **Tamaño**: No hay límite de tamaño, pero se recomienda al menos 1000 registros para un buen entrenamiento

## ¿Cómo Obtener el Dataset?

Si no tienes el archivo `datos_retail_para_modelos.csv`, contacta al administrador del proyecto o consulta la documentación de recopilación de datos.

## Seguridad

⚠️ **IMPORTANTE**: No subas datos sensibles o confidenciales al repositorio Git. Este directorio está excluido en `.gitignore` para proteger los datos.
