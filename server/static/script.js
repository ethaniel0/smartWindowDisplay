var socket = io();
socket.on("message", function (data) {
  console.log(data);
});

socket.on("tryConnect", (msg) => {
  if (msg == "received") {
    document.getElementById("error-msg").innerHTML = "";
    if (!document.getElementById("joinCode")) {
      let inputElement = document.createElement("input");
      inputElement.id = "joinCode";
      inputElement.placeholder = "Join Code";
      inputElement.onchange = () => socket.emit("joinCode", inputElement.value);
      document.body.appendChild(inputElement);
    } else {
      document.getElementById("joinCode").value = "";
      document.getElementById("joinCode").style.backgroundColor = "white";
    }
  } else {
    document.getElementById("error-msg").innerHTML = msg;
  }
});

socket.on("programList", (list) => {
  let buttons = document.getElementById("buttons");
  clearButtons();
  clearGameScreens();
  console.log(list, typeof list);
  if (typeof list == "string") {
    showGameScreen(list);
    return;
  }

  console.log("program list", list);
  for (let i = 0; i < list.length; i++) {
    let button = document.createElement("button");
    button.innerHTML = list[i];
    button.onclick = () => socket.emit("press", list[i]);
    buttons.appendChild(button);
  }
});

socket.on("joinCode", (msg) => {
  if (msg == "success") {
    let connectBtn = document.getElementById("connect-btn");
    let code_input = document.getElementById("joinCode");
    connectBtn.classList.add("hidden");
    code_input.remove();
  }
});

socket.on("piDisconnected", () => {
  console.log("No pi");
  clearButtons();
  clearGameScreens();
  document.getElementById("error-msg").innerHTML = "PI IS GONE";
  let connectBtn = document.getElementById("connect-btn");
  connectBtn.classList.remove("hidden");
  if (document.getElementById("joinCode")) {
    document.getElementById("joinCode").remove();
  }
});

socket.on("piJoined", () => {
  console.log("Connected to the pi");
  document.getElementById("error-msg").innerHTML = "";
});

socket.on("youLost", (msg) => {
  console.log("You lost");
  startButton();
});

function connect() {
  console.log("trying to connect over here");
  socket.emit("tryConnect");
}

function clearButtons() {
  let buttons = document.getElementById("buttons");
  buttons.innerHTML = "";
}

function goBack() {
  socket.emit("press", "Back");
}

function sendGameCommand(msg) {
  socket.emit("gameCommand", msg);
}

function showGameScreen(game) {
  let simon = document.getElementById("simon");
  let general = document.getElementById("general-game");
  let jump = document.getElementById("jump");

  clearGameScreens();

  if (game == "Simon") simon.classList.remove("hidden");
  else if (game == "Jump") jump.classList.remove("hidden");
  else general.classList.remove("hidden");

  let needStarts = ["Simon", "Jump"];

  if (needStarts.includes(game)) {
    startButton();
  }
}

function clearGameScreens() {
  let simon = document.getElementById("simon");
  let general = document.getElementById("general-game");
  let jump = document.getElementById("jump");

  simon.classList.add("hidden");
  general.classList.add("hidden");
  jump.classList.add("hidden");
}

function simonButtons() {
  let colors = ["Red", "Green", "Blue", "Yellow"];
  for (let i = 0; i < colors.length; i++) {
    let button = document.createElement("button");
    button.innerHTML = colors[i];
    button.style.backgroundColor = colors[i];
    button.onclick = () => socket.emit("gameCommand", colors[i]);
    buttons.appendChild(button);
  }
}

function gamepad(leftright = true) {
  let buttons = document.getElementById("buttons");
  let up = document.createElement("button");
  up.innerHTML = "Up";
  up.onclick = () => socket.emit("gameCommand", "up");
  buttons.appendChild(up);

  let down = document.createElement("button");
  down.innerHTML = "Down";
  down.onclick = () => socket.emit("gameCommand", "down");
  buttons.appendChild(down);

  if (!leftright) return;

  let left = document.createElement("button");
  left.innerHTML = "Left";
  left.onclick = () => socket.emit("gameCommand", "left");
  buttons.appendChild(left);

  let right = document.createElement("button");
  right.innerHTML = "Right";
  right.onclick = () => socket.emit("gameCommand", "right");
  buttons.appendChild(right);
}

function startButton() {
  let startButton = document.createElement("button");
  startButton.innerHTML = "Start";
  startButton.style.marginTop = "2rem";
  startButton.onclick = () => {
    socket.emit("gameCommand", "start");
    startButton.remove();
  };
  buttons.appendChild(startButton);
}
