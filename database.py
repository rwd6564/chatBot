
import sqlite3


# 총 이용자수 카운트
def count_user():
    con = sqlite3.connect('C:/Users/58454/PycharmProjects/webScrap/webScrap.db')
    cur = con.cursor()
    cur.execute("select count(*) from user")
    result = cur.fetchone()
    con.close()
    return int(*result)


# 알림받기중인 아티스트 정보 select
def select_artist_list(id):
    con = sqlite3.connect('C:/Users/58454/PycharmProjects/webScrap/webScrap.db')
    cur = con.cursor()
    cur.execute("select artist_list from user where id = ?", (id,))
    result = cur.fetchone()
    data = str(*result)
    #data = data.split('/')
    con.close()
    return data


# 지원하는 아티스트인지 select
def select_artist_YN(realname):
    con = sqlite3.connect('C:/Users/58454/PycharmProjects/webScrap/webScrap.db')
    cur = con.cursor()
    cur.execute("select count(realname) from artist where realname =  ?", (realname,))
    result = cur.fetchone()
    data = str(*result)
    con.close()
    return data



# 사용자정보 insert
def insert_user(id):
    try:
        con = sqlite3.connect('C:/Users/58454/PycharmProjects/webScrap/webScrap.db')
        cur = con.cursor()
        cur.execute("insert into user values(?, '', datetime('now','localtime'))", (id,))
        con.commit()
        con.close()
        return 1
    except Exception:
        print('이미 존재하는 사용자')
        # con = sqlite3.connect('./webScrap.db')
        # cur = con.cursor()
        # cur.execute("update user set sysdate = datetime('now','localtime') where id = ?", (id,))
        # con.commit()
        # con.close()
        return 0


# 사용자정보 select
def select_data(id):
    con = sqlite3.connect('C:/Users/58454/PycharmProjects/webScrap/webScrap.db')
    cur = con.cursor()
    cur.execute("select count(id) from user where id = ?", (id,))
    result = cur.fetchone()
    con.close()
    return str(*result)


# 구독할 아티스트정보 insert
def insert_artist_list(artist_list, userid):
    try:
        con = sqlite3.connect('C:/Users/58454/PycharmProjects/webScrap/webScrap.db')
        cur = con.cursor()
        cur.execute("update user set artist_list = (select artist_list where id = ?)||?, sysdate = datetime('now','localtime') where id = ?"
                    , (userid, artist_list, userid,))
        con.commit()
        con.close()
        return 1
    except Exception:
        print('등록 도중 오류 발생')
        return 0


# 구독할 아티스트정보 delete
def delete_artist_list(artist_list, userid):
    try:
        con = sqlite3.connect('C:/Users/58454/PycharmProjects/webScrap/webScrap.db')
        cur = con.cursor()
        cur.execute("update user set artist_list = replace(artist_list, ?, ''), sysdate = datetime('now','localtime') where id= ?", (artist_list, userid,))
        con.commit()
        con.close()
        return 1
    except Exception:
        print('삭제 도중 오류 발생')
        return 0


