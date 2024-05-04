# CommuniCare Project
![communicare-high-resolution-logo](https://github.com/GeoffreyFClark/CommuniCare/blob/main/react_frontend/public/communicare_logo.png)

![image](https://github.com/GeoffreyFClark/CommuniCare/assets/97141856/c10c77ec-8fd4-4c39-9c77-7e560b133149)

Welcome to the CommuniCare project repository!

This application is designed to connect people with community resources and volunteering opportunities such as food banks, medical clinics, churches, etc. 

This project uses React for the frontend and Flask for the backend.

## Prerequisites
- Git
- Node.js (which comes with npm)
- Python 3 (which comes with pip, starting with Python 3.4 and newer)

## Project Setup
Optionally, you may choose to fork the repository if you want to work on your own features independently before merging them into the main project.

Clone the repository:
`git clone https://github.com/GeoffreyFClark/CommuniCare` </br>
or if forked: `git clone https://github.com/YourGitHubUsername/CommuniCare`

### Backend setup:

`cd communiCare`

`cd flask_backend`

`python -m venv venv`

`venv\Scripts\activate` (On Mac: `source venv/bin/activate`)

`pip install -r requirements.txt`

### Frontend setup:

`cd ../react_frontend`

`npm install`

## Run the Development Server

Navigate to the flask_backend directory and run `python main.py`

In a new terminal, navigate to the react_frontend directory and run `npm run dev`

View at the frontend's localhost:port which will then be linked in the terminal.
