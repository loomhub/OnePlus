
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from oneplus.mylibrary.controllers import bankaccount_controller, bankdownload_controller, bird_controller, \
    cashflow_controller, emailConfig_controller, file_upload_download_controller, llc_controller, \
    partner_controller, property_master_controller, rule_controller, sample_controller, \
    tenant_controller, transaction_controller, transaction_type_controller, transactiontmp_controller, \
    transreport_controller

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(bankaccount_controller.router)
app.include_router(bankdownload_controller.router)
app.include_router(bird_controller.router)
app.include_router(cashflow_controller.router)
app.include_router(emailConfig_controller.router)
app.include_router(file_upload_download_controller.router)
app.include_router(llc_controller.router)
app.include_router(partner_controller.router)
app.include_router(property_master_controller.router)
app.include_router(rule_controller.router)
app.include_router(sample_controller.router)
app.include_router(tenant_controller.router)
app.include_router(transaction_controller.router)
app.include_router(transaction_type_controller.router)
app.include_router(transactiontmp_controller.router)
app.include_router(transreport_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to OnePlus Realty API"}
