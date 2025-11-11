from flask import Blueprint, request, jsonify, current_app
from services.scheduler_service import execute_translation_tasks
from apscheduler.schedulers.background import BackgroundScheduler
from functools import wraps
import os

bp = Blueprint("translation_scheduler", __name__)

# Token auth
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token != os.getenv("API_TOKEN"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@bp.route("/translation_scheduler/config", methods=["POST"])
@require_auth
def config_scheduler():
    data = request.get_json()
    interval = int(data.get("interval", 10))
    scheduler: BackgroundScheduler = getattr(current_app, "scheduler")

    try:
        scheduler.remove_job("translate_job")
    except:
        pass
    scheduler.add_job(
        execute_translation_tasks(current_app),
        "interval",
        minutes=interval,
        id="translate_job"
    )
    return jsonify({"status": "ok", "interval": interval})

@bp.route("/translation_scheduler/run_now", methods=["POST"])
@require_auth
def run_now():
    try:
        job = execute_translation_tasks(current_app)
        job()
        return jsonify({"status": "ok", "message": "execute translation task successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
