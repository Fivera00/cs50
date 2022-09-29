let retos = [];

$(document).ready(function () {
  load_question();
  // Click en las cartas normales
});

$(".element-card").on("click", function () {
  if ($(this).hasClass("open")) {
    $(this).removeClass("open");
  } else {
    $(".element-card").removeClass("open");
    $(this).addClass("open");
    getRandomChallenge();
  }
});

// Click en el maso de cartas
$(".element-card-r").on("click", function () {
  if ($(this).hasClass("open")) {
    $(this).removeClass("open");
  } else {
    $(".element-card-r").removeClass("open");
    $(this).addClass("open");
    getRandomChallenge();
  }
});

// Click en el boton de enviar registarJuego
// $("#registrarJuego").on("click", function () {
//   send_game();
//   // alert("hola");
// });

function getRandomChallenge() {
  const random = Math.floor(Math.random() * retos.length);
  $(".reto-game").text(retos[random]["titleChallenge"]);
}

function load_question() {
  // fetch(`/api/game/${game}/category/${category}/challenge`)
  fetch(`/api/challenges`)
    .then((response) => response.json())
    .then((data) => {
      retos = data;
    });
}

// sending game method post to the server
async function send_game() {
  let game = document.querySelector("#gameRegistrar").value;

  let response = await fetch("/insertgames", {
    method: "POST",
    body: JSON.stringify({
      game: game,
    }),
  }).then((response) => {
    if (response.ok) {
      window.location.href = "/";
    }
  });
}

function delete_game() {
  // get value from the button with id is deleteButton
  let id = document.querySelector("#deleteButton").value;
  // delete the game with the id
  fetch(`/deletegames/${id}`, {
    method: "DELETE",
  }).then((response) => {
    console.log("Respuesta", response);
    if (response.ok) {
      window.location.href = "/categories/1";
    } else {
      alert("No se ha podido eliminar el juego");
    }
  });
}

function update_game() {
  // get value from the button with id is updateButton
  let id = document.querySelector("#updateButton").value;
  let game = document.querySelector("#gameUpdate").value;
  // update the game with the id
  fetch(`/updategames/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      game: game,
    }),
  }).then((response) => {
    if (response.ok) {
      window.location.href = "/";
    } else {
      alert("No se ha podido actualizar el juego");
    }
  });
}
