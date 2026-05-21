/* main.js — typing effect + cursor glow */
(function () {
  // Typing effect
  const el = document.getElementById("typing");
  if (el) {
    const words = ["Python Developer", "Creative Coder", "Frontend Designer", "Cloud Computing Learner"];
    let i = 0, j = 0, deleting = false;
    function tick() {
      const word = words[i];
      el.textContent = word.slice(0, j);
      if (!deleting && j < word.length) { j++; setTimeout(tick, 90); }
      else if (!deleting && j === word.length) { deleting = true; setTimeout(tick, 1400); }
      else if (deleting && j > 0) { j--; setTimeout(tick, 50); }
      else { deleting = false; i = (i + 1) % words.length; setTimeout(tick, 200); }
    }
    tick();
  }

  // Cursor glow (desktop only)
  if (window.matchMedia("(min-width: 769px)").matches) {
    const dot = document.getElementById("cursor-dot");
    const glow = document.getElementById("cursor-glow");
    document.addEventListener("mousemove", (e) => {
      dot.style.left = glow.style.left = e.clientX + "px";
      dot.style.top  = glow.style.top  = e.clientY + "px";
    });
    document.addEventListener("mouseleave", () => {
      dot.style.opacity = glow.style.opacity = 0;
    });
    document.addEventListener("mouseenter", () => {
      dot.style.opacity = 1; glow.style.opacity = .35;
    });
  }

  // Auto-dismiss flash
  setTimeout(() => {
    document.querySelectorAll(".flash").forEach(f => {
      f.style.transition = "opacity .5s"; f.style.opacity = 0;
      setTimeout(() => f.remove(), 500);
    });
  }, 4000);
})();
