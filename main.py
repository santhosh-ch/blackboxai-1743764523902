from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from call_handler import initiate_call
from llm_interface import generate_response
from database import log_call, get_call_logs
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Twilio webhook endpoint
@app.post("/voice")
async def handle_voice(request: Request):
    form_data = await request.form()
    call_sid = form_data.get('CallSid')
    speech_result = form_data.get('SpeechResult', '')

    # Get AI response
    ai_response = generate_response(speech_result)
    
    # Log interaction
    log_call(call_sid, speech_result, ai_response)
    
    return f"""
    <Response>
        <Say voice="woman">{ai_response}</Say>
        <Gather input="speech" action="/voice" method="POST"/>
    </Response>
    """

# API endpoints
@app.post("/call")
async def make_call(phone_number: str):
    try:
        call = initiate_call(phone_number)
        return {"status": "success", "call_sid": call.sid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/logs")
async def get_logs():
    return get_call_logs()

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    with open("index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)