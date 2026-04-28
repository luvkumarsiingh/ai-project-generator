from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from graph import app as agent
from sqlalchemy import create_engine, text
import os
import shutil
import uuid
from datetime import datetime
from dotenv import load_dotenv

# -------------------------
# Load ENV
# -------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# PostgreSQL engine (Render requires SSL)
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)

app = FastAPI()

# -------------------------
# CORS (for React frontend)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Ensure folders exist
# -------------------------
os.makedirs("generated_projects", exist_ok=True)
os.makedirs("generated_project", exist_ok=True)

# -------------------------
# Static Preview
# -------------------------
app.mount("/preview", StaticFiles(directory="generated_projects"), name="preview")

# -------------------------
# Request model
# -------------------------
class Request(BaseModel):
    prompt: str

# -------------------------
# Routes
# -------------------------
@app.get("/")
def home():
    return {"message": "AI Builder API running 🚀"}


@app.post("/generate")
def generate(req: Request):
    try:
        # Step 1: generate project
        agent.invoke({
            "user_prompt": req.prompt.strip()
        })

        # Step 2: create unique ID
        project_id = str(uuid.uuid4())

        # Step 3: new folder path
        new_path = f"generated_projects/{project_id}"

        # Step 4: move generated files
        if os.path.exists(new_path):
            shutil.rmtree(new_path)

        shutil.move("generated_project", new_path)

        # recreate base folder
        os.makedirs("generated_project", exist_ok=True)

        # Step 5: save to DB
        save_project(
            project_id=project_id,
            name=req.prompt[:30],
            prompt=req.prompt,
            tech_stack=["HTML", "CSS", "JS"],
            path=new_path
        )

        return {"status": "done", "project_id": project_id}

    except Exception as e:
        print("ERROR:", e)
        return {"status": "error", "message": str(e)}


@app.get("/projects")
def get_projects():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT * FROM projects ORDER BY created_at DESC"
        ))

        return [
            {
                "id": row[0],
                "name": row[1],
                "prompt": row[2],
                "tech_stack": row[3].split(","),
                "created_at": row[4],
                "path": row[5]
            }
            for row in result
        ]


@app.get("/download/{project_id}")
def download_project(project_id: str):
    folder_path = f"generated_projects/{project_id}"

    if not os.path.exists(folder_path):
        return {"error": "Project not found"}

    zip_path = f"{folder_path}.zip"

    if os.path.exists(zip_path):
        os.remove(zip_path)

    shutil.make_archive(folder_path, 'zip', folder_path)

    return FileResponse(zip_path, filename=f"{project_id}.zip")


# -------------------------
# DB Save Function
# -------------------------
def save_project(project_id, name, prompt, tech_stack, path):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT,
                prompt TEXT,
                tech_stack TEXT,
                created_at TEXT,
                path TEXT
            )
        """))

        conn.execute(text("""
            INSERT INTO projects VALUES (:id, :name, :prompt, :tech, :created, :path)
        """), {
            "id": project_id,
            "name": name,
            "prompt": prompt,
            "tech": ",".join(tech_stack),
            "created": datetime.now().isoformat(),
            "path": path
        })

        conn.commit()