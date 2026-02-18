let particlesArray = [];

const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const ctx = canvas.getContext('2d');

// Track mouse position globally
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;

    // Spawn a few particles at cursor position on each move
    for (let i = 0; i < 3; i++) {
        particlesArray.push({
            x: mouseX,
            y: mouseY,
            radius: Math.random() * 4 + 1,
            speedX: Math.random() * 2 - 1,   // random horizontal drift
            speedY: Math.random() * 2 - 0.5, // drift slightly downward
            life: 1.0                         // opacity, fades out over time
        });
    }
});

function updateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = particlesArray.length - 1; i >= 0; i--) {
        const p = particlesArray[i];

        p.x += p.speedX;
        p.y += p.speedY;
        p.life -= 0.02; // fade out

        if (p.life <= 0) {
            particlesArray.splice(i, 1); // remove dead particles
            continue;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 200, 50, ${p.life})`; // golden, fades out
        ctx.fill();
    }

    requestAnimationFrame(updateParticles);
}

updateParticles();