"""
Gemini Dungeon API

Game logic, chat and image generation api for gemini-dungeon frontend
"""
from datetime import datetime
from flask import Flask, request, jsonify, make_response, Response
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import json
import uuid

from geminidm import GeminiDM
from stabilityapi import StabilityAPI

from models import db

logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

app = Flask(__name__)
# db.init_app(app)
CORS(app)
sapi = None
gdm = None

with app.app_context():
    load_dotenv()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if not sapi:
        logger.info("starting stability.ai API")
        sapi = StabilityAPI()
    
    if not gdm:
        # start DM
        logger.info(f"starting gemini dm")
        gdm = GeminiDM()
        logger.info(f"New DM - {gdm.dm_id}")

    # start with api start
    dt_run = datetime.now().strftime("%m%d%Y %H:%M:%s")
    logger.info(f"------ Starting Gemini Dungeon API @ {dt_run} ---------")

def generate_content(user_msg: str="Hello", session_id: str=None) -> dict:
    """
    Generate AI text and image from user_msg, if any
    """
    reply_dict = {"ai": "", "vision": "", "error": ""}
    caught_exception = False

    try:
        ai_resp = gdm.chat(user_msg=user_msg, session_id=session_id)
    except Exception as err:
        logger.error(err)
        reply_dict["error"] = "system error"
        reply_dict["ai"] = "I'm sorry but could you state that again? I have seem to caught an error."
        caught_exception = True

    if not caught_exception:
        try:
            ai_json = json.loads(ai_resp)
        except json.JSONDecodeError as err:
            logger.error(err)
            reply_dict["error"] = "system error - json failed from AI"
            reply_dict["ai"] = "I'm sorry but could you state that again? I have seem to caught an error."
            caught_exception = True

    if not caught_exception:
        try:
            logger.info(f"[image prompt] {ai_json['view']}")
            sapi_reply = sapi.generate_image(ai_json["view"])
        except Exception as err:
            logger.error(err)
            reply_dict["error"] = "system error - stability failed"
            reply_dict["ai"] = ai_json['content']
            caught_exception = True

    if not caught_exception:
        reply_dict["ai"] = ai_json["content"]
        reply_dict["vision"] = sapi_reply["artifacts"][0]["base64"]
        reply_dict["session_id"] = gdm.session_id

    return reply_dict


@app.route("/dmstart", methods=["POST"])
def dmstart():
    """
    Start DM chat session, starts the adventure and creates the first message and image
    """

    # generate a player session id
    reply_dict = generate_content()
    
    # give initial player stats
    reply_dict["player_stats"] = gdm.player.player_info()
    
    log_info = {
        "from": f"dmstart",
        "user": "Hello",
        "ai": reply_dict["ai"],
        "vision": len(reply_dict["vision"]),
        "dm": gdm.dm_id,
        "session": reply_dict["session_id"]
    }

    for i, v in log_info.items():
        logger.info(f"- {i}: {v}")

    json_reply = jsonify(reply_dict)
    return make_response(json_reply, 200)


@app.route("/run", methods=["POST"])
def run():
    user_msg = request.json["usermsg"]
    session_id = request.json["session_id"]

    if session_id == "" or session_id is None:
        return make_response(
            jsonify({"error": "no session id found"}),
            500
        )

    reply_dict = generate_content(user_msg, session_id)
    
    json_reply = jsonify(reply_dict)

    logger.info({
        "from": f"run",
        "user": user_msg,
        "ai": reply_dict["ai"],
        "vision": len(reply_dict["vision"]),
        "dm": gdm.dm_id,
        "session": reply_dict["session_id"]
    })

    return make_response(json_reply, 200)

# @app.route("/playerstats", methods=["POST"])
# def playerstats():
#     return make_response(
#         jsonify(gdm.player.player_info()),
#         200
#     )

