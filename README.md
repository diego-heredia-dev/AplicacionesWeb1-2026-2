Cuando escribo en chrome http://34.228.115.207:8000/ falla  
Creo que es porque el ec2 no tiene abierto el puerto 8000 para afuera del servidor
Por eso solo funciona cuando llamamos al puerto 8000 dentro del servidor EC2: http://127.0.0.1:8000/

¿qué copia exactamente COPY . /site/ y qué pasaría si tuvieras un .pem en el directorio? El Dockerfile declara EXPOSE 5001 pero la aplicación escucha en el 8000: ¿cuál de los dos manda?
Copia todo lo que esta en el directorio actual a al directiorio /site dentro del contenedor incluyendo el .pem
El que manda es el codigo.