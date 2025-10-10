import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";

// CRITICAL: PASTE YOUR FIREBASE CONFIG OBJECT HERE
const firebaseConfig = {
    apiKey: "AIzaSyAUzsRO6hm2DtVzPqJ8t3PhV_bK2maiDbI",
    authDomain: "crop-recommendation-app-d81ea.firebaseapp.com",
    projectId: "crop-recommendation-app-d81ea",
    storageBucket: "crop-recommendation-app-d81ea.firebasestorage.app",
    messagingSenderId: "42714055647",
    appId: "1:42714055647:web:32cccc20fd0eda92de7a6a",
    measurementId: "G-9ZTV23Z1EM"
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// --- Element References ---
const userEmailSpan = document.getElementById('user-email');
const userInfoDiv = document.getElementById('user-info');
const logoutButton = document.getElementById('logout-button');
const historyContainer = document.getElementById('history-container');
const loadingSpinner = document.getElementById('loading-spinner');
const emptyState = document.getElementById('empty-state');
// Stat elements
const totalRecsEl = document.getElementById('total-recs');
const uniqueCropsEl = document.getElementById('unique-crops');
const frequentCropEl = document.getElementById('frequent-crop');
const lastRecCropEl = document.getElementById('last-rec-crop');
// Chart elements
const chartCanvas = document.getElementById('recommendationChart');
const chartSubtitle = document.getElementById('chart-subtitle');
let recommendationChart = null; // To hold the chart instance

// --- Main Function on Page Load ---
onAuthStateChanged(auth, async (user) => {
    if (user) {
        userInfoDiv.style.display = 'block';
        userEmailSpan.textContent = user.email;
        await fetchAndDisplayHistory(user);
    } else {
        window.location.href = 'login.html';
    }
});

// --- Data Fetching and Display Logic ---
async function fetchAndDisplayHistory(user) {
    try {
        const idToken = await user.getIdToken();
        const response = await fetch('http://127.0.0.1:5000/history', {
            method: 'GET',
            headers: { 'Authorization': 'Bearer ' + idToken }
        });
        if (!response.ok) throw new Error('Could not fetch history.');
        
        const historyData = await response.json();
        loadingSpinner.style.display = 'none';

        if (historyData.length === 0) {
            emptyState.classList.remove('hidden');
            chartSubtitle.textContent = 'No data available to display chart.';
        } else {
            updateStats(historyData);
            displayHistoryCards(historyData);
            // Render chart with data from the MOST RECENT recommendation
            renderRecommendationChart(historyData[0].inputs); 
        }
    } catch (error) {
        loadingSpinner.style.display = 'none';
        historyContainer.innerHTML = `<p class="text-red-500 text-center">Error: Could not load your history.</p>`;
        console.error("Fetch history error:", error);
    }
}

// --- Helper Functions ---
function updateStats(data) {
    totalRecsEl.textContent = data.length;
    lastRecCropEl.textContent = data[0].crop; // Most recent is first

    const cropNames = data.map(item => item.crop);
    const uniqueCrops = new Set(cropNames);
    uniqueCropsEl.textContent = uniqueCrops.size;

    if (cropNames.length > 0) {
        const cropCounts = cropNames.reduce((acc, crop) => ({ ...acc, [crop]: (acc[crop] || 0) + 1 }), {});
        const mostFrequent = Object.keys(cropCounts).reduce((a, b) => cropCounts[a] > cropCounts[b] ? a : b);
        frequentCropEl.textContent = mostFrequent;
    }
}

function displayHistoryCards(data) {
    historyContainer.innerHTML = ''; // Clear spinner/empty state
    data.forEach((item, index) => {
        const date = new Date(item.timestamp + 'Z'); // Add 'Z' to treat it as UTC
        const formattedDate = date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
        
        const card = document.createElement('div');
        card.className = 'bg-slate-50/50 backdrop-blur-sm p-4 rounded-lg border border-slate-200 transition-all hover:shadow-md hover:border-green-500 animate-fade-in';
        card.style.animationDelay = `${index * 100}ms`; // Staggered animation
        card.innerHTML = `
            <div class="flex justify-between items-start">
                <div>
                    <p class="font-bold text-lg text-green-700">${item.crop}</p>
                    <p class="text-xs text-slate-500">${formattedDate}</p>
                </div>
                <div class="text-xs text-slate-500 bg-slate-200 px-2 py-1 rounded-full">
                    <span class="font-semibold">${item.inputs.city}</span>
                </div>
            </div>
            <div class="mt-3 pt-3 border-t text-sm text-slate-600 grid grid-cols-2 sm:grid-cols-4 gap-2">
                <span><strong>N:</strong> ${item.inputs.N}</span>
                <span><strong>P:</strong> ${item.inputs.P}</span>
                <span><strong>K:</strong> ${item.inputs.K}</span>
                <span><strong>pH:</strong> ${item.inputs.ph}</span>
            </div>
        `;
        historyContainer.appendChild(card);
    });
}

function renderRecommendationChart(data) {
    if (recommendationChart) {
        recommendationChart.destroy(); // Destroy previous chart instance if it exists
    }

    chartSubtitle.textContent = `Soil data from last analysis in ${data.city}`;
    const ctx = chartCanvas.getContext('2d');
    
    // Normalizing values for better visualization on a radar chart
    // Max values from the dataset description are roughly N:140, P:145, K:205, pH:9
    const chartData = {
        labels: ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)', 'Soil pH'],
        datasets: [{
            label: 'Soil Nutrient Levels',
            data: [
                (data.N / 140) * 100,
                (data.P / 145) * 100,
                (data.K / 205) * 100,
                (data.ph / 9.5) * 100, // pH is on a different scale (max is ~9.5)
            ],
            backgroundColor: 'rgba(34, 197, 94, 0.2)', // green-500 with transparency
            borderColor: 'rgba(22, 163, 74, 1)', // green-600
            borderWidth: 2,
            pointBackgroundColor: '#fff',
            pointBorderColor: 'rgba(22, 163, 74, 1)',
            pointHoverBackgroundColor: 'rgba(22, 163, 74, 1)',
            pointHoverBorderColor: '#fff'
        }]
    };

    recommendationChart = new Chart(ctx, {
        type: 'radar', // A radar chart is great for this kind of multi-variate data
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                    grid: { color: 'rgba(0, 0, 0, 0.1)' },
                    pointLabels: { 
                        font: { 
                            size: 12,
                            family: "'Inter', sans-serif"
                        },
                        color: '#475569' // slate-600
                    },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: {
                        backdropColor: 'rgba(255, 255, 255, 0.75)',
                        stepSize: 25,
                        // Display '%' symbol
                        callback: function(value) {
                            return value + '%'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false // We don't need a legend for a single dataset
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.dataset.label}: ${context.raw.toFixed(2)}% of ideal max`;
                        }
                    }
                }
            }
        }
    });
}

// --- Event Listeners ---
logoutButton.addEventListener('click', () => {
    signOut(auth).catch(error => console.error("Sign out error", error));
});

