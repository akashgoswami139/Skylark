# Skylark

A weather and city guide powered by a tool-calling AI agent. Type a city, pick a mode, and get a live answer in an animated single-page UI.

- **Weather mode:** shows the weather of a city, and the background changes to match it (sun rays, rain, thunderstorm, snow, fog, clouds).
- **Know a city mode:** shows a short guide to the city with location, history, attractions, food and travel tips.

The agent only answers these two things. Anything else is refused.

## How it works

```
Browser (city + mode)
  -> app.py        FastAPI endpoint, validates the city
  -> prompt.py     builds the request and the strict system prompt
  -> agent.py      Groq model (gpt-oss-20b) with LangChain tool calling
  -> tools.py      get_weather / city_details fetch the real data
  -> browser       renders the markdown answer and the weather scene
```

## Project structure

```
skylark/
├── app.py             FastAPI server, serves the UI and /api/agent
├── agent.py           Agent class (LLM + tools)
├── tools.py           get_weather and city_details tools
├── prompt.py          system prompt, city validation, request builder
├── index.html         the whole UI (HTML, CSS and JS in one file)
├── requirements.txt
└── .env               your secret keys (not committed)
```

## Setup

1. Clone the repo and open the folder.

2. Create a virtual environment and install the packages:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project folder:

   ```
   GROQ_API_KEY=your_groq_api_key
   ```

   If `tools.py` uses another service for weather or city data, add its key here too.

4. Start the server:

   ```bash
   uvicorn app:app --reload
   ```

5. Open http://127.0.0.1:8000 in your browser. Do not open `index.html` by double-clicking it, because the page needs the server.

## API

`POST /api/agent`

```json
{ "city": "Raipur", "mode": "weather" }
```

`mode` is `"weather"` or `"city"`. The response is:

```json
{ "answer": "markdown text from the agent" }
```

An invalid city name returns `I couldn't find a city with that name.` without calling the model.

## Customising

- **City suggestions:** edit the `CITIES` list in `index.html`.
- **Agent behaviour and answer format:** edit `SYSTEM_PROMPT` in `prompt.py`.
- **Model:** change the `model` name in `agent.py`.

## Troubleshooting

- **"Could not get an answer" on the page:** check the terminal running `uvicorn` for the real error. A missing `GROQ_API_KEY` or an import error in `tools.py` is the usual cause.
- **`ModuleNotFoundError`:** run `pip install -r requirements.txt` inside your virtual environment.
- **No weather animation:** the scene is chosen from the words in the answer, so it needs a condition like "rain" or "sunny" and a temperature in °C.

## Developer

Built by **Akash Goswami**, final-year BE student specialising in AI and machine learning.
