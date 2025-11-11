from flask import Blueprint, jsonify
from sqlalchemy import text
from models.models import db

bp = Blueprint("status", __name__)

@bp.route("/status", methods=["GET"])
def status():
    """
    Return status of the service
    {
        "service": "ok",
        "database": "ok",
        "tasks": {
            "translate_job": "scheduled",
            "crawler_job": "scheduled"
        }
    }
    """
    # check database status
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # check scheduler status
    from flask import current_app
    tasks_status = {}
    scheduler = getattr(current_app, "scheduler", None)
    if scheduler:
        for job in scheduler.get_jobs():
            next_run = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S") if job.next_run_time else "None"
            tasks_status[job.id] = f"next_run: {next_run}"
    else:
        tasks_status = {"scheduler": "not configured"}

    return jsonify({
        "service": "ok",
        "database": db_status,
        "tasks": tasks_status
    })
