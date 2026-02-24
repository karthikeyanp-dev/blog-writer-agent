import os
import importlib.util

# Dynamically load the root-level FastAPI app from api.py to avoid package name conflicts
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
API_FILE = os.path.join(ROOT_DIR, "api.py")

spec = importlib.util.spec_from_file_location("api_root", API_FILE)
api_root = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_root)

# Expose FastAPI application for Vercel
app = api_root.app
