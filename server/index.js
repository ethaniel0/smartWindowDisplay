const express = require('express')
const app = express()
const http = require('http');
const { join } = require('path');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

const port = 3000

app.use(express.static('static'));

piSocket = null;
userSocket = null;
joinCode = ''

io.on('connection', (socket) => {
    console.log('a user connected');
    socket.on('message', (msg) => {
        console.log(msg);
        io.emit('message', msg + " we love Duke");
    });

    // USER MESSAGES
    socket.on('tryConnect', msg => {
        if (userSocket){
            return socket.emit('tryConnect', 'already connected');
        }
        socket.emit('tryConnect', 'received');
        io.to('pi').emit('tryConnect');

        userSocket = socket.id;
    });

    socket.on('joinCode', msg => {
        if (msg == joinCode) {
            userSocket = socket;
            socket.emit('joinCode', 'success');
        }
    })

    socket.on('chooseProgram', msg => {
        if (piSocket) {
            io.to(piSocket).emit('chooseProgram', msg);
        }
    });

    // PI MESSAGES

    socket.on('supersecretpimessage', msg => {
        if (msg == "3.1415926535897932384626433832769") {
            socket.join('pi');
            socket.emit('message', "pi message received");
            piSocket = socket;
        }
    })

    socket.on('piJoinCode', msg => {
        if (piSocket && socket.id == piSocket.id) {
            joinCode = msg;
        }
    });

    socket.on('disconnect', () => {
        if (socket.id == piSocket.id) {
            piSocket = null;
        }
        else if (socket.id == userSocket.id) {
            userSocket = null;
        }
    })
});
  

server.listen(port, () => {
  console.log(`Example app listening on port http://localhost:${port}`)
})