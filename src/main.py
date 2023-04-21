from fastapi import FastAPI

app = FastAPI()

# Importing routes for users and organizations
from routes import user, organization

# Including routes
app.include_router(user.router)
app.include_router(organization.router)
