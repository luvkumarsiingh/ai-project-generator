import pathlib
import subprocess
from typing import Tuple
import shlex #to parse strings to tokens for subprocess
from langchain_core.tools import tool

BASE_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR / "generated_project"

def safe_path_for_project(path: str) -> pathlib.Path:
    p = (PROJECT_ROOT / path).resolve()
    root = PROJECT_ROOT.resolve()

    if not str(p).startswith(str(root)):
        raise ValueError("Attempt to write outside project root")

    return p

@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    try:
        p = safe_path_for_project(path)
        p.parent.mkdir(parents=True, exist_ok=True)

        with open(p, "w", encoding="utf-8") as f:
            f.write(content)

        return f"WROTE:{p}"
    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    if not p.exists():
        return f"ERROR: {p} does not exist"
    
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(PROJECT_ROOT)


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = safe_path_for_project(directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.rglob("*") if f.is_file()]
    return "\n".join(files) if files else "No files found."


@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30):
    
    """
    Executes a shell command in the project directory and returns
    (return_code, stdout, stderr).
    """
    
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT

    try:
        res = subprocess.run(
            shlex.split(cmd),
            cwd=str(cwd_dir),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)


def init_project_root():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)