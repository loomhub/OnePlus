from fastapi import FastAPI
import uvicorn
from mylibrary.controllers.transaction_controller import router as transactions_router
from mylibrary.database.db import Base, engine

app = FastAPI()
app.include_router(transactions_router)

# Ensure the database tables are created
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
