// Character animations and celebrations

// Animation for fox celebration
function animateFoxCelebration() {
    anime({
        targets: '.fox-container img',
        translateY: [-20, 0],
        scale: [0.8, 1],
        opacity: [0, 1],
        easing: 'easeOutElastic(1, .8)',
        duration: 800,
        complete: function() {
            anime({
                targets: '.fox-container img',
                translateY: [-10, 10],
                direction: 'alternate',
                loop: true,
                easing: 'easeInOutSine',
                duration: 1200
            });
        }
    });
}

// Animation for goal celebration
function animateGoalCelebration() {
    // Animate characters
    anime({
        targets: '.celebration-characters img',
        translateY: [50, 0],
        opacity: [0, 1],
        delay: anime.stagger(200),
        easing: 'easeOutElastic(1, .8)',
        duration: 1000
    });

    // Animate confetti
    anime({
        targets: '.confetti span',
        translateY: [0, '100vh'],
        translateX: function() {
            return anime.random(-20, 20) + 'px';
        },
        rotate: function() {
            return anime.random(0, 360);
        },
        opacity: [0, 1, 0],
        easing: 'easeOutExpo',
        duration: function() {
            return anime.random(1000, 3000);
        },
        delay: anime.stagger(200),
        loop: true
    });
}

// Animation for character in the main page
function animateCharacter() {
    anime({
        targets: '.character-img',
        translateY: [-5, 5],
        direction: 'alternate',
        loop: true,
        easing: 'easeInOutQuad',
        duration: 1500
    });
}

// Animation for speech bubbles
function animateSpeechBubble() {
    anime({
        targets: '.speech-bubble',
        scale: [0.95, 1],
        duration: 1500,
        easing: 'easeInOutQuad',
        direction: 'alternate',
        loop: true
    });
}

// Animation for wave emoji
function animateWave() {
    anime({
        targets: '.wave',
        rotate: [0, 20, -10, 15, -5, 0],
        duration: 1800,
        easing: 'easeInOutQuad',
        loop: true
    });
}

// Set up event listeners for popup animations
document.addEventListener('DOMContentLoaded', function() {
    // Initialize character animation
    animateCharacter();
    animateSpeechBubble();
    animateWave();

    // Set up observers for popup animations
    const foxObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                const element = mutation.target;
                if (element.classList.contains('active')) {
                    animateFoxCelebration();
                }
            }
        });
    });

    const goalObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                const element = mutation.target;
                if (element.classList.contains('active')) {
                    animateGoalCelebration();
                }
            }
        });
    });

    const foxPopup = document.getElementById('fox-animation');
    const goalPopup = document.getElementById('goal-celebration');

    if (foxPopup) {
        foxObserver.observe(foxPopup, { attributes: true });
    }

    if (goalPopup) {
        goalObserver.observe(goalPopup, { attributes: true });
    }
});