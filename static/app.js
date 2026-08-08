let socket = null;
let currentRoom = null;


const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const sendBtn = document.getElementById("sendBtn");
const createRoomBtn = document.getElementById("createRoomBtn");
const logoutBtn = document.getElementById("logoutBtn");

/* ---------------- Login ---------------- */

if (loginBtn) {
  loginBtn.onclick = async () => {
    const username = document.getElementById("username").value;
    const phone_number = document.getElementById("phone_number").value;
    const password = document.getElementById("password").value;

    if (!username || !phone_number || !password) {
      alert("Please fill in all fields");
      return;
    }

    try {
      const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, phone_number, password })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Login failed");
        return;
      }

      if (data.token) {
        localStorage.setItem("token", data.token);
      }

      window.location = "/chat.html";
    } catch (err) {
      console.error("Login error:", err);
      alert("Something went wrong while logging in.");
    }
  };
}


/* ---------------- Register ---------------- */

if (registerBtn) {
  registerBtn.onclick = async () => {
    const username = document.getElementById("username").value;
    const phone_number = document.getElementById("phone_number").value;
    const password = document.getElementById("password").value;

    if (!username || !phone_number || !password) {
      alert("Please fill in all fields");
      return;
    }

    try {
      const res = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, phone_number, password })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Registration failed");
        return;
      }

      alert("✅ Registered successfully! You can now log in.");
    } catch (err) {
      console.error("Register error:", err);
      alert("Something went wrong while registering.");
    }
  };
}

/* ---------------- Logout ---------------- */

if (logoutBtn) {
  logoutBtn.onclick = () => {
    localStorage.removeItem("token");
    if (socket) {
      socket.close();
    }
    window.location = "/login.html";
  };
}


/* ---------------- Create Room ---------------- */

if (createRoomBtn) {
  createRoomBtn.onclick = () => {
    const room = prompt("Room Name");
    if (room) {
      console.log(room);
      // POST /rooms
    }
  };
}


/* ---------------- Join Room ---------------- */

function joinRoom(roomID) {
  currentRoom = roomID;
  document.getElementById("roomTitle").innerText = "Room " + roomID;
  connectSocket(roomID);
}


/* ---------------- WebSocket ---------------- */

function connectSocket(roomID) {
  if (socket) {
    socket.close();
  }
  socket = new WebSocket(`ws://localhost:8000/ws/${roomID}`);

  socket.onopen = () => {
    document.getElementById("connectionStatus").innerHTML = "🟢 Connected";
  };

  socket.onclose = () => {
    document.getElementById("connectionStatus").innerHTML = "🔴 Disconnected";
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    addMessage(data.username, data.message, data.type);
  };
}


/* ---------------- Send ---------------- */

if (sendBtn) {
  sendBtn.onclick = sendMessage;
}

const input = document.getElementById("messageInput");

if (input) {
  input.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  });
}

function sendMessage() {
  if (!socket) return;
  const input = document.getElementById("messageInput");
  if (input.value === "") return;
  socket.send(JSON.stringify({ message: input.value }));
  input.value = "";
}

// =================================

function addMessage(username, message, type = "user") {
  const messages = document.getElementById("messages");
  const div = document.createElement("div");

  div.className = "message";
  if (type === "self") div.classList.add("self");
  if (type === "bot") div.classList.add("bot");

  div.innerHTML = `<strong>${username}</strong> <p>${message}</p>`;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}