let stars = [];

const canvas = document.getElementById("bh-bg");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const context = canvas.getContext("2d");
const centerX = canvas.width / 2;
const centerY = canvas.height / 2;
const starRadius = 2.5;

// 1000 ms / n frames
const frameTime = 1000 / 60;

class Star {
  constructor() {
    this.x = Math.random() * canvas.height;
    this.y = Math.random() * canvas.height;
    // this.ax = -0.5;
    this.ax = -Math.random();
    this.vx = this.ax;
  }

  move() {
    this.vx += this.ax;
    this.x += this.vx;
    context.beginPath();
    context.arc(this.x, this.y, starRadius, 0, 2 * Math.PI, false);
    context.fillStyle = "white";
    context.fill();

    if (this.x <= 0) {
      // Reset
      this.x = canvas.width;
      this.y = Math.random() * canvas.height;
      this.vx = 0;
    }
  }
}

// Create 100 stars
for (let i = 0; i < 150; i++) {
  stars[i] = new Star();
}

// Update
setInterval(() => {
  context.clearRect(0, 0, canvas.width, canvas.height);
  stars.forEach((star) => {
    star.move();
  });
}, frameTime);

// Resize canvas if necessary
window.onresize = () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
};

// TODO: Convert to request for high refresh rate support(?)
function onUpdate() {}

// window.requestAnimationFrame(onUpdate);
