document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll(".post").forEach((element) => {
        send_Post(element)
    })
    document.querySelectorAll("#like").forEach((element) => {
        element.onclick = function (){
            likeDislike(element)
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
            modal_body.innerHTML = `<textarea class="post-content form-control"></textarea>`
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
                        window.location.href =  window.location.href
                        // if( result.status === 201){
                            

                        // }else{
                        //     console.log("no pude recargar")
                        // }

                    });
            })

        })
    }

    // const content = element.querySelector(`#post-text`).value
    // const modal = document.querySelector(".post-modal")
    // console.log(content)


}

function likeDislike(element) {
    post_id = parseInt(element.value)

    console.log(post_id)
    fetch(`like/${post_id}`)
        .then(response => response.json())
        .then(data => {
            element = element.querySelector(".fa-heart")

            id = `#numLikes_${post_id}`

            if (data.liked) {
                element.className = 'fas fa-heart fa-2x'
                element.style.color = "red";

            }else{
                element.className = 'far fa-heart fa-2x'
                element.style.color = "black";
            }
            document.querySelector(id).innerHTML = data.num_likes + " like(s)"

        })
}

function edit_Post(element) {
    const post_id = parseInt(element.value)
    const saveButton = document.querySelector(`#send-edit-post`)
    let modalBody = document.querySelector(`.edit`)
    //document.querySelector(`#txt-edit`).value = ""
    fetch(`post/${post_id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            modalBody.innerHTML = `<input class= "form-control" id="new-content" value="${data.content}">`;
            // document.querySelector(`#txt-edit`).value = data.content   
            document.querySelector(`#postId-edit`).value = data.content
        })

}

function sendEditPost() {
    let _content = document.querySelector('#postId-edit').value
    fetch(`editpost`, {
        method: 'POST',
        body: JSON.stringify({
            content: _content
        })

    })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
        });
}