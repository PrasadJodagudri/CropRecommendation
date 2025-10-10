// Import the functions you need from the Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAUzsRO6hm2DtVzPqJ8t3PhV_bK2maiDbI",
    authDomain: "crop-recommendation-app-d81ea.firebaseapp.com",
    projectId: "crop-recommendation-app-d81ea",
    storageBucket: "crop-recommendation-app-d81ea.firebasestorage.app",
    messagingSenderId: "42714055647",
    appId: "1:42714055647:web:32cccc20fd0eda92de7a6a",
    measurementId: "G-9ZTV23Z1EM"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const loginButton = document.getElementById('login-button');
const signupButton = document.getElementById('signup-button');
const errorMessage = document.getElementById('error-message');

// Handle Signup
signupButton.addEventListener('click', () => {
    const email = emailInput.value;
    const password = passwordInput.value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in
            console.log("User signed up successfully!", userCredential.user);
            window.location.href = 'index.html'; // Redirect to main app
        })
        .catch((error) => {
            errorMessage.textContent = error.message;
        });
});

// Handle Login
loginButton.addEventListener('click', () => {
    const email = emailInput.value;
    const password = passwordInput.value;

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in
            console.log("User logged in successfully!", userCredential.user);
            window.location.href = 'index.html'; // Redirect to main app
        })
        .catch((error) => {
            errorMessage.textContent = error.message;
        });
});