import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";

const firebaseConfig = {
    apiKey: "AIzaSyDSc-dbYnuIgPLopZtAC1O51re5eH0lp_Y",
    authDomain: "iiot-7276b.firebaseapp.com",
    databaseURL: "https://iiot-7276b-default-rtdb.firebaseio.com",
    projectId: "iiot-7276b",
    storageBucket: "iiot-7276b.appspot.com",
    messagingSenderId: "243048858008",
    appId: "1:243048858008:web:08f7674d96b5ef34416bed",
    measurementId: "G-PJRZFGJ2GB"
};

const app = initializeApp(firebaseConfig);
export {app}

console.log("Script loaded");