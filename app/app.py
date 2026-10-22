"""Task tracker API. Small Flask app used for the workshop challenges."""
from flask import Flask, abort, jsonify, request

from app.config import data_file
from app.errors import register_error_handlers
from app.storage import TaskStore


def create_app():
    app = Flask(__name__)
    store = TaskStore(data_file())
    # Challenge 1: the helpers in app/errors.py were written but never wired.
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/tasks")
    def list_tasks():
        # Backlog level 1: the store already filters; the route never asked.
        status = request.args.get("status")
        if status is not None and status not in ("open", "completed"):
            abort(400, description="status must be 'open' or 'completed'")
        return jsonify(store.list_tasks(status=status))

    @app.post("/tasks")
    def create_task():
        # Challenge 1: reject bad input instead of crashing with a 500.
        payload = request.get_json(silent=True) or {}
        title = payload.get("title")
        if not isinstance(title, str) or not title.strip():
            abort(400, description="title is required and must be a non-empty string")
        priority = payload.get("priority", 1)
        if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 5:
            abort(400, description="priority must be an integer between 1 and 5")
        task = store.create_task(title=title, priority=priority)
        return jsonify(task), 201

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        task = store.get_task(task_id)
        if task is None:
            return jsonify({"error": "not_found"}), 404
        return jsonify(task)

    @app.patch("/tasks/<int:task_id>/complete")
    def complete_task(task_id):
        task = store.complete_task(task_id)
        if task is None:
            return jsonify({"error": "not_found"}), 404
        return jsonify(task)

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        if store.delete_task(task_id):
            return jsonify({"deleted": task_id})
        return jsonify({"error": "not_found"}), 404

    return app
