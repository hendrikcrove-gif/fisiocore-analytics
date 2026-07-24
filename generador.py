import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime, timedelta

fake = Faker('es_MX')

# 1. ESPECIFICA TU CARPETA AQUÍ (Ej. 'C:/Users/TuUsuario/Desktop/Proyecto Clinica')
# Recuerda usar barras diagonales normales (/)
ruta_carpeta = '' 

# Parámetros de la clínica
num_pacientes = 100
diagnosticos = [
    'Lumbalgia Mecánica',
    'Esguince Cervical Grado II',
    'Rehabilitación de Miocardio',
    'Tendinopatía del Manguito Rotador',
    'Fascitis Plantar',
    'Postoperatorio LCA'
]
estados_cita = ['Atendido', 'Cancelado', 'No Show', 'Reprogramado']

datos_clinica = []

for _ in range(num_pacientes):
    fecha_cita = fake.date_between(start_date='-3m', end_date='today')
    
    paciente = {
        'ID_Paciente': fake.unique.random_number(digits=5),
        'Nombre_Completo': fake.name(),
        'Telefono': fake.phone_number(),
        'Edad': random.randint(18, 75),
        'Diagnostico': random.choice(diagnosticos),
        'Fecha_Cita': fecha_cita,
        'Costo_Sesion': random.choice([25.00, 30.00, 45.00]),
        'Estado_Cita': random.choices(estados_cita, weights=[60, 15, 15, 10], k=1)[0]
    }
    datos_clinica.append(paciente)

df_pacientes = pd.DataFrame(datos_clinica)

# 2. Armamos la ruta y guardamos
nombre_archivo = 'base_datos_clinica.csv'
ruta_completa = os.path.join(ruta_carpeta, nombre_archivo) if ruta_carpeta else nombre_archivo

df_pacientes.to_csv(ruta_completa, index=False, encoding='utf-8')

# 3. El rastreador infalible
print("\n¡Base de datos generada con éxito!")
print("El archivo se guardó EXACTAMENTE en esta ruta:")
print(os.path.abspath(ruta_completa))