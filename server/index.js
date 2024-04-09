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

  // USER MESSAGES
  socket.on("tryConnect", () => {
    // if (userSocket) {
    //   return socket.emit("tryConnect", "already connected");
    // }
    console.log("trying to connect");
    socket.emit("tryConnect", "received");
    io.to("pi").emit("tryConnect");
  });

  socket.on("joinCode", (msg) => {
    console.log("join code", msg);
    if (msg == joinCode) {
      console.log("YAYAYYAAYAYYAY");
      userSocket = socket;
      socket.emit("joinCode", "success");
      io.to("pi").emit("joinCode", "success");
      console.log("sent success");
    } else {
      socket.emit("joinCode", "fail");
      io.to("pi").emit("joinCode", "fail");
    }
  });

  socket.on("chooseProgram", (msg) => {
    if (piSocket) {
      console.log("sending program", msg);
      io.to(piSocket).emit("chooseProgram", msg);
    }
  });

  // PI MESSAGES

  socket.on("supersecretpimessage", (msg) => {
    if (msg == "3.1415926535897932384626433832769") {
      socket.join("pi");
      socket.emit("supersecretpimessage", "success");
      piSocket = socket;
    }
  });

  socket.on("piJoinCode", (msg) => {
    console.log("got a join code", msg);
    if (piSocket && socket.id == piSocket.id) {
      joinCode = msg;
    }
  });

  socket.on("programList", (msg) => {
    if (userSocket) {
      console.log("Recieved program list: " + msg);
      io.to(userSocket).emit("programList", msg);
    }
  });

  socket.on("disconnect", () => {
    if (piSocket && socket.id == piSocket.id) {
      piSocket = null;
    } else if (userSocket && socket.id == userSocket.id) {
      userSocket = null;
    }
  });
});

server.listen(port, () => {
  console.log(`Example app listening on port http://localhost:${port}`);
});
