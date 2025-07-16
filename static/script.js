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
    options: [], // will be filled dynamically
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
  // reset answers
  for (const key in answers) delete answers[key];
};

prevBtn.onclick = () => {
  if (current
