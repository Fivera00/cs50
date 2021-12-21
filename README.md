# cs50
### Especificación 
Usando Python, JavaScript, HTML y CSS, complete la implementación de una red social que permite a los usuarios hacer publicaciones, seguir a otros usuarios y dar "me gusta" a las publicaciones. Debes cumplir con los siguientes requisitos:
* Publicación Nueva: los usuarios que hayan iniciado sesión deberían poder escribir una publicación nueva basada en texto completando el texto en un área de texto y luego haciendo clic en un botón para enviar la publicación.
* Todas las publicaciones: el enlace "Todas las publicaciones" en la barra de navegación debe llevar al usuario a una página donde pueda ver todas las publicaciones de todos los usuarios, con las publicaciones más recientes primero.
    * Cada publicación debe incluir el nombre de usuario del autor, el contenido de la publicación en sí, la fecha y hora en que se realizó la publicación y la cantidad de "me gusta" que tiene la publicación
* Página de perfil : hacer clic en un nombre de usuario debería cargar la página de perfil de ese usuario. Esta página debería:
    * Muestra el número de seguidores que tiene el usuario, así como el número de personas que sigue.
    * Muestra todas las publicaciones de ese usuario, en orden cronológico inverso.
    * Para cualquier otro usuario que haya iniciado sesión, esta página también debe mostrar un botón "Seguir" o "Dejar de seguir" que permitirá al usuario actual alternar si está siguiendo o no las publicaciones de este usuario. Tenga en cuenta que esto solo se aplica a cualquier "otro" usuario: un usuario no debería poder seguirse a sí mismo.
* Siguiente : El enlace "Siguiente" en la barra de navegación debe llevar al usuario a una página donde ve todas las publicaciones realizadas por los usuarios que sigue el usuario actual.
    * Esta página debe comportarse como lo hace la página "Todas las publicaciones", solo que con un conjunto más limitado de publicaciones.
    * Esta página solo debería estar disponible para los usuarios que hayan iniciado sesión.
* Paginación : en cualquier página que muestre publicaciones, las publicaciones solo deben mostrarse 10 en una página. Si hay más de diez publicaciones, debería aparecer un botón "Siguiente" para llevar al usuario a la siguiente página de publicaciones (que debería ser más antigua que la página actual de publicaciones). Si no está en la primera página, debería aparecer un botón "Anterior" para llevar al usuario a la página anterior de publicaciones también.
* Editar publicación : los usuarios deben poder hacer clic en un botón o enlace "Editar" en cualquiera de sus propias publicaciones para editar esa publicación.
    * Cuando un usuario hace clic en "Editar" para una de sus propias publicaciones, el contenido de su publicación debe reemplazarse con un lugar textareadonde el usuario puede editar el contenido de su publicación.
    * El usuario debería poder "Guardar" la publicación editada. Con JavaScript, debería poder lograr esto sin tener que volver a cargar toda la página.
    * Por seguridad, asegúrese de que su aplicación esté diseñada de tal manera que no sea posible para un usuario, a través de cualquier ruta, editar las publicaciones de otro usuario.
* "Me gusta" : los usuarios deben poder hacer clic en un botón o enlace en cualquier publicación para alternar si les "gusta" o no.
    * Al usar JavaScript, debe informar de forma asincrónica al servidor que debe actualizar el recuento de Me gusta (como a través de una llamada a fetch) y luego actualizar el recuento de Me gusta de la publicación que se muestra en la página, sin requerir una recarga de toda la página.