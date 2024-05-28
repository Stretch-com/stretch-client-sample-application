from fastapi import FastAPI
from availability import router as availability_router
from booking import router as booking_router
from client import router as client_router
from category import router as category_router
from search import router as search_router
from vendor import router as vendor_router

app = FastAPI()
# app.include_router(client_router)
app.include_router(category_router)
app.include_router(search_router)
app.include_router(vendor_router)
app.include_router(availability_router)
app.include_router(booking_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
