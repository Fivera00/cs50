document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll(".post").forEach((element) => {
        send_Post(element)
    })

    document.querySelectorAll("#like").forEach((element) => {
        element.onclick = function (){
            likeDislike(element)
        }
    })

    document.querySelectorAll(".edit").forEach((element) => {
        edit_Post(element)
    })

    document.querySelectorAll("#follow").forEach((element) => {
        element.onclick = function (){
            followUnfollow(element)
        }
        
    })
})



function send_Post(element) {
    let modal = element.querySelector(".post-modal")

    if (modal !== null) {
        $(modal).on('show.bs.modal', () => {
            const modal_body = element.querySelector(".modal-body")
            const modal_title = element.querySelector(".modal-title")
            const modal_button = element.querySelector(".btn-modal-send")
            const placeholder_text = element.querySelector("#open-post-modal")
            modal_body.innerHTML = `<textarea class="post-content form-control" placeholder="${placeholder_text.value}"></textarea>`
            modal_title.innerHTML = "Send Post"

            modal_button.addEventListener("click", () => {
                const content_post = modal_body.querySelector(".post-content").value
                console.log(content_post)

                $(modal).modal('hide');
                fetch('/post', {
                    method: 'POST',
                    body: JSON.stringify({
                        content_post: content_post
                    })
                })
                    .then(response => response.json())
                    .then(result => {
                        // Print result
                        console.log(result);
                        window.location.href = window.location.href
                        // if( result.status === 201){


                        // }else{
                        //     console.log("no pude recargar")
                        // }

                    });
            })

        })
    }

}

function likeDislike(element) {
    post_id = parseInt(element.value)

    console.log(post_id)
    fetch(`/like/${post_id}`,{
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            element = element.querySelector(".fa-heart")

            id = `#numLikes_${post_id}`

            if (data.liked) {
                element.className = 'fas fa-heart fa-2x'
                element.style.color = "red";

            } else {
                element.className = 'far fa-heart fa-2x'
                element.style.color = "black";
            }
            document.querySelector(id).innerHTML = data.num_likes + " likes"
            
        })
}

function edit_Post(element) {
    let modal = element.querySelector(".edit-modal")

    if (modal !== null) {
        $(modal).on('show.bs.modal', () => {
            // seccion del modal
            const modal_body = element.querySelector(".modal-body")
            const modal_title = element.querySelector(".modal-title")
            const modal_button = element.querySelector(".btn-modal-send")

            // enviamos el texto a editar al modal 
            const text = element.querySelector(".text-content-post")
            const edit_text = text.textContent.trim()
            modal_body.innerHTML = `<textarea class="post-content form-control">${edit_text}</textarea>`
            modal_title.innerHTML = "Edit Post"

            // 
            modal_button.addEventListener("click", () => {
                const content_modified = modal_body.querySelector(".post-content").value.trim()
                post_id = modal_button.value
                console.log(content_modified, post_id)

                $(modal).modal('hide');
                fetch('/post', {
                    method: 'PUT',
                    body: JSON.stringify({
                        post_id: post_id,
                        content_modified: content_modified
                    })
                })
                    .then(response => response.json())
                    .then(result => {
                        // Print result
                        console.log(result);
                        // window.location.href = window.location.href
                        if( result.status === 201){
                            const card_post = document.getElementById(`post-content-${post_id}`)
                            card_post.innerHTML = content_modified



                        }else{
                            console.log("no pude recargar")
                        }

                    });
    
            })

        })
    }
}

function followUnfollow(element){
    profile_id = parseInt(element.value)
    user = document.getElementById("user-profile").value
    fetch(`/follow/${profile_id}`,{
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {

            id = `#profile-followers-${profile_id}`

            if (data.follow) {
                element.innerHTML = 'Following'
                element.className = 'btn btn-outline-primary btn-sm col-lg-8'
                document.querySelector(".list-group").innerHTML = `<li class="list-group-item text-center">${user}</li>`

            } else {
                element.innerHTML = 'Follow'
                element.className = 'btn btn-primary btn-sm col-lg-8'
                document.querySelector(".list-group").innerHTML = ``
            }
            document.querySelector(id).innerHTML = data.num_followers
        })

}