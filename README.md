# AI Interview System

An end-to-end, AI-powered interview simulation platform that guides a candidate through a configurable interview flow, generates questions dynamically using an LLM, retrieves relevant evidence from the candidate profile/resume and job description context, evaluates answers in real time, and produces a post-interview report with transcript history.

---

## Overview

This project simulates a realistic interview session from start to finish:

* The user configures interview settings and optionally Interviewer policy.
* The frontend sends job details, resume/profile data, and session preferences to the backend.
* The backend prepares the interview session, builds retrieval context, and coordinates the AI interviewer.
* The LLM generates the next question based on current state, difficulty, history, and Resume evidence.
* The user answers through the chat interface.
* The backend evaluates the answer, updates the interview state, and continues until the interview ends.
* After the interview, the system generates a detailed evaluation report and allows the user to review the transcript.
* User can view past interviews and evaluations
* User can Build profile once in profile section for much better interview experience and avoid
uploading the resume again.

This repository is containerized with Docker for consistent local setup and deployment.

---

## Key Features

* Interactive AI interview chat flow
* Configurable interview settings
* Resume/profile and job-description-driven questioning
* Retrieval-augmented context generation using FAISS
* Dynamic next-question selection based on interview state
* Real-time answer evaluation
* Post-interview report generation
* Transcript viewing and interview history support
* Past Interview history and evaluations
* Profile building page
* Dockerized setup for reproducible execution

---

## Architecture

The system is organized around five main components:

* **User**: Starts the interview, answers questions, reviews results, and opens the transcript.
* **Frontend**: Handles UI state, settings, interview chat, loading screens, report display, and transcript modal.
* **Backend**: Orchestrates session setup, state management, retrieval, question generation, answer evaluation, and persistence.
* **LLM**: Generates interview questions and evaluation summaries.
* **Database**: Stores session data, interview turns, evaluation output, and history.


## Sequence Diagram

**Add your main sequence diagram here.**

Suggested placement:

```md
## Sequence Diagram

![End-to-End AI Interview Session Sequence Diagram](docs/diagrams/sequence-diagram.png)
```

> This diagram shows the complete interview lifecycle, from session setup to transcript review.

### Optional additional diagrams

If you want to keep the README readable, place supporting diagrams in the same `docs/diagrams/` folder and embed them in their own sections:

* `docs/diagrams/architecture.png` — system architecture overview
* `docs/diagrams/database-schema.png` — database design
* `docs/diagrams/ui-flow.png` — frontend navigation / user flow
* `docs/diagrams/deployment.png` — Docker / deployment flow

Suggested section layout:

```md
## Architecture Diagram

![Architecture Diagram](docs/diagrams/architectureDiagram.png)

## Database Schema

![Database Schema](docs/diagrams/database-schema.png)
```
    
---

## Project Structure

You should update this section to match your actual repository structure.

```text
.
├── backend/
├── frontend/
├── docs/
│   └── diagrams/
├── docker/
├── .env
├── docker-compose.yml
├── Dockerfile
└── README.md
```

Example sub-structure:

```text
backend/
├── app/
├── services/
├── routes/
├── models/
├── utils/
└── main.py

frontend/
├── src/
├── components/
├── pages/
├── assets/
└── package.json
```

---

## Tech Stack

Replace or adjust this list to match your actual implementation.

* **Frontend**: HTML, CSS, JavaScript / React / your UI framework
* **Backend**: Python / FastAPI / Flask / your backend framework
* **AI**: LLM-based generation and evaluation
* **Retrieval**: FAISS
* **Storage**: Database for sessions, turns, and history
* **Containerization**: Docker, Docker Compose

---

## Installation

### Prerequisites

* Docker
* Docker Compose
* Git

### Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

---

## Environment Variables

Create a `.env` file if your project uses environment variables.

Example:

```env
LLM_API_KEY=your_key_here
DATABASE_URL=your_database_url_here
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

Add or remove variables based on your project.

---

## Run with Docker

### Using Docker Compose

```bash
docker compose up --build
```

### Using Docker directly

If you have separate images or services:

```bash
docker build -t ai-interview-system .
docker run -p 8000:8000 ai-interview-system
```

If your frontend and backend run as separate services, document their ports clearly here.

---

## Usage

1. Open the application in your browser.
2. Configure interview settings.
3. Upload or provide resume/profile information if required.
4. Start the interview.
5. Answer each question in the chat interface.
6. Wait for the final evaluation report.
7. Review the transcript and past interview records.

---

## API Endpoints

Update this section to match your real routes.

```text
POST /setup
POST /startInterview
POST /send_text
GET  /evaluation/{sessionId}
GET  /transcript/{sessionId}
```

Responsibilities:

* `POST /setup` — initialize interview settings and session data
* `POST /startInterview` — begin the interview workflow
* `POST /send_text` — submit a user answer
* `GET /evaluation/{sessionId}` — fetch the final report
* `GET /transcript/{sessionId}` — fetch interview transcript data

---


## Docker Notes

Since the project is containerized, Docker helps with:

* consistent runtime behavior
* easy local setup
* isolated dependencies
* simplified deployment

Recommended files:

* `Dockerfile`
* `docker-compose.yml`
* `.dockerignore`

If your project uses multiple services, describe each one here, for example:

* frontend service
* backend service
* database service
* vector retrieval service

---

## Screenshots

Add screenshots here to show the actual UI.

Suggested placement:

```md
## Screenshots

### Home Screen
![Home Screen](docs/screenshots/home.png)

### Interview in Progress
![Interview Screen](docs/screenshots/interview.png)

### Evaluation Report
![Evaluation Report](docs/screenshots/report.png)

### Transcript Modal
![Transcript Modal](docs/screenshots/transcript.png)
```

---

## Future Improvements

* Better analytics for answer quality trends
* Enhanced recommendation of follow-up questions
* Exportable PDF report
* More detailed transcript filtering/search
* Additional question strategies for harder interviews
* Expanded admin or history dashboard

---

## Known Limitations

Add only the limitations that are true for your implementation.

Examples:

* The project depends on external LLM responses.
* Evaluation quality may vary based on model output.
* The retrieval quality depends on the resume/profile data provided.

---

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

---

## License

Add your license information here.

```text
MIT License
```

Or replace with the license that matches your repository.

---

## Acknowledgments

* LLM-based interview generation and evaluation
* FAISS for retrieval support
* Docker for containerized deployment

---

## Contact

Add your contact or GitHub profile here.

```text
Your Name / GitHub / Email
```
