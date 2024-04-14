const express = require("express");
const app = express();
const http = require("http");
const { join } = require("path");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

const port = 3000;

app.use(express.static("static"));

piSocket = null;
userSocket = null;
joinCode = "";

io.on("connection", (socket) => {
  console.log("a user connected");
  socket.on("message", (msg) => {
    console.log(msg);
    io.emit("message", msg + " we love Duke");
  });
  if (!piSocket) {
    socket.emit("message", "PI IS GONE");
    socket.emit("piDisconnected");
  }

  // USER MESSAGES
  socket.on("tryConnect", () => {
    if (userSocket && socket.id != userSocket.id) {
      return socket.emit("tryConnect", "Another user is already connected");
    }
    console.log("trying to connect");
    if (piSocket) {
      socket.emit("tryConnect", "received");
      io.to("pi").emit("tryConnect");
    } else {
      socket.emit("tryConnect", "PI IS GONE");
    }
  });

  socket.on("joinCode", (msg) => {
    if (msg == joinCode) {
      userSocket = socket;
      socket.join("user");
      socket.emit("joinCode", "success");
      io.to("pi").emit("joinCode", "success");
    } else {
      socket.emit("joinCode", "fail");
      io.to("pi").emit("joinCode", "fail");
    }
  });

  socket.on("press", (msg) => {
    if (piSocket) {
      console.log("sending program", msg);
      io.to("pi").emit("press", msg);
    }
  });

  socket.on("gameCommand", (msg) => {
    if (piSocket) {
      console.log("sending command", msg);
      io.to("pi").emit("gameCommand", msg);
    }
  });

  // PI MESSAGES

  socket.on("supersecretpimessage", (msg) => {
    if (piSocket) return;
    if (msg == "3.1415926535897932384626433832769") {
      socket.join("pi");
      socket.emit("supersecretpimessage", "success");
      io.emit("piJoined");
      piSocket = socket;
      console.log("Connected to the pi");
    }
  });

  socket.on("piJoinCode", (msg) => {
    console.log("got a join code", msg);
    if (piSocket && socket.id == piSocket.id) {
      joinCode = msg;
    }
  });

  socket.on("programList", (msg) => {
    if (piSocket && socket.id != piSocket.id) return;
    if (!userSocket) return;

    console.log("Recieved program list: " + msg);
    io.to("user").emit("programList", msg);
  });

  socket.on("disconnect", () => {
    if (piSocket && socket.id == piSocket.id) {
      piSocket = null;
      console.log("Disconnected from the pi");
      io.emit("piDisconnected");
      userSocket = null; //must reenter code to become user
    } else if (userSocket && socket.id == userSocket.id) {
      userSocket = null;
    }
  });
});

server.listen(port, () => {
  console.log(`Example app listening on port http://localhost:${port}`);
});
