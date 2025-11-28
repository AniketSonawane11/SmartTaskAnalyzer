# 🧠 Smart Task Analyzer – Internship Assignment (Python + Django + JS)

This project was built for the Software Development Intern assessment at **Singularium Technologies**.  
It is a full-stack system that intelligently scores and prioritizes tasks using a custom algorithm.

---

## 🚀 Features

### ✔ Backend (Django REST Framework)

- Custom scoring algorithm:
  - Urgency (due date)
  - Importance (1–10 scale)
  - Effort (estimated hours)
  - Dependencies (including cycle detection)
- Multiple strategies:
  - Smart Balance
  - Fastest Wins
  - High Impact
  - Deadline Driven
- APIs:
  - `/api/tasks/add/` – save task to DB
  - `/api/tasks/all/` – fetch saved tasks
  - `/api/tasks/analyze/` – compute priority scores
  - `/api/tasks/suggest/` – suggest top 3 tasks
- Unit tests for scoring logic

---

### ✔ Frontend

- Add tasks from UI  
- Bulk JSON input  
- Strategy dropdown  
- Analyze results  
- Suggest top 3  
- Color-coded priority indicators  
- Responsive UI with Bootstrap  

---

### ✔ Database

- MySQL with environment variable support  
- `.env` file used for DB credentials  
- `.env` ignored by Git for security  

---

## 🖥 Project UI

Below is the main interface of the Smart Task Analyzer tool:

![Smart Task Analyzer UI](smart-task-analyzer-ui.png)

---

## ⚙ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/SmartTaskAnalyzer.git
cd SmartTaskAnalyzer/backend
2️⃣ Create virtual environment
bash
Copy code
python -m venv venv
venv/Scripts/activate   # Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Add environment variables
Create a .env file in the backend folder:

ini
Copy code
DB_NAME=taskdb
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
5️⃣ Run migrations
bash
Copy code
python manage.py migrate
6️⃣ Start the backend server
bash
Copy code
python manage.py runserver
7️⃣ Run frontend
Open the file manually in your browser:

bash
Copy code
frontend/index.html
🧪 Unit Tests
Three unit tests in tests.py cover:

Score calculation

Strategy output ordering

Dependency cycle detection

Run tests:

bash
Copy code
python manage.py test
🧠 Design Decisions
Algorithm-first approach: Designed the scoring weights and logic before coding UI or APIs.

Cycle detection: Added safeguard to stop infinite loops in dependencies.

Separation of concerns: Scoring logic isolated in scoring.py for readability & testing.

Strategy plug-ins: Built sorting strategies as modular functions, easier to extend later.

Environment variables: Used .env for DB settings; ensured security via .gitignore.

User-first frontend: Simple, quick, responsive layout for easy testing and UX clarity.

⏳ Time Breakdown
Task	Time Spent
Algorithm design	1 hr
Backend API	1 hr
Frontend UI + JS	1 hr
Debugging + Testing	45 min
Documentation	30 min

🚀 Future Improvements
Eisenhower Matrix (Urgent vs Important grid view)

Weekend/holiday-aware urgency calculation

Dependency graph visualization

Save suggestions feedback to improve algorithm

Dark/Light mode for frontend

Store suggestions history

📬 Contact
Feel free to reach out for questions or improvements.

Aniket Sonawane
📧 Email: your-email
🔗 GitHub: https://github.com/AniketSonawane11
