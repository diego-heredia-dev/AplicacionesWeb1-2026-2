#Gunircon escucha en el puerto 8000 dentro del contenedor, 0.0.0.0 significa que acepta conexiones desde cualquier lugar/dispositivo
bind = '0.0.0.0:8000'
#2 procesos para antender solicitudes
workers = 2
#envia los registros de accesos y errores a la salida estandar
accesslog = '-'
errorlog = '-'
#redirige la salida de la app a los registros de errores
capture_output = True