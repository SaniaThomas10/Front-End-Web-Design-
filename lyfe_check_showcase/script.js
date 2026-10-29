
// Dark mode
const themeButton = document.getElementById("theme-toggle");

themeButton.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        themeButton.textContent = "Light Mode";
    } else {
        themeButton.textContent = "Dark Mode";
    }
});


// LYFE CHECK features
const features = [
    {
        name: "Calendar & Planning",
        category: "Productivity",
        description: "Organize schedules and upcoming events."
    },
    {
        name: "Habit Tracking",
        category: "Wellness",
        description: "Build and monitor daily habits."
    },
    {
        name: "Mood Tracking",
        category: "Wellness",
        description: "Record moods and recognize patterns."
    },
    {
        name: "Journaling",
        category: "Wellness",
        description: "Reflect on experiences and personal growth."
    },
    {
        name: "Goal Setting",
        category: "Productivity",
        description: "Establish and monitor personal goals."
    },
    {
        name: "Task Management",
        category: "Productivity",
        description: "Organize and complete daily tasks."
    },
    {
        name: "Progress Analytics",
        category: "Insights",
        description: "Review productivity and wellness progress."
    },
    {
        name: "AI Wellness Assistant",
        category: "Planned",
        description: "A planned feature for wellness suggestions and journaling prompts."
    }
];


// Feature explorer elements
const searchInput = document.getElementById("feature-search");
const categorySelect = document.getElementById("feature-category");
const featureList = document.getElementById("feature-list");
const featureCount = document.getElementById("feature-count");


// Current filters
const state = {
    search: "",
    category: "All"
};


// Display matching features
function render() {
    featureList.innerHTML = "";

    const matchingFeatures = features.filter(function (feature) {
        const matchesSearch =
            feature.name.toLowerCase().includes(state.search) ||
            feature.description.toLowerCase().includes(state.search);

        const matchesCategory =
            state.category === "All" ||
            feature.category === state.category;

        return matchesSearch && matchesCategory;
    });

    matchingFeatures.forEach(function (feature) {
        const card = document.createElement("div");
        card.className = "feature-card";

        const heading = document.createElement("h3");
        heading.textContent = feature.name;

        const category = document.createElement("p");
        category.className = "feature-category";
        category.textContent = feature.category;

        const description = document.createElement("p");
        description.textContent = feature.description;

        card.appendChild(heading);
        card.appendChild(category);
        card.appendChild(description);

        featureList.appendChild(card);
    });

    featureCount.textContent =
        "Showing " + matchingFeatures.length + " of " + features.length;
}


// Live search
searchInput.addEventListener("input", function () {
    state.search = searchInput.value.toLowerCase().trim();
    render();
});


// Category filter
categorySelect.addEventListener("change", function () {
    state.category = categorySelect.value;
    render();
});


// Show features on page load
render();


// Quiz elements
const quizForm = document.getElementById("quiz-form");
const quizError = document.getElementById("quiz-error");
const quizResult = document.getElementById("quiz-result");


// Quiz recommendations
const recommendations = {
    schedule:
        "LYFE CHECK's Calendar and Task Management features can help you organize your schedule and prioritize responsibilities.",

    "journal-time":
        "LYFE CHECK's Journaling feature provides a dedicated space to record your thoughts and build a consistent reflection routine.",

    productivity:
        "LYFE CHECK's Habit Tracking, Task Management, and Progress Analytics can help you stay organized and monitor your progress.",

    inspiration:
        "LYFE CHECK's planned AI Wellness Assistant could provide journaling prompts and suggestions to help you get started."
};


// Quiz submission
quizForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const selectedAnswer = document.querySelector(
        'input[name="struggle"]:checked'
    );

    quizError.textContent = "";
    quizResult.textContent = "";

    if (selectedAnswer === null) {
        quizError.textContent = "Please select an option before submitting.";
        return;
    }

    const recommendation = recommendations[selectedAnswer.value];

    const heading = document.createElement("h3");
    heading.textContent = "How LYFE CHECK Can Help";

    const message = document.createElement("p");
    message.textContent = recommendation;

    quizResult.appendChild(heading);
    quizResult.appendChild(message);
});
