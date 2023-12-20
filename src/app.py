"""
Gemini Dungeon API

Game logic, chat and image generation api for gemini-dungeon frontend
"""
from datetime import datetime

from flask import Flask, request, jsonify, make_response

from flask_cors import CORS

from dndlibrary import DNDLibrary

import logging

logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

app = Flask(__name__)
CORS(app)


@app.route("/run", methods=["POST"])
def run():
    try:
        # logging.info("Setting up DND library")
        # dndlib = DNDLibrary()
        # dndlib.run()

        logger.info("Starting DM Gemini")

    except Exception as err:
        logger.error(err)
        raise

    json_reply = jsonify({"ai": "test", "vision": "asvbcds"})
    return make_response(json_reply, 201)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # start med coder with api start
    dt_run = datetime.now().strftime("%m%d%Y %H:%M:%s")
    logger.info(f"------ Starting Gemini Dungeon API @ {dt_run} ---------")
    app.run(host="0.0.0.0", port=8080)
