import os
from os.path import join, getsize
import pandas as pd

from app.models import Game_comment, Game_info

games_dir = "supergames/games/"
icon_dir = "supergames/icons/"
link_url = "http://h5-games.ldd.webeyeug.com.cn"


def view_games():
    """ 以列表的形式返回所有的游戏
    """
    default_json = {
      "id": "22042110",
      "name": "Cake Design",
      "desc": "",
      "tags": "",
      "thumb": "/assets/images/icon/Cake-Design-220601.jpg",
      "link": "https://www.funkernel.com/games/Cake-Design-220421/",
      "details": "",
      "play": "",
      "is_landscape": 1
    }
    games = os.listdir(games_dir)
    icon_names = _get_icons()
    game_comments = _get_comments()
    game_infos = _get_details()
    subdir_sizes = _get_subdir_size_bydu(games_dir)

    rows = []
    for idx, game in enumerate(games):
        if game.startswith("."):
            continue
        tmp_game = default_json.copy()
        tmp_game.update({
            "id": "0000" + str(idx + 1),
            "name": game,
            "thumb": "%s/icons/%s" % (link_url, icon_names[game]) if game in icon_names.keys() else "-",
            "link": "%s/games/%s/" % (link_url, game),
            "comments": game_comments.get(game, []),
            "size": subdir_sizes.get(game)
            # "size": _get_dir_size(dir=games_dir + game)
        })
        tmp_game.update(game_infos.get(game, {}))
        rows.append(tmp_game)
    return rows


def _get_icons():
    files = os.listdir(icon_dir)
    icon_names = {os.path.splitext(x)[0]: x for x in files if x.endswith((".jpg", ".png"))}
    return icon_names


def _get_comments():
    results = Game_comment.query.all()
    comment_rows = [dict(game_name=x.game_name, game_comment=x.game_comment) for x in results]
    comments_df = pd.DataFrame(comment_rows)
    comments = {}
    for game_name, subDf in comments_df.groupby(by="game_name"):
        comments[game_name] = subDf["game_comment"].tolist()

    return comments


def _get_details():
    results = Game_info.query.all()
    details = {x.game_name: dict(
        id=x.game_id,
        game_name=x.game_name,
        desc=x.desc,
        details=x.details,
        play=x.play,
        tags=x.tags,
        is_landscape=x.is_landscape
    ) for x in results}
    return details


# 大小转换函数
def _handle_size(size):
    b = 1
    kb = b * 1024
    mb = kb * 1024
    gb = mb * 1024
    tb = gb * 1024
    if size >= tb:
        return "%.2f TB" % float(size / tb)
    if size >= gb:
        return "%.2f GB" % float(size / gb)
    if size >= mb:
        return "%.2f MB" % float(size / mb)
    if size >= kb:
        return "%.2f KB" % float(size / kb)
    if size < kb:
        return "%.2f Byte" % float(size)


def _get_dir_size(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return _handle_size(size)


def _get_subdir_size_bydu(dir, depth=1):
    # 获取以及目录下的文件夹大小
    res_list = os.popen(f'du {dir} -h --max-depth={depth}')
    """ simple data
    ['2.3\tsupergames/games/Blow-Up-Jellies-220210\n',
    '3.7M\tsupergames/games/Funny-Faces-220421\n']
    """
    res_list = [x.split('\t') for x in res_list]

    subdir_sizes = {
        x[1].split('/')[-1].strip('\n'): x[0]
        for x in res_list
    }
    return subdir_sizes


def save_icon(icon_obj, file_name):
    try:
        upload_path = icon_dir + file_name + ".png"
        icon_obj.save(upload_path)
        return True, ""
    except Exception as e:
        return False, e.__str__()
