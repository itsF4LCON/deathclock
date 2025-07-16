const questions = [
  {
    key: "age",
    title: "What is your age?",
    example: "Your current age in years, e.g. 25",
    inputType: "number",
    options: null,
  },
  {
    key: "country",
    title: "Select your country",
    example: "Choose your country from the list",
    inputType: "select",
    options: [], // will be filled dynamically from countries.json
  },
  {
    key: "smoker",
    title: "Do you smoke?",
    example: "Select yes if you smoke regularly",
    inputType: "select",
    options: ["yes", "no"],
  },
  {
    key: "exercise",
    title: "Do you exercise regularly?",
    example: "Select yes if you exercise at least 3 times per week",
    inputType: "select",
    options: ["yes", "no"],
  },
  {
    key: "diet",
    title: "How would you describe your diet?",
    example: "Choose healthy, average or unhealthy",
    inputType: "select",
    options: ["healthy", "average", "unhealthy"],
  },
  {
    key: "alcohol",
    title: "Alcohol consumption?",
    example: "Select none, light or heavy",
    inputType: "select",
    options: ["none", "light", "heavy"],
  },
  {
    key: "sleep",
    title: "How many hours of sleep do you get?",
    example: "Select less (<6), normal (6-8), or more (>8)",
    inputType: "select",
    options: ["less", "normal", "more"],
  },
  {
    key: "stress",
    title: "Stress level?",
    example: "Select low, medium, or high",
    inputType: "select",
    options: ["low", "medium", "high"],
  },
  {
    key: "medical",
    title: "Medical conditions?",
    example: "Select none, some, or severe",
    inputType: "select",
    options: ["none", "some", "severe"],
  },
];

let currentQuestionIndex = 0;
const answers = {};

const welcomeScreen = document.getElementById("welcome-screen");
const questionScreen = document.getElementById("question-screen");
const resultScreen = document.getElementById("result-screen");
const startBtn = document.getElementById("start-btn");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");
const restartBtn = document.getElementById("restart-btn");

const questionTitle = document.getElementById("question-title");
const questionExample = document.getElementById("question-example");
const inputArea = document.getElementById("input-area");

const deathDateEl = document.getElementById("death-date");
const lifeYearsEl = document.getElementById("life-years");
const countdownEl = document.getElementById("countdown");

startBtn.onclick = () => {
  welcomeScreen.classList.add("hidden");
  questionScreen.classList.remove("hidden");
  currentQuestionIndex = 0;
  showQuestion();
};

restartBtn.onclick = () => {
  resultScreen.classList.add("hidden");
  welcomeScreen.classList.remove("hidden");
  for (const key in answers) delete answers[key];
};

prevBtn.onclick = () => {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    showQuestion();
  }
};

nextBtn.onclick = () => {
  if (!validateAnswer()) return;
  saveAnswer();
  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex++;
    showQuestion();
  } else {
    submitAnswers();
  }
};

function showQuestion() {
  prevBtn.disabled = currentQuestionIndex === 0;
  nextBtn.disabled = true;
  const q = questions[currentQuestionIndex];
  questionTitle.textContent = q.title;
  questionExample.textContent = q.example;

  inputArea.innerHTML = "";

  if (q.inputType === "number") {
    const input = document.createElement("input");
    input.type = "number";
    input.min = 0;
    input.value = answers[q.key] || "";
    input.oninput = () => {
      nextBtn.disabled = input.value.trim() === "" || isNaN(input.value) || input.value <= 0;
    };
    inputArea.appendChild(input);
  } else if (q.inputType === "select") {
    const select = document.createElement("select");
    select.innerHTML = '<option value="">-- Select --</option>';

    if (q.key === "country" && q.options.length === 0) {
      nextBtn.disabled = true; // disable next until countries loaded
      fetch('/static/countries.json')
        .then(res => res.json())
        .then(data => {
          q.options = data.map(c => c.name);
          q.lifeExpectancies = {};
          data.forEach(c => {
            q.lifeExpectancies[c.name] = c.life_expectancy;
          });

          q.options.forEach(country => {
            const option = document.createElement("option");
            option.value = country;
            option.textContent = country;
            select.appendChild(option);
          });
          if (answers[q.key]) select.value = answers[q.key];
          nextBtn.disabled = select.value === "";
        })
        .catch(() => {
          alert("Failed to load countries.");
          nextBtn.disabled = false;
        });
    } else {
      q.options.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt;
        option.textContent = opt.charAt(0).toUpperCase() + opt.slice(1);
        select.appendChild(option);
      });
      select.value = answers[q.key] || "";
      nextBtn.disabled = select.value === "";
    }

    select.onchange = () => {
      nextBtn.disabled = select.value === "";
    };

    inputArea.appendChild(select);
  }
}

function validateAnswer() {
  const input = inputArea.querySelector("input, select");
  if (!input) return false;
  if (input.value.trim() === "") {
    alert("Please answer the question.");
    return false;
  }
  if (input.type === "number" && (isNaN(input.value) || input.value <= 0)) {
    alert("Please enter a valid positive number.");
    return false;
  }
  return true;
}

function saveAnswer() {
  const input = inputArea.querySelector("input, select");
  if (!input) return;
  answers[questions[currentQuestionIndex].key] = input.value.trim();
}

function submitAnswers() {
  fetch("/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(answers),
  })
    .then(res => res.json())
    .then(data => {
      showResult(data);
    })
    .catch(() => {
      alert("Failed to calculate. Please try again.");
    });
}

function showResult(data) {
  questionScreen.classList.add("hidden");
  resultScreen.classList.remove("hidden");
  deathDateEl.textContent = data.death_date;
  
  // Calculate life years from seconds (1 year ~ 365.25 days)
  const lifeYears = data.seconds / (365.25 * 24 * 3600);
  lifeYearsEl.textContent = lifeYears.toFixed(1);

  let secondsLeft = data.seconds;
  updateCountdown(secondsLeft);

  const interval = setInterval(() => {
    secondsLeft--;
    if (secondsLeft < 0) {
      clearInterval(interval);
      countdownEl.textContent = "Time's up!";
      return;
    }
    updateCountdown(secondsLeft);
  }, 1000);

  function updateCountdown(sec) {
    const hrs = Math.floor(sec / 3600);
    const mins = Math.floor((sec % 3600) / 60);
    const secs = sec % 60;
    countdownEl.textContent = `Time left: ${hrs}h ${mins}m ${secs}s`;
  }
}
