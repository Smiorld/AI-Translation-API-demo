from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from services.openai_service import translate_and_proofread
from models.models import db, Translation

bp = Blueprint("translate", __name__, url_prefix="/api")

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token != current_app.config["API_TOKEN"]:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

@bp.route("/translate", methods=["POST"])
@token_required
def translate():
    data = request.get_json()
    text = data.get("text")
    target = data.get("target", "English")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = translate_and_proofread(text, target)

    # save to database
    translation_entry = Translation(
        original_text=text,
        target_lang=target,
        translated_text=result["translated"],
        proofread_text=result["proofread"]
    )
    db.session.add(translation_entry)
    db.session.commit()

    return jsonify({
        "detected": "auto",  # TODO
        "translated": result["translated"],
        "proofread": result["proofread"]
    })
