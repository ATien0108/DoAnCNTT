import mysql.connector

# Thông tin kết nối cơ sở dữ liệu
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Tt010803',
    'database': 'tetrisgame_ver2',
}

def add_player_to_database(player_name):
    connection = None  # Khởi tạo connection với giá trị None

    try:
        # Tạo kết nối đến cơ sở dữ liệu
        connection = mysql.connector.connect(**db_config)

        # Sử dụng with để đảm bảo đóng kết nối ngay cả khi có ngoại lệ xảy ra
        with connection.cursor() as cursor:
            # Thêm tên người chơi vào cơ sở dữ liệu
            add_player_query = "INSERT INTO names (namescol) VALUES (%s)"
            player_data = (player_name,)

            cursor.execute(add_player_query, player_data)
            connection.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Đóng kết nối
        if connection and connection.is_connected():
            connection.close()

def add_score_to_database(score):
    connection = None  # Khởi tạo connection với giá trị None

    try:
        # Tạo kết nối đến cơ sở dữ liệu
        connection = mysql.connector.connect(**db_config)

        # Sử dụng with để đảm bảo đóng kết nối ngay cả khi có ngoại lệ xảy ra
        with connection.cursor() as cursor:
            # Thêm tên người chơi và điểm số vào cơ sở dữ liệu
            add_player_query = "INSERT INTO scores (scorescol) VALUES (%s)"
            player_data = (score,)

            cursor.execute(add_player_query, player_data)
            connection.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Đóng kết nối
        if connection and connection.is_connected():
            connection.close()

def get_history():
    connection = None

    try:
        connection = mysql.connector.connect(**db_config)

        with connection.cursor() as cursor:
            # Truy vấn lịch sử từ cơ sở dữ liệu sử dụng INNER JOIN
            select_query = """
                SELECT names.namescol, scores.scorescol
                FROM names
                INNER JOIN scores ON names.idnames = scores.idscores
                ORDER BY scores.scorescol DESC
                LIMIT 10
            """
            cursor.execute(select_query)
            history = cursor.fetchall()

            return history

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        if connection and connection.is_connected():
            connection.close()



# Xóa dữ liệu trong bảng names và reset lại khóa chính tự tăng (MySQL)
# DELETE FROM tetrisgame_ver2.names;
# ALTER TABLE tetrisgame_ver2.names AUTO_INCREMENT = 1;