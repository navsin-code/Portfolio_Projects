// Global variables
let postureChart = null;
let previousPostureStatus = '';
let goalSeconds = 0;
let currentStreak = 0;
let showedFoxAnimation = false;
let showedGoalAnimation = false;
let characterPhrases = {
    'upright': [
        "Looking good! Keep it up!",
        "Excellent posture! 👍",
        "Your back will thank you!",
        "You're doing great!",
        "Look at you sitting like a pro!"
    ],
    'slouching': [
        "Oops! Let's fix that posture!",
        "Straighten up a bit! 🔄",
        "Remember to sit upright!",
        "Let's correct that slouch!",
        "Your future self thanks you for sitting straight!"
    ],
    'streak': [
        "Amazing streak going! Keep it up!",
        "Wow! Your posture streak is impressive!",
        "You're on fire with your posture!",
        "Consistency is key, and you're nailing it!",
        "Your posture discipline is goals!"
    ]
};

// Helper Functions
function showPopup(popupId) {
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.classList.add('active');

        // Auto-hide after 5 seconds
        setTimeout(() => {
            popup.classList.remove('active');
        }, 5000);
    }
}

function hidePopup(popupId) {
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.classList.remove('active');
    }
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
}

function getRandomPhrase(category) {
    const phrases = characterPhrases[category];
    return phrases[Math.floor(Math.random() * phrases.length)];
}

function updateCharacterSpeech() {
    const characterSpeech = document.getElementById('character-speech');
    if (!characterSpeech) return;

    if (currentStreak >= 10 * 60) { // 10 minutes or more
        characterSpeech.textContent = getRandomPhrase('streak');
    } else if (previousPostureStatus === 'Upright') {
        characterSpeech.textContent = getRandomPhrase('upright');
    } else {
        characterSpeech.textContent = getRandomPhrase('slouching');
    }
}

// Posture Data Functions
function checkPostureData() {
    fetch('/get_posture_data')
        .then(response => response.json())
        .then(data => {
            updatePostureUI(data);

            // Check for streak milestones
            currentStreak = data.current_streak;
            goalSeconds = data.goal_seconds;

            if (currentStreak >= 30 * 60 && !showedFoxAnimation) { // 30 minutes
                showPopup('fox-animation');
                showedFoxAnimation = true;
            }

            if (currentStreak >= goalSeconds && !showedGoalAnimation) {
                const goalMessage = document.getElementById('goal-message');
                if (goalMessage) {
                    const hours = Math.floor(goalSeconds / 3600);
                    goalMessage.textContent = `You sat straight for ${hours} hour${hours !== 1 ? 's' : ''}!`;
                }
                showPopup('goal-celebration');
                showedGoalAnimation = true;

                // Reset after showing celebration
                setTimeout(() => {
                    showedFoxAnimation = false;
                    showedGoalAnimation = false;
                }, 5000);
            }

            // Update every 2 seconds
            setTimeout(checkPostureData, 2000);
        })
        .catch(error => {
            console.error('Error fetching posture data:', error);
            setTimeout(checkPostureData, 5000); // Retry after 5 seconds
        });
}

function updatePostureUI(data) {
    // Update streak counter
    const streakCounter = document.getElementById('streak-counter');
    const streakMinutes = document.getElementById('streak-minutes');

    if (streakCounter) {
        const minutes = Math.floor(data.current_streak / 60);
        streakCounter.textContent = minutes;
    }

    if (streakMinutes) {
        const minutes = Math.floor(data.current_streak / 60);
        streakMinutes.textContent = minutes + ' mins';
    }

    // Update posture status
    const postureStatus = document.getElementById('posture-status');
    const postureIcon = document.getElementById('posture-icon');

    if (data.posture_data && data.posture_data.length > 0) {
        const latestPosture = data.posture_data[data.posture_data.length - 1];

        if (postureStatus) {
            if (latestPosture.status === 'Upright') {
                postureStatus.textContent = 'Great posture! Keep it up!';
                previousPostureStatus = 'Upright';
                if (postureIcon) {
                    postureIcon.className = 'fas fa-user';
                    postureIcon.style.color = '#7ED7A9'; // success color
                }
            } else {
                postureStatus.textContent = 'Careful! You\'re slouching!';
                previousPostureStatus = 'Slouch';
                if (postureIcon) {
                    postureIcon.className = 'fas fa-user-slash';
                    postureIcon.style.color = '#FF6B6B'; // error color
                }
            }
        }
    }
}

// Progress Chart Functions
function initProgressChart() {
    const ctx = document.getElementById('posture-chart');
    if (!ctx) return;

    postureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Posture Status',
                    data: [],
                    borderColor: '#C5F7E2',
                    backgroundColor: 'rgba(197, 247, 226, 0.2)',
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#C5F7E2',
                    stepped: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: 0,
                    max: 1,
                    ticks: {
                        stepSize: 1,
                        callback: function(value) {
                            return value === 0 ? 'Slouching' : 'Upright';
                        },
                        count: 2
                    },
                    grid: {
                        display: true,
                        drawBorder: true
                    }
                },
                x: {
                    ticks: {
                        maxTicksLimit: 8,
                        maxRotation: 0
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function updateProgress() {
    fetch('/get_posture_data')
        .then(response => response.json())
        .then(data => {
            updateProgressChart(data);
            updateProgressBar(data);
        })
        .catch(error => {
            console.error('Error fetching progress data:', error);
        });
}

let currentChartView = 'hour';

function updateProgressChart(data) {
    if (!postureChart) return;

    const labels = [];
    const chartData = [];

    let dataToShow;
    if (currentChartView === 'hour') {
        // Last 20 entries for hourly view
        dataToShow = data.posture_data.slice(-20);
    } else {
        // For day view, show aggregated data (every 10th entry for longer timespan)
        dataToShow = data.posture_data.filter((_, index) => index % 10 === 0).slice(-20);
    }

    for (const entry of dataToShow) {
        const date = new Date(entry.time);
        if (currentChartView === 'hour') {
            labels.push(date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
        } else {
            labels.push(date.toLocaleDateString([], { month: 'short', day: 'numeric' }));
        }
        chartData.push(entry.status === 'Upright' ? 1 : 0);
    }

    postureChart.data.labels = labels;
    postureChart.data.datasets[0].data = chartData;
    postureChart.update();
}

function switchChartView(view) {
    currentChartView = view;

    // Update toggle buttons
    document.querySelectorAll('.chart-toggle').forEach(toggle => {
        toggle.classList.remove('active');
    });
    event.target.classList.add('active');

    // Refresh chart with new view
    updateProgress();
}

function updateProgressBar(data) {
    const progressFill = document.getElementById('progress-fill');
    const progressPercentage = document.getElementById('progress-percentage');
    const progressFillMini = document.getElementById('progress-bar-mini');
    const progressPercent = document.getElementById('progress-percent');

    if (data.goal_seconds === 0) return;

    const percentage = Math.min(100, Math.round((data.current_streak / data.goal_seconds) * 100));

    // Update main progress page bars
    if (progressFill && progressPercentage) {
        progressFill.style.width = `${percentage}%`;
        progressPercentage.textContent = `${percentage}%`;
    }

    // Update mini progress bar on main page
    if (progressFillMini && progressPercent) {
        progressFillMini.style.width = `${percentage}%`;
        progressPercent.textContent = `${percentage}%`;
    }
}

// Meetings Functions
function loadMeetings() {
    fetch('/get_meetings')
        .then(response => response.json())
        .then(meetings => {
            displayMeetings(meetings);
        })
        .catch(error => {
            console.error('Error fetching meetings:', error);
        });
}

function displayMeetings(meetings) {
    const meetingsList = document.getElementById('meetings-list');
    const noMeetings = document.getElementById('no-meetings');

    if (!meetingsList) return;

    meetingsList.innerHTML = '';

    if (meetings.length === 0) {
        if (noMeetings) {
            noMeetings.style.display = 'block';
        }
        return;
    }

    if (noMeetings) {
        noMeetings.style.display = 'none';
    }

    for (const meeting of meetings) {
        const meetingDate = new Date(meeting.dateTime);

        const meetingItem = document.createElement('div');
        meetingItem.className = 'meeting-item';

        const meetingDateEl = document.createElement('div');
        meetingDateEl.className = 'meeting-date';
        meetingDateEl.textContent = `${meetingDate.toLocaleDateString()} at ${meetingDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;

        const meetingReminder = document.createElement('div');
        meetingReminder.className = 'meeting-reminder';
        meetingReminder.textContent = `Reminder: ${meeting.reminder} minutes before`;

        meetingItem.appendChild(meetingDateEl);
        meetingItem.appendChild(meetingReminder);

        meetingsList.appendChild(meetingItem);
    }
}

// UI Interaction Functions
function showPostureTips() {
    showPopup('tips-popup');
}

function closeTips() {
    hidePopup('tips-popup');
}

function animateLeaderboard() {
    anime({
        targets: '.leaderboard-item',
        translateX: [50, 0],
        opacity: [0, 1],
        delay: anime.stagger(100),
        easing: 'easeOutQuad',
        duration: 800
    });

    anime({
        targets: '.trophy-icon',
        rotate: [0, 20, 0, -20, 0],
        duration: 1500,
        easing: 'easeInOutQuad',
        loop: true
    });
}

// Tips slider functionality
let currentTipIndex = 0;
let tipInterval;

function initTipsSlider() {
    const tipSlides = document.querySelectorAll('.tip-slide');
    const tipDots = document.querySelectorAll('.tip-dot');

    if (tipSlides.length === 0) return;

    function showTip(index) {
        // Hide all slides
        tipSlides.forEach(slide => slide.classList.remove('active'));
        tipDots.forEach(dot => dot.classList.remove('active'));

        // Show current slide
        tipSlides[index].classList.add('active');
        tipDots[index].classList.add('active');
    }

    function nextTip() {
        currentTipIndex = (currentTipIndex + 1) % tipSlides.length;
        showTip(currentTipIndex);
    }

    // Auto-rotate tips every 4 seconds
    tipInterval = setInterval(nextTip, 4000);

    // Add click handlers to dots
    tipDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentTipIndex = index;
            showTip(currentTipIndex);
            // Reset interval
            clearInterval(tipInterval);
            tipInterval = setInterval(nextTip, 4000);
        });
    });
}

// Initialize tips slider when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initTipsSlider();
});