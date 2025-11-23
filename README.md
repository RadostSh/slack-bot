# **Incident Communication Helper with Saved History**

A Flask-based Slack bot that processes incident descriptions and generates customer-facing and internal messages using Google Gemini AI. The bot automatically saves incident data to a Parse Server database.

---

## Project Features

- **AI-Powered Message Generation:** Uses **Google Gemini AI** to process raw incident descriptions and instantly generate two distinct, professional outputs: a customer-facing status message and a technical internal note for support teams.
- **RESTful API Interface:** Provides a single, clean HTTP endpoint (**/incident-handler**) for easily processing incident data from external services (**simulating Slack interaction**).
- **Database Integration:** Automatically saves incident communication records (incident text, customer message, and internal message) to a **Parse Server database (Back4App)** for historical tracking.
- **Error Handling:** Implements error handling across the service layer:
  - **Configuration Validation:** Validates all required environment variables on startup
  - **Input Validation:** Validates request data before processing
  - **AI Service Errors:** Catches and logs AI service failures
  - **Database Errors:** Handles database save failures (returns messages even if save fails)
  - **HTTP Error Handlers:** Custom error handlers for 400 and 500 errors

---

## **Project Structure**

```
slack-bot/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration management
│   ├── routes.py            # Primary HTTP endpoint (/incident-handler)
│   ├── models/
│   │   └── incident.py      # Data models
│   └── services/
│       ├── ai_service.py    # Gemini AI integration
│       └── db_service.py    # Parse Server integration
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

---

## Technical Stack

| Category             | Technology                  | Details                                                |
| -------------------- | --------------------------- | ------------------------------------------------------ |
| **Backend Language** | **Python 3.12**             | Primary development language.                          |
| **Web Framework**    | **Flask 3.0.0**             | Used for the application structure and routing.        |
| **AI Model**         | **Google Gemini 2.5 Flash** | Used via the Google Gemini API for message generation. |
| **Database**         | **Back4App (Parse Server)** | Used to store incident records.                        |

---

## Installation and Startup

**Follow these steps to set up and run the project locally**

1. Clone and Set Up Environment

First, create a virtual environment to isolate dependencies and avoid version conflicts.

```bash
# Clone the repository or navigate to project folder
git clone <repository-url>
cd slack-bot

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

1. Install dependencies:

Install the required Python packages (Flask, Google Generative AI SDK, Requests)

```bash
pip install -r requirements.txt
```

1. Configure Environment Variables

Create a file named **.env** in the root directory. Add your API keys for Google Gemini and Back4App.

```bash
# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Back4App (Parse Server) Configuration
PARSE_APPLICATION_ID=your_back4app_application_id
PARSE_REST_API_KEY=your_back4app_rest_api_key
PARSE_SERVER_URL=https://parseapi.back4app.com/parse
```

1. Run the Server

```bash
python3 run.py
```

You should see the following output indicating the server is running:
 *** Running on http://127.0.0.1:5000**

---

## Technical Implementation Details & Constraints

The development process involved specific decisions and solutions to overcome technical constraints related to LLM performance and data persistence:

### 1. AI Model Selection and Stability

- **Constraint (OpenAI):** The free tier of OpenAI models was unsuitable due to limitations on the number of prompts allowed during testing.
- **Constraint (Gemini Pro):** Initial use of **Gemini 2.5 Pro** resulted in the AI constantly triggering **Safety Blocks** (**finish_reason: 2**) when processing technical incident prompts, interpreting the content as potentially dangerous.
- **Solution (Gemini Flash):** Switching to **Gemini 2.5 Flash** mitigated the issue of safety blocks.

### 2. Database Migration (SashiDo to Back4App)

The initial plan to use SashiDo for storage was altered due to registration/connection difficulties.

- **Action:** The database was migrated to **Back4App**.
- **Result:** Since both SashiDo and Back4App adhere to the **Parse Server standard**, the implementation code in **db_service.py** remained **unchanged** and fully reusable.

---

## Future Improvements

Transition from the current HTTP Simulation to a **Fully Integrated Production System (Slack)**

- **Implement Real-Time Event Listening** - connect the bot to live Slack activity (**app_mention events** and **slash command**)
- **Active Bi-Directional Communication** - **Slack Web Client Integration** - the backend should send the generated messages back to the specific Slack channel where the request originated
- **Security: Request Verification** - make sure the **/incident-handler** endpoint only processes requests that are confirmed to come from **Slack**