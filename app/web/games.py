import logging

from flask import request
from flask_login import login_required

from app import db
from app.common.games import view_games, save_icon
from app.common.utils import make_success_result, make_result
from app.models import Game_comment, Game_info
from app.web import h5_game

logger = logging.getLogger(__name__)


@h5_game.route('/test_api/<key>', methods=['GET'])
def test_api(key):
    return make_success_result(data={"key": key})


@h5_game.route('/get_games', methods=['GET'])
def get_games():
    game_list = view_games()
    logger.info(f"get games success! {game_list[:3]}")
    return make_success_result(data={"game_list": game_list})


@h5_game.route('/game_comment/get/<game_name>', methods=['GET'])
def get_comments(game_name):
    results = Game_comment.query.filter(Game_comment.game_name == game_name).all()
    game_comments = [x.game_comment for x in results]

    logger.info(f"get game_comments success! {game_comments}")
    return make_success_result(
        data={
            "game_name": game_name,
            "game_comments": game_comments})


@h5_game.route('/game_comment/add', methods=['POST'])
def add_comment():
    request_data = request.get_json()
    logger.info(f"add data {request_data}")
    game_name = request_data.get("game_name")
    comment = request_data.get("comment")

    # 如果 评论为空就不保存
    if not comment:
        return make_result(code=201, msg="comment is ''",
                           data={
                               "game_name": game_name,
                               "result": f"add comment failed"
                           })

    game_comment = Game_comment(game_name=game_name, game_comment=comment)

    db.session.add(game_comment)
    db.session.commit()
    logger.info(f"add game_comment success! {game_name}: '{comment}'")
    return make_success_result(
        data={
            "game_name": game_name,
            "game_comment": comment,
            "result": f"add comment success"})


@h5_game.route('/game_details/get/<game_name>', methods=['GET'])
def get_details(game_name):
    game_info = Game_info.query.filter_by(game_name=game_name).first()
    if game_info is None:
        game_info = Game_info(game_name=game_name)
        db.session.add(game_info)
        db.session.commit()

    # 评论信息
    results = Game_comment.query.filter(Game_comment.game_name == game_name).all()
    game_comments = [x.game_comment for x in results]

    game_details = dict(
        game_id=game_info.game_id,
        game_name=game_info.game_name,
        desc=game_info.desc,
        play=game_info.play,
        details=game_info.details,
        tags=game_info.tags,
        is_landscape=game_info.is_landscape,
        comments=game_comments
    )

    logger.info(f"get game_details success! {game_details}")
    return make_success_result(
        data={
            "game_name": game_name,
            "game_details": game_details})


@h5_game.route('/game_details/update', methods=['POST'])
def add_and_update_details():
    game_details = request.get_json()
    logger.info(f"add or update game details {game_details}")
    game_name = game_details.pop("game_name")
    game_info = Game_info.query.filter_by(game_name=game_name).first()
    if game_info is None:
        game_info = Game_info(game_name=game_name)
        db.session.add(game_info)
        db.session.commit()

    # 修改字段
    for k, v in game_details.items():
        setattr(game_info, k, v)
    db.session.commit()

    logger.info(f"add game details success! {game_name}: '{game_details}'")
    return make_success_result(
        data={
            "game_name": game_name,
            "game_details": game_details,
            "result": f"update game details success"})


@h5_game.route('/game_icon/upload/<game_name>', methods=['POST'])
def upload_icon(game_name):
    if 'icon' in request.files:
        icon_obj = request.files['icon']
        res, msg = save_icon(icon_obj, game_name)
    else:
        res, msg = False, "Not find icon file."
    if res:
        return make_success_result(
            data={
                "game_name": game_name,
                "result": f"add or update icon success"})
    else:
        return make_result(code=201, msg=msg,
                           data={
                               "game_name": game_name,
                               "result": f"add or update icon failed"
                           })


