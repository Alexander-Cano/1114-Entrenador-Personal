const toast = document.getElementById("toast");
let timer;

function showMessage(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(timer);
  timer = setTimeout(() => toast.classList.remove("show"), 2400);
}

async function loadDashboard() {
  const response = await fetch("/api/dashboard");
  const data = await response.json();

  document.getElementById("userName").textContent = data.user.name;
  document.getElementById("todayLabel").textContent = data.today_label;
  document.getElementById("workoutTitle").textContent = data.today_workout.title;
  document.getElementById("workoutMeta").textContent = `${data.today_workout.duration} min · ${data.today_workout.level}`;
  document.getElementById("streak").textContent = `${data.stats.streak} días`;
  document.getElementById("minutes").textContent = `${data.stats.week_minutes} min`;
  document.getElementById("continueTitle").textContent = data.continue_workout.title;
  document.getElementById("continueMeta").textContent = `${data.continue_workout.progress} de ${data.continue_workout.duration} minutos completados`;

  const days = data.week.map(day => {
    const active = day.active ? "active" : "";
    return `<button class="day ${active}"><span>${day.name}</span><strong>${day.number}</strong></button>`;
  });
  document.getElementById("weekDays").innerHTML = days.join("");
}

document.getElementById("startBtn").addEventListener("click", async () => {
  const response = await fetch("/api/workouts/today/start", { method: "POST" });
  const data = await response.json();
  showMessage(data.message);
  loadDashboard();
});

document.getElementById("calendarBtn").addEventListener("click", () => {
  showMessage("Calendario de septiembre abierto.");
});

document.getElementById("weekDays").addEventListener("click", event => {
  const day = event.target.closest(".day");
  if (!day) return;
  document.querySelector(".day.active")?.classList.remove("active");
  day.classList.add("active");
});

document.querySelectorAll(".nav-item").forEach(item => {
  item.addEventListener("click", () => {
    document.querySelector(".nav-item.active").classList.remove("active");
    item.classList.add("active");
  });
});

loadDashboard().catch(() => showMessage("Inicia la app con Python para cargar tus datos."));
