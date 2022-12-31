const _templateQuestion = `
<div
  class="p-4 w-full max-w-sm bg-white rounded-lg border shadow-lg mb-8 md:mb-4 dark:bg-gray-800 dark:border-gray-700">
  <h5 class="text-base font-semibold text-center text-gray-900 md:text-xl dark:text-white">
    Es hora de jugar!
  </h5>
</div>
<div id="menu-card"
  class="p-4 w-full justify-center hidden md:flex items-center max-w-screen-lg rounded-lg sm:flex-col dark:bg-gray-800 dark:border-gray-700">
  <div class="element-card">
    <div class="front-facing">
    </div>
    <div class="back-facing">
    <p class="name-game"></p>
    <p class="reto-game"></p>
    <p class="cat-game"></p>
    </div>
  </div>
  <div class="element-card">
    <div class="front-facing">
    </div>
    <div class="back-facing">
    <p class="name-game"></p>
    <p class="reto-game"></p>
    <p class="cat-game"></p>
    </div>
  </div>
  <div class="element-card">
    <div class="front-facing">
    </div>
    <div class="back-facing">
    <p class="name-game"></p>
    <p class="reto-game"></p>
    <p class="cat-game"></p>
    </div>
  </div>
  <div class="element-card">
    <div class="front-facing">
    </div>
    <div class="back-facing">
    <p class="name-game"></p>
    <p class="reto-game"></p>
    <p class="cat-game"></p>
    </div>
  </div>
</div>

<div id="menu-card-responsive" class="w-full flex md:hidden justify-center">
  <div class="relative">
    <!-- <div class="w-50 h-80 absolute top-0">
      <div class="absolute translate-x-3 translate-y-3 rounded-2xl shadow-lg border-gray-200">
      </div>
    </div> -->

    <div class="element-card-r1 absolute">
      <div class="front-facing-r1 " style="transform: translate(20px, 15px) rotate(6deg);">
      </div>
      <div class="front-facing-r1" style="transform: translate(12px, 12px) rotate(3deg);">
      </div>
    </div>

    <div class="card-primaria">
      <div class="element-card-r">
        <div class="front-facing-r">
        </div>
        <div class="back-facing-r">
        <p class="name-game"></p>
        <p class="reto-game"></p>
        <p class="cat-game"></p>
        </div>
      </div>
    </div>


  </div>

</div>
`;

document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  let retos = [];
  const _categories = document.querySelectorAll("#btnAJugar");

  document.querySelector("#category").style.display = "flex";
  document.querySelector("#questions").style.display = "none";
});

function loadQuestion(event) {
  document.querySelector("#category").style.display = "none";
  document.querySelector("#questions").style.display = "flex";
  document.querySelector("#questions").innerHTML = _templateQuestion;
  const _idCat = event.value;
  const _idGame = window.location.pathname.split("/").pop();
  fetch(`/api/game/${_idGame}/category/${_idCat}/challenges`)
    .then((response) => response.json())
    .then((data) => {
      retos = data;
      console.log(data);
      document.querySelector("#category").style.display = "none";
      document.querySelector("#questions").style.display = "flex";
      document.querySelector("#questions").innerHTML = _templateQuestion;
      // window.location.href = "/games";
      $(".element-card").on("click", function () {
        if ($(this).hasClass("open")) {
          $(this).removeClass("open");
        } else {
          getRandomChallenge();
          $(".element-card").removeClass("open");
          $(this).addClass("open");
        }
      });

      // Click en el maso de cartas
      $(".element-card-r").on("click", function () {
        if ($(this).hasClass("open")) {
          $(this).removeClass("open");
        } else {
          getRandomChallenge();
          $(".element-card-r").removeClass("open");
          $(this).addClass("open");
        }
      });
    });
}

function send_game() {
  let game = document.querySelector("#gameRegistrar").value;

  fetch("/insertgames", {
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

function deleteGame(event) {
  const id = event.value;
  fetch(`/deletegames/${id}`, {
    method: "DELETE",
  }).then((response) => {
    if (response.ok) {
      window.location.href = "/";
    } else {
      alert("No se ha podido eliminar el juego");
      window.location.href = "/";
    }
  });
  // alert("Se va a eliminar el juego");
}
// sending game method post to the server

function getRandomChallenge() {
  if (retos.length == 0) {
    $(".reto-game").text("No hay retos disponibles");
    return;
  }
  const random = Math.floor(Math.random() * retos.length);
  const nameGame = retos[random]["gameChallenge"]["name"];
  const nameCategory = retos[random]["categoryChallenge"]["categoryName"];
  let nameChallenge = retos[random]["titleChallenge"];
  const isChallenge = retos[random]["isChallenge"];
  const isVerdad = retos[random]["gameChallenge"]["id"];
  if (isVerdad === 3) {
    if (isChallenge) {
      nameChallenge = "Reto: " + nameChallenge;
    } else {
      nameChallenge = "Verdad: " + nameChallenge;
    }
  }
  $(".reto-game").text(nameChallenge);
  $(".name-game").text(nameGame);
  $(".cat-game").text(nameCategory);
}
