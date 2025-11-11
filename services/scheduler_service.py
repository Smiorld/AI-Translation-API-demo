from models.models import CrawledText, Translation, db
from services.openai_service import translate_and_proofread
from datetime import datetime

def execute_translation_tasks(app):
    def job():
        with app.app_context():
            tasks = CrawledText.query.filter_by(status="new").order_by(CrawledText.timestamp).all()
            for task in tasks:
                task.status = "processing"
                db.session.commit()

                result = translate_and_proofread(task.content, "English")
                if result["translated"] == "" or result["proofread"] == "":
                    with open("output.txt", "a", encoding="utf-8") as f:
                        f.write(f"[{datetime.now()}] Translation task failed, gonna skip this pack of task.\nSource: {task.source}\nOriginal: {task.content}\n\n")
                        task.status = "new" # reset
                        db.session.commit()
                    return None
                translation_entry = Translation(
                    original_text=task.content,
                    target_lang="English",
                    translated_text=result["translated"],
                    proofread_text=result["proofread"],
                    crawled_text_id=task.id
                )
                db.session.add(translation_entry)

                task.status = "done"
                db.session.commit()

                with open("output.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] Translation task execueted successfully\nSource: {task.source}\nOriginal: {task.content}\nTranslated: {result['translated']}\nProofread: {result['proofread']}\n\n")

    return job