from predict import predict 

from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
import os
from fastapi import FastAPI
app = FastAPI()

# app.add_middleware(
#     CORSMiddleware, 
#     allow_origins = origins,
#     allow_credentials = True,
#     allow_methods = methods,
#     allow_headers = headers    
# )

@app.post("/")
async def process_list(my_list: dict):
    data = my_list["list"]

    # Assuming the input is a JSON object with a "list" key containing the list
    input_list = data

    # Perform any processing on the list if needed

    return {"result": predict(input_list)}

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 8000))
	run(app, host="0.0.0.0", port=port)