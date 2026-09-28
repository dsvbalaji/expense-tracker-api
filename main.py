from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from models import Expense
from database import expenses_collection
from bson import ObjectId

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}


@app.post("/expenses")
def add_expense(expense: Expense):
    expense_data = expense.model_dump()
    expense_data["date"] = expense_data["date"].isoformat()

    result = expenses_collection.insert_one(expense_data)

    return {
        "message": "Expense added successfully",
        "id": str(result.inserted_id)
    }

@app.get("/expenses")
def get_expenses(
    category: str | None = None,
    month: str | None = None
):
    query = {}

    if category:
        query["category"] = category

    if month:
        query["date"] = {
            "$regex": f"^{month}"
        }

    expenses = list(expenses_collection.find(query))

    for expense in expenses:
        expense["id"] = str(expense["_id"])
        del expense["_id"]

    return expenses

@app.get("/expenses/total")
def get_total(category: str | None = None):
    match_stage = {}

    if category:
        match_stage["category"] = category

    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": None,
                "total": {"$sum": "$amount"}
            }
        }
    ]

    result = list(expenses_collection.aggregate(pipeline))

    if not result:
        total = 0
    else:
        total = result[0]["total"]

    return {
        "category": category,
        "total": total
    }

@app.get("/expenses/{id}")
def get_expense(id: str):
    expense = expenses_collection.find_one({"_id": ObjectId(id)})

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense["id"] = str(expense["_id"])
    del expense["_id"]

    return expense

@app.put("/expenses/{id}")
def update_expense(id: str, expense: Expense):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    expense_data = expense.model_dump()
    expense_data["date"] = expense_data["date"].isoformat()

    result = expenses_collection.update_one(
        {"_id": object_id},
        {"$set": expense_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {
        "message": "Expense updated successfully"
    }

@app.delete("/expenses/{id}")
def delete_expense(id: str):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    result = expenses_collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {
        "message": "Expense deleted successfully"
    }

