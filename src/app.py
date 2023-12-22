"""
Gemini Dungeon API

Game logic, chat and image generation api for gemini-dungeon frontend
"""
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import json

from geminidm import GeminiDM
from stabilityapi import StabilityAPI

logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

app = Flask(__name__)
CORS(app)

with app.app_context():
    load_dotenv()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.info("Starting GeminiDM module")
    gdm = GeminiDM()

    logger.info("starting stability.ai API")
    sapi = StabilityAPI()

    # start med coder with api start
    dt_run = datetime.now().strftime("%m%d%Y %H:%M:%s")
    logger.info(f"------ Starting Gemini Dungeon API @ {dt_run} ---------")

@app.route("/dmstart", methods=["POST"])
def dmstart():
    """
    Starts the process and creates the first message and image
    """

    user_msg = "Hello"
    reply_dict = {"ai": "", "vision": "", "error": ""}

    caught_exception = False

    try:
        ai_resp = gdm.chat(user_msg=user_msg)
    except Exception as err:
        logger.error(err)
        reply_dict["error"] = "system error"
        reply_dict[
            "ai"
        ] = "I'm sorry but could you state that again? I have seem to caught an error."
        caught_exception = True

    try:
        ai_json = json.loads(ai_resp)
    except json.JSONDecodeError as err:
        logger.error(err)
        reply_dict["error"] = "system error - json failed from AI"
        reply_dict[
            "ai"
        ] = "I'm sorry but could you state that again? I have seem to caught an error."
        caught_exception = True

    try:
        sapi_reply = sapi.generate_image(ai_json["view"])
    except Exception as err:
        logger.error(err)
        reply_dict["error"] = "system error - stability failed"
        reply_dict[
            "ai"
        ] = f"I'm sorry but could not generate you an image.\n{ai_json['content']}"
        caught_exception = True

    if not caught_exception:
        reply_dict["ai"] = ai_json["content"]
        reply_dict["vision"] = sapi_reply["artifacts"][0]["base64"]

    json_reply = jsonify(reply_dict)
    return make_response(json_reply, 200)


@app.route("/run", methods=["POST"])
def run():
    user_msg = request.json["usermsg"]
    reply_dict = {"ai": "", "vision": "", "error": ""}

    try:
        ai_resp = gdm.chat(user_msg=user_msg)
    except Exception as err:
        logger.error(err)
        reply_dict["error"] = "system error"
        json_reply = jsonify(reply_dict)
        return make_response(json_reply, 500)

    print(ai_resp)

    try:
        ai_json = json.loads(ai_resp)
    except json.JSONDecodeError as err:
        logger.error(err)
        reply_dict["error"] = "system error - json failed from AI"
        json_reply = jsonify(reply_dict)
        return make_response(json_reply, 500)

    try:
        sapi_reply = sapi.generate_image(ai_json["view"])
    except Exception as err:
        logger.error(err)
        reply_dict["error"] = "system error - stability failed"
        json_reply = jsonify(reply_dict)
        return make_response(json_reply, 500)

    reply_dict["ai"] = ai_json["content"]
    reply_dict["vision"] = sapi_reply["artifacts"][0]["base64"]
    json_reply = jsonify(reply_dict)
    return make_response(json_reply, 201)

