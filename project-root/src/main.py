from src.workflows.orchestrator import run_full_pipeline
from src.database.db_manager import init_db

if __name__ == "__main__":
    init_db()
    run_full_pipeline() 