import time
import requests
import json
import csv
import pymysql
import datetime


def get_data(author_id):
    author_id = author_id["a_id"]
    cookies = {
        'CMM_A_C_ID': 'bc5b5d96-fb55-11ec-a840-d2db3ff11dae',
        'LOGIN-TOKEN-FORSNS': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6MTAwMDAsImV4cGlyZV90aW1lIjoxNjU3NDc5NjAwLCJpYXQiOjE2NTY5Mzc2NDcsImlkIjozOTY4ODUxfQ.Tz0UIMXGXpjcY5qKSNputTyl2oUH_zfgPF9BB_NEYuM',
    }

    headers = {
        'authority': 'api-service.chanmama.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.chanmama.com',
        'pragma': 'no-cache',
        'referer': 'https://www.chanmama.com/authorDetail/2384194153219051/live',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-client-id': '276288852',
    }

    params = {
        'author_id': author_id,
    }

    while 1:
        try:
            print("第一个")
            response = requests.get('https://api-service.chanmama.com/v1/author/detail/info', params=params, cookies=cookies,
                                headers=headers)
            data = json.loads(response.text)
            break
        except Exception:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    data = data["data"]

    # 作者id
    authors_id = data["author_id"]

    # 作者名字
    nickname = data["nickname"]

    # 地址
    city = data["city"]

    # 年龄
    birthday = data["birthday"]

    # 性别
    gender = data["gender"]

    # 类别
    tag = data["single_tags"]["first"]

    # 主营类型
    spread_category = data["spread_category"][0]["title"]

    # 粉丝总数
    follower_count = data["follower_count"]

    # 粉丝团总数
    fans_club_total = data["fans_club_total"]


    # ycy 部分：liveOverview
    while 1:
        try:
            print("到第二个了")
            res = requests.get('https://api-service.chanmama.com/v2/author/detail/liveOverview', params=params,
                               cookies=cookies, headers=headers)
            data4 = json.loads(res.text)
            break

        except Exception:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            # continue
            break

    data4 = data4["data"]

    # 直播总数
    total_live_count = data4["total_live_count"]

    # 近30天直播数量
    live_count_30 = data4["live_count_30"]

    # 近30天直播累计销售额
    live_amount_30 = data4["live_amount_30"]

    # 近30天直播累计销量
    live_volume_30 = data4["live_volume_30"]

    # 平均直播时长
    avg_live_time = data4["avg_live_time"]
    #
    # # 写入要查询数据的日期
    paramss = {
        'author_id': author_id,
        'start_date': '2022-05-26',
        'end_date': '2022-06-26',
        'is_contain_today': 'true',
    }
    while 1:
        try:
            print("到第三个了")
            res1 = requests.get('https://api-service.chanmama.com/v1/author/detail/liveAnalysisV2', params=paramss,
                               cookies=cookies, headers=headers)

            data2 = json.loads(res1.text)
            break
        except Exception:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    data2 = data2["data"]["summary"]
    # 带货场次
    live_product_count = data2["live_product_count"]

    # 场均观看
    avg_live_user_count = data2["avg_live_user_count"]

    # 带货转化率
    product_rate = data2["product_rate"]

    # 场均销量
    avg_volume = data2["avg_volume"]

    # 场均销售额
    avg_amount = data2["avg_amount"]

    # 场均UV价值
    avg_uv = data2["avg_uv"]

    # 上架商品数量
    product_size = data2["product_size"]

    # ycy 部分：awemeOverview
    while 1:
        try:
            print("到第四个了")
            res2 = requests.get('https://api-service.chanmama.com/v1/author/detail/awemeOverview', params=params,
                               cookies=cookies, headers=headers)

            data3 = json.loads(res2.text)

            break
        except Exception:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    data3 = data3["data"]
    # 近30天涨粉数量
    follower_incr_30 = data3["follower_incr_30"]

    # 近30天发布视频数目
    aweme_count_30 = data3["aweme_count_30"]

    # 近30天视频平均点赞数量
    avg_digg_count_30 = data3["avg_digg_count_30"]

    # 近30天视频平均播放量
    avg_play_count_30 = data3["avg_play_count_30"]


    # ycy 部分：awemeAnalysis
    while 1:
        try:
            print("到第五个了")
            res3 = requests.get('https://api-service.chanmama.com/v1/author/detail/awemeAnalysis', params=paramss,
                               cookies=cookies, headers=headers)
            data6 = json.loads(res3.text)
            break
        except Exception:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    data6 = data6["data"]

    # 近30天平均视频评论数量
    avg_comment = data6["summary"]["avg_comment"]

    # 近30天平均视频转发数量
    avg_share = data6["summary"]["avg_share"]

    # 近30天平均视频收藏量
    avg_favorited = data6["summary"]["avg_favorited"]


    # 写入要查询观众类别
    paramsss = {
        'author_id': author_id,
        'picture_type': 'room',
    }
    while 1:
        try:
            print("到第六个了")
            # ycy 部分：fanspicture
            res4 = requests.get('https://api-service.chanmama.com/v1/author/detail/fansPicture', params=paramsss,
                               cookies=cookies, headers=headers)
            data5 = json.loads(res4.text)

            break
        except Exception:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    data5 = data5["data"]

    # 直播粉丝女性比例
    gender0 = data5["gender"][0]["rate"]

    # 直播粉丝男性比例
    gender1 = data5["gender"][1]["rate"]

    # 直播粉丝地域分布第一名
    province0 = data5["province"][0]["title"]

    # 直播粉丝地域分布第二名
    province1 = data5["province"][1]["title"]

    # 直播粉丝地域分布第三名
    province2 = data5["province"][2]["title"]

    # 直播粉丝地域分布第四名
    province3 = data5["province"][3]["title"]

    # 直播粉丝地域分布第五名
    province4 = data5["province"][4]["title"]

    # 直播粉丝18-23岁占比
    age0 = data5["age"][0]["rate"]

    # 直播粉丝24-30岁占比
    age1 = data5["age"][1]["rate"]

    # 直播粉丝31-40岁占比
    age2 = data5["age"][2]["rate"]

    # 直播粉丝41-50岁占比
    age3 = data5["age"][3]["rate"]

    # 直播粉丝50岁以上占比
    age4 = data5["age"][4]["rate"]


    # with open('禅妈妈数据.csv', 'a+', encoding='utf-8-sig', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerows([[authors_id, nickname, city, birthday,gender, tag, spread_category, follower_count,fans_club_total, live_product_count, avg_live_user_count, product_rate, avg_volume, avg_amount]])
    sql_1 = "UPDATE cmm SET state = 1 WHERE a_id = %s"
    cursor.execute(sql_1, (author_id))
    conn.commit()

    sql_3 = "INSERT INTO cmm_data(authors_id, nickname, city, birthday, gender, tag, spread_category, follower_count, fans_club_total" \
            ", total_live_count, live_count_30, live_amount_30, live_volume_30, avg_live_time, live_product_count" \
            ", avg_live_user_count, product_rate, avg_volume, avg_amount, avg_uv, product_size, follower_incr_30, aweme_count_30" \
            ", avg_digg_count_30, avg_play_count_30, avg_comment, avg_share, avg_favorited, gender0, gender1" \
            ", province0, province1, province2, province3, province4, age0, age1, age2, age3, age4)" \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql_3,(authors_id, nickname, city, birthday, gender, tag, spread_category, follower_count, fans_club_total
                          , total_live_count, live_count_30, live_amount_30, live_volume_30, avg_live_time, live_product_count
                          , avg_live_user_count, product_rate, avg_volume, avg_amount, avg_uv, product_size, follower_incr_30, aweme_count_30
                          ,avg_digg_count_30, avg_play_count_30, avg_comment, avg_share, avg_favorited, gender0, gender1
                          , province0, province1, province2, province3, province4, age0, age1, age2, age3, age4))
    conn.commit()

def get_author():
    cookies = {
        'CMM_A_C_ID': 'bc5b5d96-fb55-11ec-a840-d2db3ff11dae',
        'LOGIN-TOKEN-FORSNS': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6MTAwMDAsImV4cGlyZV90aW1lIjoxNjU3NDc5NjAwLCJpYXQiOjE2NTY5MjUwNTcsImlkIjozOTY4ODUxfQ.mdKEaKfxLm2L3Hmsv484HFjTbPSN5Ci1ruTdtV2bLJI',
    }

    headers = {
        'authority': 'api-service.chanmama.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.chanmama.com',
        'pragma': 'no-cache',
        'referer': 'https://www.chanmama.com/bloggerRank?keyword=',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="103", "Google Chrome";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-client-id': '3928481475',
    }

    for i in range(1, 101):
        params = {
            'keyword': '',
            'author_type': '1',
            'goods_cat': '',
            'star_category': '',
            'star_sub_category': '',
            'gender': '-1',
            'age': '',
            'province': '',
            'fans_gender': '-1',
            'fans_age': '',
            'fans_province': '',
            'live_price_preference': '',
            'aweme_price_preference': '',
            'live_purchase_intention': '',
            'aweme_purchase_intention': '',
            'follower_count': '',
            'take_product_method': '0',
            'verification_type': '0',
            'author_level': '',
            'is_brand_self_author': '0',
            'is_shop_author': '0',
            'is_star_author': '0',
            'is_low_fans_high_gmv': '0',
            'is_commerce': '0',
            'author_self_play': '0',
            'take_product_level': '',
            'take_product_price': '',
            'reputation_level': '-1',
            'live_watch_count': '',
            'live_average_amount_30_v2': '',
            'gpm': '',
            'digg_count': '',
            'is_ignore_government': '1',
            'contact': '0',
            'similar_author_id': '',
            'page': i,
            'size': '50',
            'sort': 'live_average_amount_30_v2',
            'order_by': 'desc',
            'from': 'detail',
        }

        res = requests.get('https://api-service.chanmama.com/v2/home/author/search', params=params,
                           cookies=cookies, headers=headers)
        data = json.loads(res.text)
        data = data["data"]["list"]
        print("正在爬取中")
        for author in data:
            author_id = author["author_id"]

            sql_2 = "INSERT INTO cmm(a_id,state) VALUES (%s,%s)"
            cursor.execute(sql_2, (author_id, 0))
            conn.commit()

        time.sleep(1)


def write():
    sql = "SELECT * FROM  `cmm_data`;"
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    all_add = cursor.fetchall()
    for data in all_add:
        # 作者id
        authors_id = data["authors_id"]

        # 作者名字
        nickname = data["nickname"]

        # 地址
        city = data["city"]

        # 年龄
        birthday = data["birthday"]

        # 性别
        gender = data["gender"]

        # 类别
        tag = data["tag"]

        # 主营类型
        spread_category = data["spread_category"]

        # 粉丝总数
        follower_count = data["follower_count"]

        # 粉丝团总数
        fans_club_total = data["fans_club_total"]

        # 直播总数
        total_live_count = data["total_live_count"]

        # 近30天直播数量
        live_count_30 = data["live_count_30"]

        # 近30天直播累计销售额
        live_amount_30 = data["live_amount_30"]

        # 近30天直播累计销量
        live_volume_30 = data["live_volume_30"]

        # 平均直播时长
        avg_live_time = data["avg_live_time"]

        # 近30天涨粉数量
        follower_incr_30 = data["follower_incr_30"]

        # 近30天发布视频数目
        aweme_count_30 = data["aweme_count_30"]

        # 近30天视频平均点赞数量
        avg_digg_count_30 = data["avg_digg_count_30"]

        # 近30天视频平均播放量
        avg_play_count_30 = data["avg_play_count_30"]

        # 近30天平均视频评论数量
        avg_comment = data["avg_comment"]

        # 近30天平均视频转发数量
        avg_share = data["avg_share"]

        # 近30天平均视频收藏量
        avg_favorited = data["avg_favorited"]

        # 直播粉丝女性比例
        gender0 = data["gender0"]

        # 直播粉丝男性比例
        gender1 = data["gender1"]

        # 直播粉丝地域分布第一名
        province0 = data["province0"]

        # 直播粉丝地域分布第二名
        province1 = data["province1"]

        # 直播粉丝地域分布第三名
        province2 = data["province2"]

        # 直播粉丝地域分布第四名
        province3 = data["province3"]

        # 直播粉丝地域分布第五名
        province4 = data["province4"]

        # 直播粉丝18-23岁占比
        age0 = data["age0"]

        # 直播粉丝24-30岁占比
        age1 = data["age1"]

        # 直播粉丝31-40岁占比
        age2 = data["age2"]

        # 直播粉丝41-50岁占比
        age3 = data["age3"]

        # 直播粉丝50岁以上占比
        age4 = data["age4"]

        # 带货场次
        live_product_count = data["live_product_count"]

        # 场均观看
        avg_live_user_count = data["avg_live_user_count"]

        # 带货转化率
        product_rate = data["product_rate"]

        # 场均销量
        avg_volume = data["avg_volume"]

        # 场均销售额
        avg_amount = data["avg_amount"]

        # 场均UV价值
        avg_uv = data["avg_uv"]

        # 上架商品数量
        product_size = data["product_size"]

        with open('禅妈妈数据.csv', 'a+', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerows([[authors_id, nickname, city, birthday, gender, tag, spread_category, follower_count, fans_club_total, total_live_count, live_count_30, live_amount_30, live_volume_30, avg_live_time, live_product_count, avg_live_user_count, product_rate, avg_volume,
                            avg_amount, avg_uv, product_size, follower_incr_30, aweme_count_30, avg_digg_count_30, avg_play_count_30, avg_comment, avg_share, avg_favorited, gender0, gender1, province0, province1, province2, province3, province4, age0, age1, age2, age3, age4
                        ]])


if __name__ == '__main__':
    # 打开数据库连接 根据自身数据库修改
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', port=3306, charset='utf8mb4', db='data',
                           cursorclass=pymysql.cursors.DictCursor)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 获取所有主播id
    # get_author()

    # # 查询id 表去获取数据
    # sql = "SELECT a_id FROM  `cmm` as b WHERE b.state = 0;"
    # # # 使用 execute()  方法执行 SQL 查询
    # cursor.execute(sql)
    #
    # all_add = cursor.fetchall()
    # for id in all_add:
    #     print("你正在 ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), " 打印 ", id)
    #     get_data(id)

    # 写入到文件
    with open('禅妈妈数据.csv', 'a+', encoding='utf-8-sig', newline='') as f:
       fieldnames = ['id', "名称", "地址", "年龄", "性别", "类别", "主营类型", "粉丝总数", "粉丝团总数", "直播总数", "近30天直播数量",
       "近30天直播累计销售额", "近30天直播累计销量", "平均直播时长", "带货场次", "场均观看", "带货转化率", "场均销量", "场均销售额", "场均UV价值", "上架商品数量",
       "近30天涨粉数量", "近30天发布视频数目", "近30天视频平均点赞数量", "近30天视频平均播放量", "近30天平均视频评论数量", "近30天平均视频转发数量",
       "近30天平均视频收藏量", "直播粉丝女性比例", "直播粉丝男性比例","直播粉丝地域分布第一名",
       "直播粉丝地域分布第二名", "直播粉丝地域分布第三名", "直播粉丝地域分布第四名", "直播粉丝地域分布第五名"
       , "直播粉丝18-23岁占比", "直播粉丝24-30岁占比", "直播粉丝31-40岁占比", "直播粉丝41-50岁占比", "直播粉丝50岁以上占比"]
       writer_ = csv.DictWriter(f, fieldnames=fieldnames)  # DictWriter以字典形式写入
       writer_.writeheader()
    write()
