import time
import requests
import json
import csv
import pymysql
import datetime

def local_time(timestamp):
  #转换成localtime
  time_local = time.localtime(timestamp)
  #转换成新的时间格式(2016-05-05 20:28:54)
  dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
  return dt

def get_data(author_id):
    author_id = author_id["a_id"]
    cookies = {
        'CMM_A_C_ID': '612d7161-0701-11ed-b934-d68f7db8b06b',
        'LOGIN-TOKEN-FORSNS': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6MTAwMDAsImV4cGlyZV90aW1lIjoxNjU5ODEyNDAwLCJpYXQiOjE2NTkyNjQzNjEsImlkIjozOTY4ODUxfQ.HkOtb6USng5FqVaz58wddIfFGVe3Zi3oh1YyB9i1Jdw',
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
        'room_id': author_id,
    }
    #
    while 1:
        try:
            print("第一个")
            response = requests.get('https://api-service.chanmama.com/v1/douyin/live/room/info', params=params, cookies=cookies,
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

    # 达人名称
    nickname = data["author"]["nickname"]

    data = data["room"]

    # 直播间名字
    room_title = data["room_title"]

    # 直播开始时间
    begin_time = local_time(data["begin_time"])

    # 直播时长
    live_duration = data["live_duration"]/3600

    # 观看人次
    watch_cnt = data["watch_cnt"]

    # 上架商品
    product_size = data["product_size"]

    # 发送弹幕数量
    user_peak = data["user_peak"]

    # 本场销量
    volume = data["volume"]

    # 本场销售额
    amount = data["amount"]

    # 涨粉人数
    increment_follower_count = data["increment_follower_count"]

    # 转粉率
    convert_fan_rate = data["convert_fan_rate"]

    # 累计点赞数
    like_count = data["like_count"]

    # 带货转化率
    conversion_rate_percent = data["conversion_rate_percent"]

    # 客单价
    price = data["price"]

    # UV值
    user_value = data["user_value"]

    while 1:
        try:
            print("到第二个了")
            res = requests.get('https://api-service.chanmama.com/v1/douyin/live/room/lottery', params=params,
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

    data4 = data4["data"]["summary"]

    # 福袋累计发放次数
    lottery_times = data4["lottery_times"]

    # 福袋累计发放总数
    lottery_count = data4["lottery_count"]

    # 福袋发放时间间隔
    gap_time = data4["gap_time"]

    # 全场平均停留时长
    all_average_residence_time = data4["all_average_residence_time"]

    # 发放期间平均停留时长
    lottery_average_residence_time = data4["lottery_average_residence_time"]


    while 1:
        try:
            print("到第三个了")
            res2 = requests.get('https://api-service.chanmama.com/v1/douyin/live/room/fans/analysis', params=params,
                               cookies=cookies, headers=headers)

            data5 = json.loads(res2.text)

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
    gender0 = data5["gender"]["female"]

    # 直播粉丝男性比例
    gender1 = data5["gender"]["male"]

    # 直播粉丝地域分布第一名
    if len(data5["province"]) >= 1:
        province0 = data5["province"][0]["title"]
    else:
        province0 = ""

    # 直播粉丝地域分布第二名

    if len(data5["province"]) >= 2:
        province1 = data5["province"][1]["title"]
    else:
        province1 = ""

    # 直播粉丝地域分布第三名
    if len(data5["province"]) >= 3:
        province2 = data5["province"][2]["title"]
    else:
        province2 = ""

    # 直播粉丝地域分布第四名
    if len(data5["province"]) >= 4:
        province3 = data5["province"][3]["title"]
    else:
        province3 = ""

    # 直播粉丝地域分布第五名
    if len(data5["province"]) >= 5:
        province4 = data5["province"][4]["title"]
    else:
        province4 = ""

    # 直播粉丝18-23岁占比
    if len(data5["age"]) == 0:
        age0 = ""
        age1 = ""
        age2 = ""
        age3 = ""
        age4 = ""
    else:
        age0 = data5["age"][0]["rate"]

        # 直播粉丝24-30岁占比
        if len(data5["age"]) >= 2:
            age1 = data5["age"][1]["rate"]
        else:
            age1 = ""

        # 直播粉丝31-40岁占比
        if len(data5["age"]) >= 3:
            age2 = data5["age"][2]["rate"]
        else:
            age2 = ""

        # 直播粉丝41-50岁占比
        if len(data5["age"]) >= 4:
            age3 = data5["age"][3]["rate"]
        else:
            age3 = ""

        # 直播粉丝50岁以上占比
        if len(data5["age"]) >= 5:
            age4 = data5["age"][4]["rate"]
        else:
            age4 = ""

    # 直播观众来源粉丝
    if len(data5["user_source"]) >= 1:
        user_source0 = data5["user_source"][0]["rate"]
    else:
        user_source0 = ""

    # 直播观众来源视频推荐
    if len(data5["user_source"]) >= 2:
        user_source1 = data5["user_source"][1]["rate"]
    else:
        user_source1 = ""

    # 直播观众来源其他
    if len(data5["user_source"]) >= 3:
        user_source2 = data5["user_source"][2]["rate"]
    else:
        user_source2 = ""


    while 1:
        try:
            print("到第四个了")
            res3 = requests.get('https://api-service.chanmama.com/v1/douyin/live/room/words/cloud/detail', params=params,
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

    # 弹幕人数
    barrage_author_count = data6["barrage_author_count"]

    # 观众互动率
    interaction_percent = data6["interaction_percent"]

    sql_1 = "UPDATE cmm_room SET state = 1 WHERE a_id = %s"
    cursor.execute(sql_1, (author_id))
    conn.commit()

    sql_3 = "INSERT INTO cmm_roomdata(nickname, room_title, begin_time, live_duration, watch_cnt, product_size, user_peak, volume" \
            ", amount, increment_follower_count, convert_fan_rate, like_count, conversion_rate_percent, price, user_value" \
            ", lottery_times, lottery_count, gap_time, all_average_residence_time, lottery_average_residence_time " \
            ", user_source0, user_source1,  user_source2, barrage_author_count, interaction_percent" \
            ", gender0, gender1, province0, province1, province2, province3, province4, age0, age1, age2, age3, age4)" \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql_3,(nickname, room_title, begin_time, live_duration, watch_cnt, product_size, user_peak, volume,
                          amount, increment_follower_count, convert_fan_rate, like_count, conversion_rate_percent, price, user_value
                          , lottery_times, lottery_count, gap_time, all_average_residence_time, lottery_average_residence_time
                          , user_source0, user_source1, user_source2, barrage_author_count, interaction_percent
                          , gender0, gender1, province0, province1, province2, province3, province4, age0, age1, age2, age3, age4
                          ))
    conn.commit()


def get_author():
    cookies = {
        'CMM_A_C_ID': '781fa7a9-ff6f-11ec-b934-d68f7db8b06b',
        'LOGIN-TOKEN-FORSNS': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6MTAwMDAsImV4cGlyZV90aW1lIjoxNjU3OTk4MDAwLCJpYXQiOjE2NTc0NTM0OTcsImlkIjo0Njc3MTc5fQ.fd2bt92gKqq356gQbBOg2joAZArYiznyJpdGPnup2tw',
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

    for i in range(1, 5):
        params = {
            'keyword': '',
            'author_type': '1',
            'goods_cat': '美妆护肤',
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
            print("正在爬取中2")

        sql_1 = "UPDATE cmm_room SET state = 1 WHERE a_id = %s"
        cursor.execute(sql_1, (author_id))
        conn.commit()

        time.sleep(1)


def write():
    sql = "SELECT * FROM  `cmm_roomdata`;"
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    all_add = cursor.fetchall()
    for data in all_add:
        # 达人名称
        nickname = data["nickname"]

        # 直播间名字
        room_title = data["room_title"]

        # 直播开始时间
        begin_time = data["begin_time"]

        # 直播时长
        live_duration = data["live_duration"]

        # 观看人次
        watch_cnt = data["watch_cnt"]

        # 上架商品
        product_size = data["product_size"]

        # 发送弹幕数量
        user_peak = data["user_peak"]

        # 本场销量
        volume = data["volume"]

        # 本场销售额
        amount = data["amount"]

        # 涨粉人数
        increment_follower_count = data["increment_follower_count"]

        # 转粉率
        convert_fan_rate = data["convert_fan_rate"]

        # 累计点赞数
        like_count = data["like_count"]

        # 带货转化率
        conversion_rate_percent = data["conversion_rate_percent"]

        # 客单价
        price = data["price"]

        # UV值
        user_value = data["user_value"]

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

        # 直播观众来源粉丝
        user_source0 = data["user_source0"]

        # 直播观众来源视频推荐
        user_source1 = data["user_source1"]

        # 直播观众来源其他
        user_source2 = data["user_source2"]

        # 福袋累计发放次数
        lottery_times = data["lottery_times"]

        # 福袋累计发放总数
        lottery_count = data["lottery_count"]

        # 福袋发放时间间隔
        gap_time = data["gap_time"]

        # 全场平均停留时长
        all_average_residence_time = data["all_average_residence_time"]

        # 发放期间平均停留时长
        lottery_average_residence_time = data["lottery_average_residence_time"]

        # 弹幕人数
        barrage_author_count = data["barrage_author_count"]

        # 观众互动率
        interaction_percent = data["interaction_percent"]

        with open('禅妈妈单场数据.csv', 'a+', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerows([[nickname, room_title, begin_time, live_duration, watch_cnt, product_size, user_peak, volume,
                          amount, increment_follower_count, convert_fan_rate, like_count, conversion_rate_percent, price, user_value
                          , lottery_times, lottery_count, gap_time, all_average_residence_time, lottery_average_residence_time
                          , user_source0, user_source1, user_source2, barrage_author_count, interaction_percent
                          , gender0, gender1, province0, province1, province2, province3, province4, age0, age1, age2, age3, age4]])


if __name__ == '__main__':
    # 打开数据库连接 根据自身数据库修改
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', port=3306, charset='utf8mb4', db='data',
                           cursorclass=pymysql.cursors.DictCursor)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    # 获取所有主播id
    # get_author()


    # 查询id 表去获取数据
    # sql = "SELECT a_id FROM  `cmm_room` as b WHERE b.state = 0;"
    # # # 使用 execute()  方法执行 SQL 查询
    # cursor.execute(sql)
    # #
    # all_add = cursor.fetchall()
    # for id in all_add:
    #     print("你正在 ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), " 打印 ", id)
    #     get_data(id)

    # 写入到文件
    with open('禅妈妈单场数据.csv', 'a+', encoding='utf-8-sig', newline='') as f:
       fieldnames = ["达人名称", "直播间名字", "直播开始时间", "直播时长", "观看人次", "上架商品", "发送弹幕数量",
                     "本场销量", "本场销售额", "涨粉人数", "转粉率", "累计点赞数", "带货转化率", "客单价", "UV值",
                     "福袋累计发放次数", "福袋累计发放总数", "福袋发放时间间隔", "全场平均停留时长", "发放期间平均停留时长",
                     "直播观众来源粉丝", "直播观众来源视频推荐", "直播观众来源其他", "弹幕人数", "观众互动率", "直播粉丝女性比例", "直播粉丝男性比例","直播粉丝地域分布第一名",
                     "直播粉丝地域分布第二名", "直播粉丝地域分布第三名", "直播粉丝地域分布第四名", "直播粉丝地域分布第五名",
                     "直播粉丝18-23岁占比", "直播粉丝24-30岁占比", "直播粉丝31-40岁占比", "直播粉丝41-50岁占比", "直播粉丝50岁以上占比"]
       writer_ = csv.DictWriter(f, fieldnames=fieldnames)  # DictWriter以字典形式写入
       writer_.writeheader()
    write()
