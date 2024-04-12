from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.transaction_service import TransactionService
from ..database.db import get_db  # Assume you have a function to get DB session
from ..dtos.transaction_dto import TransactionDTO, TransactionCreate
from ..repositories.transaction_repository import TransactionRepository
  # Import the TransactionRepository class

router = APIRouter()

@router.get(
        "/",
        summary="Welcome message",
        description="Welcome message for the Oneplus API.",
        status_code=200,
        tags=["Root"],
        )
async def root():
    return {"message": "Welcome to Oneplus API!"}

@router.get(
        "/hello/",
        summary="Welcome message",
        description="Welcome message for the Oneplus API.",
        status_code=200,
        tags=["Root"],
        )
async def root():
    return {"message": "Welcome to Oneplus API!"}


@router.post(
        "/transactions/",
        summary="Add transactions",
        description="Add transactions to the database.",
        status_code=200,
        tags=["Add Data"],
        response_model=TransactionDTO,
        )
def add_transaction(
        transaction: TransactionCreate,
        db: Session = Depends(get_db),
):
    try:
        print("Endpoint hit")
        transaction_repository = TransactionRepository(db)
        transaction_service = TransactionService(transaction_repository)
        return transaction_service.create_transaction(db=db, transaction=transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transactions/upload/")
def upload_transactions_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if file.content_type not in [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
    ]:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    TransactionService.load_transactions_from_excel(db, file)

    return {"message": "Transactions successfully loaded."}


@router.get("/transactions/{transaction_id}", response_model=TransactionDTO)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction_repository = TransactionRepository(db)
    transaction_service = TransactionService(transaction_repository)
    return transaction_service.get_transaction(transaction_id)
