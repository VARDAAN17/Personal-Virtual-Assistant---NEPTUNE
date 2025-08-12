from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from openai import OpenAI
api_key = ""
if not api_key:
    raise ValueError("API key not found. Set OPENAI_API_KEY as an environment variable.")
client = OpenAI(api_key=api_key)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from serpapi import GoogleSearch
import json, uuid
from pprint import pprint
from datetime import datetime


app = FastAPI(reload=True)

templates = Jinja2Templates(directory="app/templates")
DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWORD = 'admin'
SERP_API_KEYS = ['   ','   ']
SERPAPI_API_KEY = SERP_API_KEYS[1]
AI_MODEL = 'gpt-4o-mini'
MEMORY_FILE = 'chat_memory.json'

try:
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    memory = []

def append_to_memory(data):
    global memory
    # Assign an incremental order column
    data['order'] = len(memory) + 1
    memory.append(data)
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=4)

def clean_memory_file():
    global memory
    memory = sorted(memory, key=lambda x: x['order'])[-3:]
    updated_memory = []
    for i, data in enumerate(memory):
        data['order'] = i + 1
        updated_memory.append(data)

    updated_memory = [i for n, i in enumerate(updated_memory) if i['user_messege'] not in [j['user_messege'] for j in updated_memory[:n]]]

    with open(MEMORY_FILE, 'w') as f:
        json.dump(updated_memory, f, indent=4)

def summarize_memory():
    global memory
    if len(memory) == 0:
        return
    
    user_messages = [i['user_messege'] for i in sorted(memory, key=lambda x: x['order'])[-2:]]
    summary = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes user messages. If in any case user is don't wanted to focus on specific area, just remove that context from summarization."},
            {"role": "user", "content": '\n'.join(user_messages)}
        ],
        temperature=0.0
    )
    summary_message = summary.choices[0].message.content
    memory[-1]['user_messege'] = summary_message
    
    append_to_memory(memory[-1])
    clean_memory_file()


@app.get("/memory")
def read_memory():
    return JSONResponse(content=memory, media_type="application/json")


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):

    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def verify_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
        return RedirectResponse(url="/chat", status_code=302)
    else:
        return HTMLResponse("<h1>Invalid username or password.</h1>")

@app.get('/chat', response_class=HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


def get_openai_response(prompt):
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
    recent_messages = '\n'.join([i['user_messege'] for i in memory[-2:]])
    memory_str = recent_messages if recent_messages else ''

    return client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"""You are Neptune, a helpful assistant for "
                    "Real time book flights, search for jobs and latest news. Use emojis, return HTML (and tables) "
                    "if data is requested, and embed any links as <a> tags.,Also additonaly here is the user recent messege context summarization to understand what user is looking for context: {memory_str}"""
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        stream=True,
    )

def get_openai_response_for_flights(prompt):
    return client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Neptune, a helpful personal assistant for flights booking information. "
                    "Data is provided in json format, use that data and desing proper html design for chat reponse and include flights information and do include the images if available."
                    "Also include the price of the flight and the duration of the flight in the response."
                    "Don't limit the response to only flights information, include other details as well."
                    "Also don't show limited flights show all the flights or minimum 5 flights."
                    "Also if there is way to provide direct link to book flight create anchor tag with target='_blank' for that, so anyone can click and redirect there"

                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        stream=True,
    )

def get_openai_response_for_jobs(prompt):
    return client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Neptune, a helpful personal assistant for jobs. "
                    "Data is provided in json format, use that data and desing proper html design for chat reponse and include jobs information and do include the images if available."
                    "Also include the job title and the job description in the response."
                    "Don't limit the response to only job information, include other details as well."
                    "Also don't show limited jobs show all the jobs or minimum 5 jobs."
                    "Also if there is way to provide direct link to apply for job create anchor tag with target='_blank' for that, so anyone can click and redirect there"

                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        stream=True,
    )

def get_openai_response_for_news(prompt):
    return client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Neptune, a helpful personal assistant for news. "
                    "Data is provided in json format, use that data and desing proper html design for chat reponse and include news information and do include the images if available."
                    "Also include the news title and the news description in the response."
                    "Don't limit the response to only news information, include other details as well."
                    "Also don't show limited news show all the news or minimum 5 news."
                    "Also if there is way to provide direct link to read news create anchor tag with target='_blank' for that, so anyone can click and redirect there"

                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        stream=True,
    )


parse_context_function = {
    "name": "parse_context",
    "description": "Extract user intent and any flight-booking details into a strict JSON format.",
    "parameters": {
        "type": "object",
        "properties": {
            "context_type": {
                "type": "string",
                "enum": ["flight", "missing_flight_information", "general_chat", "jobs", "news"]
            },
            "data": {
                "type": "object",
                "properties": {
                    "departure_id": {"type": "string"},
                    "arrival_id": {"type": "string"},
                    "outbound_date": {
                        "type": "string",
                        "format": "date"
                    },
                    "return_date": {
                        "type": ["string", "null"],
                        "format": "date"
                    },
                    "message": {"type": "string"}
                },
                "required": []
            },
            "jobs": {
                "job_search_text": {"type": "string"}
            },
            "news":{
                "news_search_text": {"type": "string"}
            }
        },
        "required": ["context_type", "data"]
    }
}

def understand_user_message_context(prompt: str) -> dict:

    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
    recent_messages = '\n'.join([i['user_messege'] for i in memory[-5:]])
    memory_str = recent_messages if recent_messages else ''

    resp = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"""You are Neptune.  Your sole job here is to read the user's message "
                    "and output *only* a JSON object matching the `parse_context` schema.  "
                    "No extra keys, no prose.  "
                    "If they clearly want to search for news use `context_type` to `news` and echo back their search text under `data.news_search_text`"
                    "If they clearly want to search for job use `context_type` to `jobs` and echo back their search text under `data.job_search_text`"
                    "If they clearly want to book a flight and you have departure, arrival, and in departure and arrival you have to add code like for Amritsar it's ATQ and dubai i's DXB so use your own knowledge to fill this codes"
                    "outbound_date (YYYY-MM-DD), and optional return_date, set `context_type` to "
                    "`flight`.  "
                    "If they ask for flights but are missing any of those fields, use "
                    "`missing_flight_information` and response back what information is missing "
                    "Otherwise, set `context_type` to `general_chat` and echo back their "
                    "message under `data.message`.  additonally for a context we do have a user previous messege context here is the context: {memory_str}"""
                )
            },
            {"role": "user", "content": prompt}
        ],
        functions=[parse_context_function],
        function_call={"name": "parse_context"},
        temperature=0
    )

    arg_str = resp.choices[0].message.function_call.arguments
    return json.loads(arg_str)



def search_flights(departure_id: str, arrival_id: str, outbound_date: str, return_date: str = None):
    """Fetch flight options from Google Flights."""
    params = {
        "engine": "google_flights",
        "departure_id":departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "INR",
        "hl": "en",
        "api_key": SERPAPI_API_KEY,
        
    }
    if return_date:
        params["return_date"] = return_date
    return GoogleSearch(params).get_dict()


def search_jobs(job_search_text: str):
    params = {
        "engine": "google_jobs",
        "q": job_search_text,
        "hl": "en",
        "api_key": SERPAPI_API_KEY,
    }

    return GoogleSearch(params).get_dict()


def search_news(query: str):
    params = {
        "engine": "google_news",
        "q": query,
        "gl": "us",
        "hl": "en",
        "api_key": SERPAPI_API_KEY,
    }
    return GoogleSearch(params).get_dict()

class ChatMessage(BaseModel):
    message: str


@app.post("/chat_endpoint", response_class=StreamingResponse)
async def chat_endpoint(chat_message: ChatMessage):
    user_message = chat_message.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message not provided")
    
    append_to_memory({
        "user_messege": user_message,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uuid": uuid.uuid4().hex
    })
    summarize_memory()

    # build module to understand the trigger code and return the response
    understand_messege_response = understand_user_message_context(user_message)
    if understand_messege_response['context_type'] == 'flight':
        dep = understand_messege_response['data']['departure_id']
        arr = understand_messege_response['data']['arrival_id']
        dep_date = understand_messege_response['data']['outbound_date']
        ret_date = understand_messege_response['data']['outbound_date']
        flights_data = search_flights(dep, arr, dep_date, ret_date)
        flight_ai_response = get_openai_response_for_flights(str(flights_data))
        def generate_flight_data():
            try:
                for chunk in flight_ai_response:
                    delta = chunk.choices[0].delta
                    if delta and hasattr(delta, "content") and delta.content:
                        yield delta.content
            except Exception as e:
                yield f"\nError: {e}"
        return StreamingResponse(generate_flight_data(), media_type="text/html")
    

    if understand_messege_response['context_type'] == 'missing_flight_information':
        def dummy_response():
            messege = "You have to provide all the information to book a flight, Please provide all the information like Departure airport, Arrival airport, Departure date, Return date"
            for i in messege:
                yield i
        return StreamingResponse(dummy_response(), media_type="text/html")
    
    if understand_messege_response['context_type'] == 'jobs':
        job_search_text = understand_messege_response['data']['job_search_text']
        jobs_data = search_jobs(job_search_text)
        jobs_ai_response = get_openai_response_for_jobs(str(jobs_data))
        def generate_jobs_data():
            try:
                for chunk in jobs_ai_response:
                    delta = chunk.choices[0].delta
                    if delta and hasattr(delta, "content") and delta.content:
                        yield delta.content
            except Exception as e:
                yield f"\nError: {e}"
        return StreamingResponse(generate_jobs_data(), media_type="text/html")

    if understand_messege_response['context_type'] == 'news':
        news_search_text = understand_messege_response['data']['news_search_text']
        news_data = search_news(news_search_text)
        news_ai_response = get_openai_response_for_news(str(news_data))
        def generate_news_data():
            try:
                for chunk in news_ai_response:
                    delta = chunk.choices[0].delta
                    if delta and hasattr(delta, "content") and delta.content:
                        yield delta.content
            except Exception as e:
                yield f"\nError: {e}"
        return StreamingResponse(generate_news_data(), media_type="text/html")



    response_stream = get_openai_response(user_message)

    def generate():
        try:
            for chunk in response_stream:
                delta = chunk.choices[0].delta
                if delta and hasattr(delta, "content") and delta.content:
                    yield delta.content
        except Exception as e:
            yield f"\nError: {e}"

    return StreamingResponse(generate(), media_type="text/html")
