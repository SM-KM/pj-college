import pandas as pd
import random
from datetime import datetime, timedelta

# Define possible values for each column
gravedad = ['Alta', 'Media', 'Baja']
modalidad = ['Hurto', 'Vandalismo', 'Secuestro', 'Robo de identidad', 'Ciberacoso',
             'Asalto con violencia', 'Fraude electrónico', 'Hurto menor', 'Extorsión',
             'Robo de vehículos', 'Acoso verbal', 'Tráfico de drogas', 'Fraude bancario',
             'Daños a la propiedad', 'Homicidio', 'Estafa', 'Contrabando', 'Violencia doméstica']
motivacion = ['Financiera', 'Oportunidad', 'Protesta', 'Rescate', 'Fraude', 'Económica',
              'Personal', 'Rencor', 'Criminal']
areas_geograficas = ['Ciudad de México', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana',
                     'Mérida', 'León', 'Querétaro', 'Durango', 'Veracruz', 'Chihuahua', 
                     'Hermosillo', 'Saltillo', 'La Paz', 'Aguascalientes', 'Torreón', 
                     'Mexicali', 'Toluca', 'Reynosa', 'Zacatecas']
crimenes_graves = [random.randint(0, 10000) for _ in range(1000)]
crimenes_menores = [random.randint(0, 10000) for _ in range(1000)]
crimenes_violentos = ['Homicidio', 'Asalto', 'Secuestro', 'Violación', 'Extorsión']
crimenes_no_violentos = ['Hurto', 'Fraude', 'Robo menor', 'Estafa']
crimenes_motivacion_economica = ['Fraude bancario', 'Contrabando', 'Lavado de dinero']
crimenes_odio = ['Racismo', 'Xenofobia', 'Homofobia']
crimenes_pasion_venganza = ['Celos', 'Rencor', 'Despecho']
crimenes_urbanos = ['Robo', 'Vandalismo', 'Asalto']
crimenes_rurales = ['Caza ilegal', 'Robo de ganado', 'Tráfico de especies']
naturaleza = ['Financiera', 'Oportunidad', 'Criminal', 'Fraude']
temporalidad = [(datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(1000)]
involucramiento_tecnologico = ['Bajo', 'Alto', 'Ninguno']
estado_caso = ['Resuelto', 'No resuelto']
crimenes_contra_personas = [random.randint(0, 100) for _ in range(1000)]
crimenes_contra_propiedad = [random.randint(0, 100) for _ in range(1000)]
crimenes_sexuales = [random.randint(0, 100) for _ in range(1000)]
crimenes_economicos = [random.randint(0, 100) for _ in range(1000)]
crimenes_periodo_anual = [random.randint(0, 1000) for _ in range(1000)]
crimenes_hora_dia = [random.randint(0, 24) for _ in range(1000)]
cybercrimenes = [random.randint(0, 1) for _ in range(1000)]
crimenes_tradicionales = [random.randint(0, 1) for _ in range(1000)]
casos_resueltos = [random.randint(0, 100) for _ in range(1000)]
casos_no_resueltos = [random.randint(0, 100) for _ in range(1000)]

# Create a DataFrame
data = {
    'Gravedad': [random.choice(gravedad) for _ in range(1000)],
    'Modalidad': [random.choice(modalidad) for _ in range(1000)],
    'Motivación': [random.choice(motivacion) for _ in range(1000)],
    'Área Geográfica': [random.choice(areas_geograficas) for _ in range(1000)],
    'Crímenes Graves': crimenes_graves,
    'Crímenes Menores': crimenes_menores,
    'Crímenes Violentos': [random.choice(crimenes_violentos) for _ in range(1000)],
    'Crímenes No Violentos': [random.choice(crimenes_no_violentos) for _ in range(1000)],
    'Crímenes Motivación Económica': [random.choice(crimenes_motivacion_economica) for _ in range(1000)],
    'Crímenes de Odio': [random.choice(crimenes_odio) for _ in range(1000)],
    'Crímenes de Pasión/Venganza': [random.choice(crimenes_pasion_venganza) for _ in range(1000)],
    'Crímenes Urbanos': [random.choice(crimenes_urbanos) for _ in range(1000)],
    'Crímenes Rurales': [random.choice(crimenes_rurales) for _ in range(1000)],
    'Naturaleza': [random.choice(naturaleza) for _ in range(1000)],
    'Temporalidad': temporalidad,
    'Involucramiento Tecnológico': [random.choice(involucramiento_tecnologico) for _ in range(1000)],
    'Estado del Caso': [random.choice(estado_caso) for _ in range(1000)],
    'Crímenes contra Personas': crimenes_contra_personas,
    'Crímenes contra Propiedad': crimenes_contra_propiedad,
    'Crímenes Sexuales': crimenes_sexuales,
    'Crímenes Económicos': crimenes_economicos,
    'Crímenes Periodo Anual': crimenes_periodo_anual,
    'Crímenes Hora Día': crimenes_hora_dia,
    'Cibercrímenes': cybercrimenes,
    'Crímenes Tradicionales': crimenes_tradicionales,
    'Casos Resueltos': casos_resueltos,
    'Casos no resueltos': casos_no_resueltos,
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
file_path = 'extra_data.csv'
df.to_csv(file_path, index=False)
