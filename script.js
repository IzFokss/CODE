// Snowfall animation implementation
const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const ctx = canvas.getContext('2d');

const snowflakes = [];
const numSnowflakes = 100;

function createSnowflakes() {
    for (let i = 0; i < numSnowflakes; i++) {
        snowflakes.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 4 + 1,
            speed: Math.random() * 1 + 0.5,
            sway: Math.random() * 2 - 1
        });
    }
}

function updateSnowflakes() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let flake of snowflakes) {
        flake.x += flake.sway;
        flake.y += flake.speed;

        // Bounce back when hitting the edges
        if (flake.x > canvas.width || flake.x < 0) {
            flake.x = Math.random() * canvas.width;
            flake.y = 0; // Reset to top
        }

        // Draw snowflake
        ctx.beginPath();
        ctx.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.fill();
    }
    requestAnimationFrame(updateSnowflakes);
}

createSnowflakes();
updateSnowflakes();