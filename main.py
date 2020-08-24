import json,os,sys

import requests

import const
from point_manager import PointManager

assert len(sys.argv) == 2
response = requests.get(const.URL.format(sys.argv[1]))

game_json = json.loads(response.text)
players = [game_json["player1"], game_json["player2"]]
output = ["{},{},ラリー本数".format(*players)]

pmger = PointManager()
for p,cnt in zip(game_json["getPointPlayer"], game_json["rallyCnt"]):
    pmger.add_point(p)
    score = pmger.get_score()
    output.append("{},{},{}".format(score["p1p"], score["p2p"], cnt))

with open("output/normal.csv", "w") as f:
    f.write("\n".join(output))

with open("output/memo.txt", "w") as f:
    f.write(game_json["memo"])

#  ラリー内容 2シート目
output = []
pmger = PointManager()
for i, p in enumerate(game_json["getPointPlayer"]):
    pmger.add_point(p)
    score = pmger.get_score()
    hits_list = game_json["hitsList"][str(i)]
    head = "{} - {}".format(score["p1p"], score["p2p"])
    output.append(head)

    # ラリー本数
    tmp = ["ラリー回数"]
    cnt = 1
    for i in hits_list["isServe"]:
        if i:
            cnt = 1
        else:
            cnt += 1
        tmp.append(str(cnt))
    output.append(",".join(tmp))

    output.append(",".join(["選手"] + [players[i-1] for i in hits_list["player"]]))

    # 打球位置はサーブかどうかで変わる
    tmp = ["打球位置"]
    for isServe, hitPosition in zip(hits_list["isServe"], hits_list["hitPosition"]):
        if isServe:
            tmp.append(const.hitPostionAtServe[hitPosition])
        else:
            tmp.append(const.hitPostion[hitPosition])
    output.append(",".join(tmp))

    output.append(",".join(["フォアorバック"] + [const.handList[i] for i in hits_list["hand"]]))
    
    tmp = ["打法"]
    for isServe, hitStyle in zip(hits_list["isServe"], hits_list["hitStyle"]):
        if isServe:
            tmp.append(const.serveList[hitStyle])
        else:
            tmp.append(const.hitsStyleList[hitStyle])
    output.append(",".join(tmp))

    output.append(",".join(["コース"] + [const.courseList[i] for i in hits_list["course"]]))

    output.append(",".join(["インorアウト"] + ["イン" if i else "アウト" for i in hits_list["inOut"]]))

    # インのときとアウトのときで変わる
    tmp = ["その他"]
    for i in range(len(hits_list["inOutDetail"])-1):
        tmp.append(const.inList[hits_list["inOutDetail"][i]])
    tmp.append(const.outList[hits_list["inOutDetail"][-1]])
    output.append(",".join(tmp))
    output.append("")

with open("output/detail.csv", "w") as f:
    f.write("\n".join(output))

