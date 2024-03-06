importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js");

var firebaseConfig = {
    apiKey: "AIzaSyDk-6BrlcSSWDyPr_1rcitip3IIjdBuGZU",
    authDomain: "storage-43adb.firebaseapp.com",
    projectId: "storage-43adb",
    storageBucket: "storage-43adb.appspot.com",
    messagingSenderId: "1061053949926",
    appId: "1:1061053949926:web:291940cbdfcd2030a75827",
    measurementId: "G-K4LN3K4YTM"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
    console.log(payload)
})