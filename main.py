from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

def get_swapi_url(endpoint, search_term):
    swapi_url = f'https://swapi.dev/api/{endpoint}/'
    if search_term:
        swapi_url += f'?search={search_term}'

    response = requests.get(swapi_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from SWAPI")

@app.get("/ships")
async def get_starships(search: str = None):
    response = get_swapi_url("starships", search)
    return JSONResponse(content=response)

@app.get("/characters")
async def get_people(search: str = None):
    response = get_swapi_url("people", search)
    return JSONResponse(content=response)

@app.get("/")
async def home():
    api_list = {
        "_welcome_note": "Star Wars API Wrapper from SWAPI. Use the available APIs to access information about Star Wars starships and characters.",
        "available_apis": {
            "/ships": "Access information about Star Wars starships. Use the 'search' query parameter to filter results.",
            "/characters": "Access information about Star Wars characters. Use the 'search' query parameter to filter results.",
            "/": "Home page listing all available APIs.",
        "search_query": "Use the 'search' query parameter to filter results based on the name of the starship or character."
        }
    }
    return JSONResponse(content=api_list)

@app.get("/{path:path}")
async def catch_all(path: str):
    return JSONResponse(content={"message": "Not active API"}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
