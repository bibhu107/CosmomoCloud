from fastapi import FastAPI

from src.routers import user, organization

app = FastAPI()

# Including routes
app.include_router(user.router)
app.include_router(organization.router)
