# **Incident Communication Helper with Saved History**

A Flask-based Slack bot that processes incident descriptions and generates customer-facing and internal messages using Google Gemini AI. The bot automatically saves incident data to a Parse Server database.

---

## Project Features

- **AI-Powered Message Generation:** Uses **Google Gemini AI** to process raw incident descriptions and instantly generate two distinct, professional outputs: a customer-facing status message and a technical internal note for support teams.
- **RESTful API Interface:** Provides a single, clean HTTP endpoint (**/incident-handler**) for easily processing incident data from external services (**simulating Slack interaction**).
- **Database Integration:** Automatically saves incident communication records (incident text, customer message, and internal message) to a **Parse Server database (Back4App)** for historical tracking.
- **Error Handling:** Implements resilient error handling across the service layer:
  - **Configuration Validation:** Validates all required environment variables on startup
  - **Input Validation:** Validates request data before processing
  - **AI Service Errors:** Catches and logs AI service failures
  - **Database Errors:** Gracefully handles database save failures (returns messages even if save fails)
  - **HTTP Error Handlers:** Custom error handlers for 400 and 500 errors

---

## **Tech Stack**

- **Backend language**: Python 3.12
- **Framework:** Flask 3.0.0
- **AI**: Google Gemini API
  - Gemini model: Gemini 2.5 flash
- **Parse Server:** Back4app

---

## **Project Structure**

```
slack-bot/
├── app/
│   ├── __**init**__.py          # Flask app factory
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

## Live Demo

Demonstrated the complete data flow using a single HTTP POST request (simulate Slack requests with **Postman**). The process validates the successful connection between the **Flask Backend, Google Gemini AI, and the Back4App Database**.

### Input and AI Transformation (Postman)

This step verifies that the Flask endpoint is functional and the AI service successfully generates the required messages

![image.png](/assets/postman.png)

### Data Persistence (Back4App Dashboard)

The data is successfully stored in the permanent database, fulfilling the historical tracking requirement.

![image.png](/assets/back4app.png)

---

## **Technical Decisions and Trade-offs**

### **Choice of LLM: Gemini Flash vs. OpenAI**

**Decision:** The project utilises **Google Gemini 2.5 Flash** instead of OpenAI (GPT-3.5/4)

**Performance vs. Cost:**

- Gemini Flash is optimised for high speed and low latency, which is critical for a bot where engineers need immediate feedback during an incident. It is also cost-effective (free tier for development).
- While OpenAI models might sometimes follow complex instructions better, Flash offers the best balance of speed and sufficient intelligence.

### Gemini Safety Filters & Model Selection

**The Challenge: Infrastructure incidents often sound "dangerous" to an AI.**

- Gemini's default safety settings interpret some technical terms as **Harmful Content** (Harassment or Dangerous Content), triggering a **finish_reason: 2** (Safety Block). This causes the API to return an empty response or an error, crashing the bot.

**The Solution: Switching to Gemini Flash -** the project switched from **Gemini Pro** to **Gemini 2.5 Flash**.

- "Pro" models often have more complex safety alignment designed for open-ended reasoning. **Gemini Flash**, being optimised for speed and high-volume tasks, is less prone to "over-thinking" the potential danger of technical terms, resulting in fewer false positives and **finish_reason: 2** errors.
- We trade the deeper reasoning capabilities of the Pro model for the **stability and speed** of the Flash model, which is a necessary compromise to ensure the bot remains operational during critical incidents.

### Unreliable JSON Responses

**The Challenge:** Getting an LLM to output strict, machine-readable JSON is difficult.

- Even when instructed to output JSON, LLMs generate token by token. Sometimes they include unescaped quote marks inside a message or they stop generating mid-stream. This causes json.loads() to fail with errors like “Unterminated string”.
- LLMs are trained to be helpful assistants, so they often wrap the JSON in Markdown code blocks (json ... ) instead of returning raw JSON.

**The Solution:** Robust Logic in **ai_service.py**

- The code uses the **SDK**'s native **Structured Output** capabilities to maximize the chance of success:
  - **response_mime_type="application/json"**: Explicitly tells the model the output format must be JSON.
  - **response_schema:** Defines the exact fields (customerMessage, internalMessage) so the model knows exactly what keys to generate.
- LLMs often ignore the "raw JSON" instruction and wrap the output in Markdown. This code handles this specifically with **Regular Expression** - this prevents **json.loads()** from failing due to non-JSON characters at the start of the string.
- Since JSON errors are brittle, the code includes extensive logging in the **except block** - this allows developers to see exactly what the AI generated (e.g., a stray quote or a hallucinated character) that broke the parser, making future prompt tuning much easier.

### Database Migration

**SashiDo to Back4App:** Due to connection issues with SashiDo, the database was migrated to **Back4App**. As both platforms use the **Parse Server** standard, the **db_service.py** code was fully reusable.

---

## Future Improvements

Transition from the current HTTP Simulation to a **Fully Integrated Production System (Slack)**

- **Implement Real-Time Event Listening** - connect the bot to live Slack activity (**app_mention events** and **slash command**)
- **Active Bi-Directional Communication** - **Slack Web Client Integration** - the backend should send the generated messages back to the specific Slack channel where the request originated
- **Security: Request Verification** - make sure the **/incident-handler** endpoint only processes requests that are confirmed to come from **Slack**

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

2. Install dependencies:

Install the required Python packages (Flask, Google Generative AI SDK, Requests)

```bash
pip install -r requirements.txt
```

3. Configure Environment Variables

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

4. Run the Server

```bash
python3 run.py
```

You should see the following output indicating the server is running:
 *** Running on http://127.0.0.1:5000 ***