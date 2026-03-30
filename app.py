from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
import asyncio

from scheduler import smart_call
from cache import get_cache, set_cache

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
async def ui():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Aggregator API</title>
        <style>
            body { font-family: Inter, sans-serif; background: #0a0a0b; color: #fff; padding: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #f7931a; }
            textarea { width: 100%; padding: 12px; background: #141418; color: #fff; border: 1px solid #1f1f24; border-radius: 8px; font-size: 14px; }
            button { background: #f7931a; color: #000; padding: 12px 24px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 12px; }
            button:hover { background: #fbbf24; }
            pre { background: #141418; padding: 16px; border-radius: 8px; overflow-x: auto; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Aggregator API</h1>
            <p>Multi-model scheduling with caching & streaming</p>
            <textarea id='q' rows='6' placeholder='Ask anything...'></textarea><br>
            <button onclick='send()'>Send</button>
            <button onclick='stream()' style='margin-left:8px;background:#3b82f6'>Stream</button>
            <pre id='res'></pre>
        </div>
        <script>
        async function send(){
            let q=document.getElementById('q').value;
            if(!q) return;
            document.getElementById('res').innerText='Loading...';
            try {
                let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:q})});
                let data=await res.json();
                document.getElementById('res').innerText=JSON.stringify(data,null,2);
            } catch(e) {
                document.getElementById('res').innerText='Error: '+e.message;
            }
        }
        async function stream(){
            let q=document.getElementById('q').value;
            if(!q) return;
            document.getElementById('res').innerText='Streaming...';
            try {
                let res=await fetch('/stream',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:q})});
                let text=await res.text();
                document.getElementById('res').innerText=text;
            } catch(e) {
                document.getElementById('res').innerText='Error: '+e.message;
            }
        }
        </script>
    </body>
    </html>
    """)

@app.post("/chat")
async def chat(req: ChatRequest):
    cached = get_cache(req.prompt)
    if cached:
        return {"cached": True, **cached}

    result = await smart_call(req.prompt)
    set_cache(req.prompt, result)
    return result

@app.post("/stream")
async def stream(req: ChatRequest):
    async def generator():
        result = await smart_call(req.prompt)
        text = str(result)
        for i in range(0, len(text), 20):
            yield text[i:i+20]
            await asyncio.sleep(0.05)

    return StreamingResponse(generator(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
