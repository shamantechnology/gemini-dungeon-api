"""
Gemini Dungeon API

Game logic, chat and image generation api for gemini-dungeon frontend
"""
from datetime import datetime
from flask import Flask, request, jsonify, make_response, Response
from flask_cors import CORS
import logging
import json
import os

from dotenv import load_dotenv
load_dotenv()

from geminidm import GeminiDM
from stabilityapi import StabilityAPI
from player import Player

from models import db
from models.player import Player as PlayerModel
from models.player_session import PlayerSession

logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

app = Flask(__name__)
CORS(app)

# setup db
connection_url = f"{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASS']}"
connection_url += f"@{os.environ['MYSQL_HOST']}/{os.environ['MYSQL_DB']}"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{connection_url}"
db.init_app(app)

sapi = None
gdm = None

with app.app_context():
    # run this to initially create database
    # will create a python script to run this
    db.create_all()

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

def generate_content(user_msg: str="Hello", session_id: str=None, player: any=None) -> dict:
    """
    Generate AI text and image from user_msg, if any
    """
    reply_dict = {"ai": "", "vision": "", "error": ""}
    caught_exception = False

    try:
        if session_id and player:
            logger.info(f"Starting session [{session_id}]")
            ai_resp = gdm.chat(user_msg=user_msg, session_id=session_id, player=player)
        else:
            logger.info("No session_id or player, starting a new session")
            ai_resp = gdm.chat(user_msg=user_msg)
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
            reply_dict["session_id"] = gdm.session_id
            caught_exception = True

    if not caught_exception:
        try:
            logger.info(f"[image prompt] {ai_json['view']}")
            sapi_reply = sapi.generate_image(ai_json["view"])
        except Exception as err:
            logger.error(err)
            reply_dict["error"] = "system error - stability failed"
            reply_dict["ai"] = ai_json['content']
            reply_dict["session_id"] = gdm.session_id
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

    # save player information
    player = PlayerModel(
        first_name=gdm.player.player_first_name,
        last_name=gdm.player.player_last_name,
        char_class=gdm.player.player_class,
        race=gdm.player.race,
        alignment=gdm.player.alignment,
        level=gdm.player.level,
        hit_points=gdm.player.current_hp,
        gender=gdm.player.gender,
        description=gdm.player.description,
        background=gdm.player.background,
        strength=gdm.player.strength,
        dexterity=gdm.player.dexterity,
        constitution=gdm.player.constitution,
        intelligence=gdm.player.intelligence,
        wisdom=gdm.player.wisdom,
        charisma=gdm.player.charisma,
        age=gdm.player.age
    )

    db.session.add(player)
    db.session.commit()

    # save session information
    player_session = PlayerSession(
        session_id=reply_dict["session_id"],
        player_id=player.id
    )

    db.session.add(player_session)
    db.session.commit()
    
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

    # get player information from session id
    player_query = PlayerModel.query.filter_by(session_id=session_id).first()
    player = Player(
        first_name=player_query.first_name
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

