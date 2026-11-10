import sqlite3
def init_db():
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Movies
                   (
                       movie_id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       title
                       TEXT
                       NOT
                       NULL,
                       genre
                       TEXT,
                       rating
                       INTEGER
                   )
                   ''')
    conn.commit()
    conn.close()

def add_movie(title, genre, rating):
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Movies (title, genre, rating) VALUES (?, ?, ?)", (title, genre, rating))
        conn.commit()
        return True
    except Exception as e:
        print("报错啦：", e)
        return False
    finally:
        conn.close()

def get_movies():
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    cursor.execute("SELECT movie_id, title, genre, rating FROM Movies")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_movie(movie_id):
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Movies WHERE movie_id = ?", (movie_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("开始测试【数据访问模块】...")
    init_db()
    add_movie("星际穿越", "科幻", 5)
    add_movie("泰坦尼克号", "爱情", 4)
    print("测试：成功添加2条数据。")
    movies = get_movies()
    print(f"当前数据库共有 {len(movies)} 条数据：")
    for m in movies:
        print(f"  ID:{m[0]} | 片名:{m[1]} | 类型:{m[2]} | 评分:{m[3]}")
    if movies:
        delete_movie(movies[0][0])
        print("测试：成功删除第一条记录。")
    print("模块测试结束！")