from fastapi import FastAPI
import uvicorn
from mylibrary.controllers.llc_controller import router as llc_router
from mylibrary.controllers.bird_controller import router as bird_router
from mylibrary.database.db import Base, sync_engine

app = FastAPI(debug=True)
app.include_router(bird_router)
app.include_router(llc_router)

# Ensure the database tables are created
Base.metadata.create_all(sync_engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    #uvicorn.run(app, host="0.0.0.0", port=8080)
