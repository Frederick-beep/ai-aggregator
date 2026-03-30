from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
import asyncio

from scheduler import smart_call, call_deepseek, call_gemini, call_openrouter, call_groq
from scheduler import deepseek_pool, gemini_pool, openrouter_pool, groq_pool
from cache import get_cache, set_cache

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    model: str = "auto"

@app.get("/")
async def ui():
    return HTMLResponse("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Aggregator API</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,system-ui,sans-serif;background:#0a0a0b;color:#fff;min-height:100vh;display:flex;flex-direction:column}
.header{background:#0f0f11;border-bottom:1px solid #1f1f24;padding:20px 32px;display:flex;align-items:center;gap:16px}
.logo{font-size:1.5em;font-weight:800;background:linear-gradient(135deg,#f7931a,#fbbf24);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.badge{background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);color:#10b981;padding:4px 12px;border-radius:20px;font-size:0.75em;font-weight:600}
.main{flex:1;max-width:900px;margin:0 auto;padding:32px 24px;width:100%}
.card{background:#141418;border:1px solid #1f1f24;border-radius:16px;padding:24px;margin-bottom:20px}
.card h2{font-size:1em;font-weight:600;color:#a0a0a8;margin-bottom:16px;text-transform:uppercase;letter-spacing:0.05em}
.model-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin-bottom:20px}
.model-btn{background:#1a1a1f;border:1px solid #1f1f24;color:#a0a0a8;padding:12px 16px;border-radius:10px;cursor:pointer;font-size:0.85em;font-weight:500;transition:all .2s;text-align:left}
.model-btn:hover{border-color:#f7931a;color:#fff}
.model-btn.active{background:rgba(247,147,26,0.1);border-color:#f7931a;color:#f7931a}
.model-btn .m-name{font-weight:600;display:block}
.model-btn .m-tag{font-size:0.7em;color:#6b6b73;margin-top:2px}
textarea{width:100%;background:#1a1a1f;border:1px solid #1f1f24;color:#fff;padding:16px;border-radius:10px;font-size:0.95em;resize:vertical;font-family:inherit;outline:none;transition:border .2s}
textarea:focus{border-color:#f7931a}
.btn-row{display:flex;gap:10px;margin-top:12px}
.btn{padding:12px 24px;border:none;border-radius:10px;font-weight:600;cursor:pointer;font-size:0.9em;transition:all .2s}
.btn-primary{background:#f7931a;color:#000}
.btn-primary:hover{background:#fbbf24}
.btn-stream{background:#3b82f6;color:#fff}
.btn-stream:hover{background:#2563eb}
.btn-clear{background:#1a1a1f;color:#a0a0a8;border:1px solid #1f1f24}
.btn-clear:hover{background:#1f1f24}
.response{background:#0f0f11;border:1px solid #1f1f24;border-radius:10px;padding:16px;margin-top:16px;min-height:120px;font-size:0.9em;line-height:1.6;white-space:pre-wrap;word-break:break-word;color:#e0e0e0}
.status{display:flex;align-items:center;gap:8px;font-size:0.8em;color:#6b6b73;margin-top:8px}
.dot{width:8px;height:8px;border-radius:50%;background:#6b6b73}
.dot.loading{background:#f7931a;animation:pulse 1s infinite}
.dot.ok{background:#10b981}
.dot.err{background:#ef4444}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
.api-card{background:#0f0f11;border:1px solid #1f1f24;border-radius:10px;padding:16px}
.api-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #1f1f24;font-size:0.85em}
.api-row:last-child{border-bottom:none}
.api-name{font-weight:600}
.api-status{padding:3px 10px;border-radius:10px;font-size:0.75em;font-weight:600}
.api-ok{background:rgba(16,185,129,0.15);color:#10b981}
.api-na{background:rgba(107,107,115,0.15);color:#6b6b73}
</style>
</head>
<body>
<div class="header">
<div class="logo">🤖 AI Aggregator</div>
<div class="badge">LIVE</div>
</div>
<div class="main">
<div class="card">
<h2>Select Model</h2>
<div class="model-grid">
<button class="model-btn active" onclick="selectModel('auto',this)"><span class="m-name">⚡ Auto</span><span class="m-tag">Smart routing</span></button>
<button class="model-btn" onclick="selectModel('deepseek',this)"><span class="m-name">🔵 DeepSeek</span><span class="m-tag">deepseek-chat</span></button>
<button class="model-btn" onclick="selectModel('gemini',this)"><span class="m-name">🟣 Gemini</span><span class="m-tag">gemini-pro</span></button>
<button class="model-btn" onclick="selectModel('openrouter',this)"><span class="m-name">🟠 OpenRouter</span><span class="m-tag">Llama 3.1 8B</span></button>
<button class="model-btn" onclick="selectModel('groq',this)"><span class="m-name">🟢 Groq</span><span class="m-tag">Llama3 70B</span></button>
</div>
<textarea id="q" rows="5" placeholder="Ask anything..."></textarea>
<div class="btn-row">
<button class="btn btn-primary" onclick="send()">Send</button>
<button class="btn btn-stream" onclick="stream()">Stream</button>
<button class="btn btn-clear" onclick="clear()">Clear</button>
</div>
<div class="status"><span class="dot" id="dot"></span><span id="statusText">Ready</span></div>
<div class="response" id="res">Response will appear here...</div>
</div>
<div class="card">
<h2>API Status</h2>
<div class="api-card">
<div class="api-row"><span class="api-name">🔵 DeepSeek</span><span class="api-status api-ok">Active</span></div>
<div class="api-row"><span class="api-name">🟣 Gemini</span><span class="api-status api-ok">Active</span></div>
<div class="api-row"><span class="api-name">🟠 OpenRouter</span><span class="api-status api-ok">Active</span></div>
<div class="api-row"><span class="api-name">🟢 Groq</span><span class="api-status api-na">No Key</span></div>
<div class="api-row"><span class="api-name">🔴 Together</span><span class="api-status api-na">No Key</span></div>
</div>
</div>
<div class="card">
<h2>API Endpoints</h2>
<div class="api-card">
<div class="api-row"><span class="api-name">POST /chat</span><span style="color:#a0a0a8;font-size:0.8em">{"prompt":"...", "model":"auto|deepseek|gemini|openrouter|groq"}</span></div>
<div class="api-row"><span class="api-name">POST /stream</span><span style="color:#a0a0a8;font-size:0.8em">Streaming response</span></div>
</div>
</div>
</div>
<script>
let selectedModel='auto';
function selectModel(m,btn){
    selectedModel=m;
    document.querySelectorAll('.model-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
}
function setStatus(state,text){
    const dot=document.getElementById('dot');
    dot.className='dot '+(state==='loading'?'loading':state==='ok'?'ok':'err');
    document.getElementById('statusText').textContent=text;
}
async function send(){
    const q=document.getElementById('q').value.trim();
    if(!q)return;
    setStatus('loading','Sending...');
    document.getElementById('res').textContent='Loading...';
    try{
        const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:q,model:selectedModel})});
        const d=await r.json();
        // 提取文本内容
        let text=JSON.stringify(d,null,2);
        if(d.choices&&d.choices[0]&&d.choices[0].message){
            text=d.choices[0].message.content;
        }else if(d.candidates&&d.candidates[0]&&d.candidates[0].content){
            text=d.candidates[0].content.parts[0].text;
        }
        document.getElementById('res').textContent=text;
        setStatus('ok','Done');
    }catch(e){
        document.getElementById('res').textContent='Error: '+e.message;
        setStatus('err','Error');
    }
}
async function stream(){
    const q=document.getElementById('q').value.trim();
    if(!q)return;
    setStatus('loading','Streaming...');
    document.getElementById('res').textContent='';
    try{
        const r=await fetch('/stream',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:q,model:selectedModel})});
        const reader=r.body.getReader();
        const decoder=new TextDecoder();
        while(true){
            const{done,value}=await reader.read();
            if(done)break;
            document.getElementById('res').textContent+=decoder.decode(value);
        }
        setStatus('ok','Done');
    }catch(e){
        document.getElementById('res').textContent='Error: '+e.message;
        setStatus('err','Error');
    }
}
function clear(){
    document.getElementById('q').value='';
    document.getElementById('res').textContent='Response will appear here...';
    setStatus('','Ready');
}
document.getElementById('q').addEventListener('keydown',e=>{if(e.ctrlKey&&e.key==='Enter')send();});
</script>
</body>
</html>""")

@app.post("/chat")
async def chat(req: ChatRequest):
    cached = get_cache(req.prompt + req.model)
    if cached:
        return cached

    result = await dispatch(req.prompt, req.model)
    set_cache(req.prompt + req.model, result)
    return result

@app.post("/stream")
async def stream(req: ChatRequest):
    async def generator():
        result = await dispatch(req.prompt, req.model)
        # 提取文本
        text = ""
        if isinstance(result, dict):
            if "choices" in result and result["choices"]:
                text = result["choices"][0].get("message", {}).get("content", "")
            elif "candidates" in result and result["candidates"]:
                text = result["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
            else:
                text = str(result)
        else:
            text = str(result)
        
        for i in range(0, len(text), 20):
            yield text[i:i+20]
            await asyncio.sleep(0.03)

    return StreamingResponse(generator(), media_type="text/plain")

async def dispatch(prompt, model):
    try:
        if model == "deepseek":
            key = deepseek_pool.get()
            if key:
                return await call_deepseek(prompt, key)
        elif model == "gemini":
            key = gemini_pool.get()
            if key:
                return await call_gemini(prompt, key)
        elif model == "openrouter":
            key = openrouter_pool.get()
            if key:
                return await call_openrouter(prompt, key)
        elif model == "groq":
            key = groq_pool.get()
            if key:
                return await call_groq(prompt, key)
        # auto 或 fallback
        return await smart_call(prompt)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
