
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js';
import { getDatabase, ref, set, onValue } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-database.js';

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
const database = getDatabase(app);

const service = {}

service.load =  (username) => {
    console.log("loading data...");
    const userref = ref(database, username)
    
    return new Promise((resolve, reject) => {
        onValue(userref, (snapshot) => {
            const data = snapshot.val();
            if(data) {
                resolve(data);
            } else {
                reject(new Error("No data avaliable!"))
            }
        }, (error) => {
            reject(error)
        })
    }) 
}

service.set = (url, data) => {
    set(ref(database, url ), data)
}


export {service}