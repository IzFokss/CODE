let particlesArray = [];

const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const ctx = canvas.getContext('2d');

// Track mouse position globally
let mouseX = 0;
let mouseY = 0;

particlesArray.push({
    x: mouseX,
    y: mouseY,
    radius: Math.random() * 4 + 1,
    speedX: Math.random() * 2 - 1,
    speedY: Math.random() * 2 - 0.5,
    life: 1.0,
    r: Math.floor(Math.random() * 256),  // add these
    g: Math.floor(Math.random() * 256),
    b: Math.floor(Math.random() * 256)
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
        ctx.fillStyle = `rgba(${p.r}, ${p.g}, ${p.b}, ${p.life})`;
        ctx.fill();
    }

    requestAnimationFrame(updateParticles);
}

updateParticles();