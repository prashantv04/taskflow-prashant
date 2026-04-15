from fastapi import FastAPI

from app.api.routes import auth, projects, tasks

app = FastAPI(title="TaskFlow API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, tags=["Tasks"])

@app.get("/")
def root():
    return {"message": "TaskFlow API running"}