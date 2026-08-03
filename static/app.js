let socket = null;
let currentRoom = null;


const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const sendBtn = document.getElementById("sendBtn");
const createRoomBtn = document.getElementById("createRoomBtn");
const logoutBtn = document.getElementById("logoutBtn");


/* ---------------- Login ---------------- */

if(loginBtn){

loginBtn.onclick = async ()=>{

    console.log("Login");

    // TODO:
    // POST /login

};

}



/* ---------------- Register ---------------- */

if(registerBtn){

registerBtn.onclick = async ()=>{

    console.log("Register");

    // TODO:
    // POST /register

};

}

/* ---------------- Logout ---------------- */

if(logoutBtn){

logoutBtn.onclick = ()=>{

    localStorage.removeItem("token");

    if(socket){
        socket.close();
    }

    window.location="/login";

};

}



/* ---------------- Create Room ---------------- */

if(createRoomBtn){

createRoomBtn.onclick=()=>{

    const room=prompt("Room Name");

    if(room){

        console.log(room);
        // POST /rooms
    }

};

}



/* ---------------- Join Room ---------------- */

function joinRoom(roomID){

    currentRoom=roomID;

    document.getElementById("roomTitle").innerText="Room "+roomID;

    connectSocket(roomID);

}



/* ---------------- WebSocket ---------------- */

function connectSocket(roomID){

    if(socket){
        socket.close();
    }
    socket=new WebSocket(`ws://localhost:8000/ws/${roomID}`);



    socket.onopen=()=>{document.getElementById("connectionStatus").innerHTML="🟢 Connected";

    };



    socket.onclose=()=>{

    document.getElementById("connectionStatus").innerHTML="🔴 Disconnected";

    };

socket.onmessage=(event)=>{

const data=JSON.parse(event.data);
addMessage(data.username,data.message,data.type);

    };

}



/* ---------------- Send ---------------- */

if(sendBtn){sendBtn.onclick=sendMessage;}


const input=document.getElementById("messageInput");

if(input){input.addEventListener("keypress",(event)=>{

    if(event.key==="Enter"){
        sendMessage();
    }

});

}

function sendMessage(){

    if(!socket)return;

    const input=document.getElementById("messageInput");

    if(input.value==="")return;

    socket.send(JSON.stringify({message:input.value}));

    input.value="";

}
// =================================

function addMessage(username,message,type="user"){

    const messages=document.getElementById("messages");
    const div=document.createElement("div");

    div.className="message";

    if(type==="self")
        div.classList.add("self");



    if(type==="bot")
        div.classList.add("bot");

    div.innerHTML=`<strong>${username}</strong> <p>${message}</p>`;
    messages.appendChild(div);
    messages.scrollTop=messages.scrollHeight;

}