cd "flask_backend"
start cmd /k "python -m venv venv && venv\Scripts\activate && python main.py"
cd "../react_frontend"
start cmd /k npm run dev
