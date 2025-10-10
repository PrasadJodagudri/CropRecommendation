// Import the functions you need from the Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";

// CRITICAL: PASTE YOUR FIREBASE CONFIG OBJECT HERE
// This is the most common source of errors.
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

// Get references to the HTML elements
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const loginButton = document.getElementById('login-button');
const signupButton = document.getElementById('signup-button');
const errorMessage = document.getElementById('error-message');

// --- Event Listener for Signup Button ---
signupButton.addEventListener('click', () => {
    const email = emailInput.value;
    const password = passwordInput.value;
    
    // Clear any previous error messages
    errorMessage.textContent = '';

    if (!email || !password) {
        errorMessage.textContent = "Please enter both email and password.";
        return;
    }

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed up successfully
            console.log("User signed up successfully!", userCredential.user);
            // Redirect to the dashboard
            window.location.href = 'dashboard.html'; 
        })
        .catch((error) => {
            // Handle errors
            console.error("Signup Error:", error.message);
            errorMessage.textContent = error.message;
        });
});

// --- Event Listener for Login Button ---
loginButton.addEventListener('click', () => {
    const email = emailInput.value;
    const password = passwordInput.value;

    // Clear any previous error messages
    errorMessage.textContent = '';

    if (!email || !password) {
        errorMessage.textContent = "Please enter both email and password.";
        return;
    }

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in successfully
            console.log("User logged in successfully!", userCredential.user);
            // Redirect to the dashboard
            window.location.href = 'dashboard.html';
        })
        .catch((error) => {
            // Handle errors
            console.error("Login Error:", error.message);
            errorMessage.textContent = error.message;
        });
});
