// GLOBAL TASK STORAGE (loaded from DB)
let dbTasks = [];


// -----------------------------
// LOAD SAVED TASKS FROM DATABASE
// -----------------------------
window.onload = function () {
    loadTasksFromDB();
};


function loadTasksFromDB() {
    fetch("http://127.0.0.1:8000/api/tasks/all/")
        .then(res => res.json())
        .then(data => {
            dbTasks = data;
            console.log("Loaded tasks from DB:", dbTasks);
        })
        .catch(err => console.error("DB Load Error:", err));
}



// -----------------------------
// ADD TASK TO DATABASE
// -----------------------------
function addTaskToDB() {
    const title = document.getElementById("title").value;
    const due_date = document.getElementById("due_date").value || null;
    const estimated_hours = parseFloat(document.getElementById("hours").value);
    const importance = parseInt(document.getElementById("importance").value);
    const dependenciesRaw = document.getElementById("dependencies").value.trim();

    const dependencies = dependenciesRaw.length > 0
        ? dependenciesRaw.split(",").map(id => id.trim())
        : [];

    fetch("http://127.0.0.1:8000/api/tasks/add/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title,
            due_date,
            estimated_hours,
            importance,
            dependencies
        })
    })
    .then(res => res.json())
    .then(data => {
        alert("Task added successfully!");
        loadTasksFromDB();  // refresh list after save
    })
    .catch(err => {
        alert("Error saving task!");
        console.error(err);
    });
}



// -----------------------------
// DETERMINE WHICH TASKS TO ANALYZE
// -----------------------------
function getTasks() {
    const bulk = document.getElementById("bulk_json").value.trim();

    if (bulk.length > 0) {
        try {
            return JSON.parse(bulk);
        } catch (err) {
            alert("❌ Invalid JSON format in bulk input!");
            return [];
        }
    }

    // DEFAULT → use DB tasks
    return dbTasks;
}



// -----------------------------
// ANALYZE ALL TASKS
// -----------------------------
function analyzeTasks() {
    const tasks = getTasks();
    const strategy = document.getElementById("strategy").value;

    if (tasks.length === 0) {
        alert("No tasks found to analyze!");
        return;
    }

    fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tasks, strategy })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.tasks) {
            alert("Error analyzing tasks. Check backend logs.");
            return;
        }
        displayResults(data.tasks);
    })
    .catch(err => console.error("Analyze Error:", err));
}



// -----------------------------
// SUGGEST TOP 3 TASKS
// -----------------------------
function suggestTasks() {
    const tasks = getTasks();
    const strategy = document.getElementById("strategy").value;

    if (tasks.length === 0) {
        alert("No tasks available to suggest!");
        return;
    }

    fetch("http://127.0.0.1:8000/api/tasks/suggest/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tasks, strategy })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.suggested_tasks) {
            alert("Error fetching suggestions!");
            return;
        }
        displayResults(data.suggested_tasks);
    })
    .catch(err => console.error("Suggest Error:", err));
}



// -----------------------------
// DISPLAY RESULTS ON UI
// -----------------------------
function displayResults(list) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    list.forEach(task => {
        const color =
            task.priority_level === "High" ? "priority-high" :
            task.priority_level === "Medium" ? "priority-medium" :
            "priority-low";

        container.innerHTML += `
            <p>
                <strong>${task.title}</strong> — 
                <span class="${color}">${task.priority_level}</span> <br>
                Score: ${task.score} <br>
                ${task.explanation || ""} <br>
                <hr>
            </p>
        `;
    });
}
