from fastapi import FastAPI
import uvicorn
from mylibrary.controllers.bird_controller import router as bird_router
from mylibrary.controllers.emailConfig_controller import router as emailConfig_router
from mylibrary.controllers.llc_controller import router as llc_router
from mylibrary.controllers.property_master_controller import router as propertyMaster_router
from mylibrary.controllers.bankaccount_controller import router as bankaccount_router
from mylibrary.controllers.cashflow_controller import router as cashflow_router
from mylibrary.controllers.partner_controller import router as partner_router
from mylibrary.controllers.tenant_controller import router as tenant_router
from mylibrary.controllers.transaction_type_controller import router as transactionType_router
from mylibrary.controllers.transaction_controller import router as transaction_router
from mylibrary.controllers.transactiontmp_controller import router as transactiontmp_router
from mylibrary.controllers.rule_controller import router as rule_router
from mylibrary.controllers.bankdownload_controller import router as bankdownload_router
from mylibrary.controllers.file_upload_download_controller import router as upload_download_router

from mylibrary.database.db import Base, sync_engine

app = FastAPI(debug=True)
app.include_router(bird_router)
app.include_router(emailConfig_router)
app.include_router(llc_router)
app.include_router(propertyMaster_router)
app.include_router(bankaccount_router)
app.include_router(cashflow_router)
app.include_router(partner_router)
#app.include_router(customer_router)
app.include_router(tenant_router)
app.include_router(transactionType_router)
app.include_router(transaction_router)
app.include_router(transactiontmp_router)
app.include_router(rule_router)
app.include_router(bankdownload_router)
app.include_router(upload_download_router)


# Ensure the database tables are created
Base.metadata.create_all(sync_engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    #uvicorn.run(app, host="0.0.0.0", port=8080)
