from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def api():
    return jsonify({"status": "OK"}, 200)
