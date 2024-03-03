import psutil
import pymysql
import time

# Configuración de la conexión a la base de datos
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Prometeus.0',
    'database': 'test_api'
}

# Función para obtener el número de conexiones activas en la base de datos MySQL
def get_active_connections():
    db = pymysql.connect(**DATABASE_CONFIG)
    cursor = db.cursor()
    cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
    result = cursor.fetchone()
    db.close()
    return int(result[1])

# Función para obtener el uso de memoria del proceso MySQL
def get_mysql_memory_usage():
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
        if proc.info['name'] == "mysqld":
            return proc.info['memory_info'].rss

# Función para obtener la actividad de la CPU del proceso MySQL
def get_mysql_cpu_usage():
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        if proc.info['name'] == "mysqld":
            return proc.info['cpu_percent']

# Función para obtener el uso de CPU del sistema
def get_system_cpu_usage():
    return psutil.cpu_percent()

# Función para obtener el uso de memoria del sistema
def get_system_memory_usage():
    return psutil.virtual_memory().percent

# Función para imprimir las métricas de rendimiento
def print_performance_metrics():
    active_connections = get_active_connections()
    mysql_memory_usage = get_mysql_memory_usage()
    mysql_cpu_usage = get_mysql_cpu_usage()
    system_cpu_usage = get_system_cpu_usage()
    system_memory_usage = get_system_memory_usage()

    print("----------------------------------------")
    print(f"Active Connections: {active_connections}")
    print(f"MySQL Memory Usage: {mysql_memory_usage } MB")
    print(f"MySQL CPU Usage: {mysql_cpu_usage} %")
    print(f"System CPU Usage: {system_cpu_usage} %")
    print(f"System Memory Usage: {system_memory_usage} %")

# Bucle principal para recopilar y mostrar métricas de rendimiento cada 5 segundos
while True:
    print_performance_metrics()
    time.sleep(5)
