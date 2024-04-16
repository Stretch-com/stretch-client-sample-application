from fastapi import FastAPI
from fastapi.openapi.models import Response
from generate_template import GenerateTemplateUseCase
from web_client import WebClient


app = FastAPI()
generate_template = GenerateTemplateUseCase()
web_client = WebClient()

@app.get("/create/client/form", response_class=Response)
async def create_client_form():
    return generate_template.execute("client_form.html")

@app.post("/create/client", response_class=Response)
async def create_client():
    return web_client



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
