from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from models.models import db, CrawledText, Translation
from api.translate import bp as translate_bp
from api.translation_scheduler import bp as translation_scheduler_bp  
from api.status import bp as status_bp
from services.openai_service import translate_and_proofread
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from services.fake_crawler import fake_crawl
from services.scheduler_service import execute_translation_tasks

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

# initlaize blueprints
app.register_blueprint(translate_bp, url_prefix="/api")
app.register_blueprint(translation_scheduler_bp, url_prefix="/api") 
app.register_blueprint(status_bp, url_prefix="/api")

# initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(execute_translation_tasks(app), "interval", minutes=5, id="translate_job")
scheduler.add_job(fake_crawl(app), "interval", minutes=30, id="fake_crawler_job")
scheduler.start()
setattr(app, "scheduler", scheduler) # app.scheduler = scheduler  the same, only to suppress warning


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translation_scheduler")
def translation_scheduler_page():
    return render_template("scheduler_translation.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # reset processing tasks
        db.session.query(CrawledText).filter_by(status="processing").update({"status": "new"}, synchronize_session=False)
        db.session.commit()
    app.run(host="0.0.0.0", port=5001)
    
    
