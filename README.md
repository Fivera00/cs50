# cs50

### Especificación

Complete la implementación de su sitio de subastas. Debes cumplir con los siguientes requisitos:

- Modelos : su aplicación debe tener al menos tres modelos además del Usermodelo: uno para los listados de subastas, otro para las ofertas y otro para los comentarios realizados en los listados de subastas. Depende de usted decidir qué campos debe tener cada modelo y cuáles deben ser los tipos de esos campos. Puede tener modelos adicionales si lo desea.
- Crear listado : los usuarios deben poder visitar una página para crear un nuevo listado. Deben poder especificar un título para la lista, una descripción basada en texto y cuál debe ser la oferta inicial. Los usuarios también deberían poder proporcionar opcionalmente una URL para una imagen para el listado y / o una categoría (por ejemplo, moda, juguetes, electrónica, hogar, etc.).
- Página de listados activos : la ruta predeterminada de su aplicación web debe permitir a los usuarios ver todos los listados de subastas actualmente activos. Para cada listado activo, esta página debe mostrar (como mínimo) el título, la descripción, el precio actual y la foto (si existe uno para el listado).
- Página de listado : al hacer clic en un listado, los usuarios deben ir a una página específica para ese listado. En esa página, los usuarios deberían poder ver todos los detalles sobre la lista, incluido el precio actual de la lista.
  _ Si el usuario ha iniciado sesión, el usuario debería poder agregar el elemento a su "Lista de seguimiento". Si el artículo ya está en la lista de seguimiento, el usuario debería poder eliminarlo.
  _ Si el usuario ha iniciado sesión, el usuario debería poder pujar por el artículo. La oferta debe ser al menos tan grande como la oferta inicial y debe ser mayor que cualquier otra oferta que se haya realizado (si corresponde). Si la oferta no cumple con esos criterios, se debe presentar un error al usuario.
  _ Si el usuario ha iniciado sesión y es quien creó la lista, el usuario debe tener la capacidad de "cerrar" la subasta desde esta página, lo que convierte al mejor postor en el ganador de la subasta y hace que la lista ya no esté activa.
  _ Si un usuario inició sesión en una página de listado cerrada y el usuario ganó esa subasta, la página debería decirlo.
  Los usuarios que hayan iniciado sesión deberían poder agregar comentarios a la página de la lista. La página de la lista debe mostrar todos los comentarios que se han hecho en la lista.
- Lista de seguimiento : los usuarios que hayan iniciado sesión deberían poder visitar una página de Lista de seguimiento, que debería mostrar todos los listados que un usuario ha agregado a su lista de seguimiento. Hacer clic en cualquiera de esos listados debería llevar al usuario a la página de ese listado.
- Categorías : los usuarios deben poder visitar una página que muestre una lista de todas las categorías de la lista. Hacer clic en el nombre de cualquier categoría debería llevar al usuario a una página que muestra todos los listados activos en esa categoría.
- Interfaz de administración de Django : a través de la interfaz de administración de Django, un administrador del sitio debería poder ver, agregar, editar y eliminar cualquier listado, comentario y oferta realizada en el sitio.

https://www.sony.com.ec/image/b789488955522f13ffb4778bd08465c6?fmt=pjpeg&wid=330&bgcolor=FFFFFF&bgc=FFFFFF
