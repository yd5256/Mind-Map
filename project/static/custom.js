const starsContainer = document.getElementById("stars");
const starCount = 150;

for (let i = 0; i < starCount; i++) {
  const star = document.createElement("div");
  star.className = "star";

  // Add color variety
  const colorRand = Math.random();
  if (colorRand < 0.1) {
    star.style.background = "#ffd700";
    star.style.boxShadow = "0 0 4px #ffd700";
  } else if (colorRand < 0.2) {
    star.style.background = "#ff69b4";
    star.style.boxShadow = "0 0 4px #ff69b4";
  } else if (colorRand < 0.3) {
    star.style.background = "#da70ff";
    star.style.boxShadow = "0 0 4px #da70ff";
  }

  const size = Math.random() * 3 + 1;
  star.style.width = `${size}px`;
  star.style.height = `${size}px`;

  star.style.left = `${Math.random() * 100}%`;
  star.style.top = `${Math.random() * 100}%`;

  star.style.animationDuration = `${Math.random() * 3 + 2}s`;
  star.style.animationDelay = `${Math.random() * 3}s`;

  starsContainer.appendChild(star);
}