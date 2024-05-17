"""
Gemini Dungeon API

Game logic, chat and image generation api for gemini-dungeon frontend
"""
from datetime import datetime
from flask import Flask, request, jsonify, make_response, redirect
from flask_cors import CORS
import logging
import json
import os
import uuid

from dotenv import load_dotenv
load_dotenv()

from geminidm import GeminiDM
from stabilityapi import StabilityAPI
from player import Player

from models import db
from models.player import Player as PlayerModel
from models.player_session import PlayerSessions

logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("gdm_server")
logger.setLevel(logging.DEBUG)

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
    # db.create_all()

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

def generate_content(user_msg: str="Hello", session_id: str=None, player: Player=None) -> str:
    """
    Generate AI text and image from user_msg, if any
    """
    reply_dict = {
        "role_name": "",
        "ai": "", 
        "vision": "", 
        "error": "",
        "player_stats": "",
        "player_items": ""
    }
    caught_exception = False

    try:
        logger.info(f"Starting session [{session_id}]")
        ai_resp = gdm.chat(
            user_msg=user_msg,
            session_id=session_id,
            player=player
        )
    except Exception as err:
        logger.error(f"generate_content err 1: {err}")
        reply_dict["error"] = "system error"
        reply_dict["ai"] = "I'm sorry but could you state that again? I have seem to caught an error."
        caught_exception = True

    if not caught_exception:
        try:
            if "```json" in ai_resp:
                logger.info("MARKDOWN detected in AI json reponse. Removing")
                ai_resp = ai_resp.replace("```json", "").replace("```", "")
            ai_json = json.loads(ai_resp)
        except json.JSONDecodeError as err:
            logger.error(f"generate_content err 2: {err}")
            reply_dict["error"] = "system error - json failed from AI"
            reply_dict["ai"] = "I'm sorry but could you state that again? I have seem to caught an error."
            reply_dict["session_id"] = gdm.session_id
            caught_exception = True

    if not caught_exception:
        try:
            logger.info(f"[image prompt] {ai_json['view']}")
            sapi_reply = sapi.generate_image(ai_json["view"])
        except Exception as err:
            logger.error(f"generate_content err 3: {err}")
            reply_dict["error"] = "system error - stability failed"
            reply_dict["ai"] = ai_json['content']
            reply_dict["session_id"] = gdm.session_id
            caught_exception = True

    if not caught_exception:
        reply_dict["role_name"] = ai_json["role_name"]
        reply_dict["ai"] = ai_json["content"]
        reply_dict["session_id"] = gdm.session_id

        if len(sapi_reply["artifacts"]) > 0:
            reply_dict["vision"] = sapi_reply["artifacts"][0]["base64"]
        else:
            reply_dict["error"] = f"sapi artifact out of range: {sapi_reply}"
            logger.error(f"{reply_dict}")
        
        reply_dict["player_stats"] = ai_json["player_stats"]
        reply_dict["player_items"] = ai_json["player_items"]
            
    return reply_dict


@app.route("/dmstart", methods=["POST"])
def dmstart():
    """
    Start DM chat session, starts the adventure and creates the first message and image
    """

    # create and save new session id
    new_session_id = str(uuid.uuid4()).replace("-", "")

    # create new player
    player_obj = Player()

    # save player information to database
    print(f"\n---Saving player\n\n{str(player_obj)}\n")
    new_player = PlayerModel(
        first_name=player_obj.player_first_name,
        last_name=player_obj.player_last_name,
        char_class=player_obj.player_class,
        race=player_obj.dndc.race,
        alignment=player_obj.dndc.alignment,
        level=player_obj.dndc.level,
        hit_points=player_obj.dndc.current_hp,
        gender=player_obj.dndc.gender,
        description=player_obj.dndc.description,
        background=player_obj.dndc.background,
        strength=player_obj.dndc.strength,
        dexterity=player_obj.dndc.dexterity,
        constitution=player_obj.dndc.constitution,
        intelligence=player_obj.dndc.intelligence,
        wisdom=player_obj.dndc.wisdom,
        charisma=player_obj.dndc.charisma,
        age=player_obj.dndc.age
    )

    db.session.add(new_player)
    db.session.commit()

    # save session information to database
    player_session = PlayerSessions(
        session_id=new_session_id,
        player_id=new_player.id
    )

    db.session.add(player_session)
    db.session.commit()

    try:
        # generate a player session id
        reply_dict = generate_content(
            user_msg="Hello, please introduce me to the campaign, current area, who you are and other information.",
            session_id=new_session_id,
            player=player_obj
        )
    except Exception as err:
        logger.error(f"reply_dict generation failed: {err}")
        return make_response(
            jsonify({"error": "content generation failed", "type": 0}),
            400
        )
    
    log_info = {
        "from": f"dmstart",
        "user": "Hello, please introduce me to the campaign, current area, who you are and other information.",
        "role_name": reply_dict["role_name"],
        "ai": reply_dict["ai"],
        "vision": len(reply_dict["vision"]),
        "dm": gdm.dm_id,
        "session": reply_dict["session_id"],
        "player_stats": reply_dict["player_stats"],
        "player_items": reply_dict["player_items"]
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
        logger.error("no session id found")
        return make_response(
            jsonify({"error": "no session id found", "type": 0}),
            400
        )
    
    # check if valid session_id
    session_query = PlayerSessions.query.filter_by(session_id=session_id).first()
    if not session_query:
        logger.error("no session id found")
        return make_response(
            jsonify({"error": "no session id found", "type": 0}),
            400
        )

    # get player information from session id
    player_query = PlayerModel.query.filter_by(id=session_query.player_id).first()
    player = Player(
        first_name=player_query.first_name,
        last_name=player_query.last_name,
        char_class=player_query.char_class,
        race=player_query.race,
        alignment=player_query.alignment,
        level=player_query.level,
        hit_points=player_query.hit_points,
        strength=player_query.strength,
        dexterity=player_query.dexterity,
        constitution=player_query.constitution,
        intelligence=player_query.intelligence,
        wisdom=player_query.wisdom,
        charisma=player_query.charisma,
        age=player_query.age,
        gender=player_query.gender,
        background=player_query.background,
        description=player_query.description
    )

    reply_dict = generate_content(user_msg, session_id, player)
    json_reply = jsonify(reply_dict)

    # check if player needs to be updated
    update_player = False

    if "action" in reply_dict:
        logger.info(f"Action called: {reply_dict['action']}")

    if "player_stats" in reply_dict:
        player.update_player(reply_dict["player_stats"])
        update_player = True

    if "player_items" in reply_dict:
        player.update_items(reply_dict["player_items"])
        update_player = True

    if update_player:
        try:
            db.session.commit()
        except Exception as err:
            logger.error(f"updating play db info error: {err}")
        
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

