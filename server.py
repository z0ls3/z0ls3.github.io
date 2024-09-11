from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})  # 允许所有来源

@app.route('/api/save-data', methods=['POST'])
def save_data():
    # 获取请求体中的JSON数据
    data = request.get_json()

    # 这里仅作演示，实际情况下你需要将数据保存到数据库或其他存储介质
    # 示例：将数据打印出来，并返回成功信息
    print("Received data:", data)
    print(data['elapsedTimeInSeconds'])
    print(data['mbti'])
    print(data['sum'])
    # 连接MySQL数据库
    connection = pymysql.connect(host='',
                        user='',
                        password='',
                        db='mbti',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # 构造INSERT语句
            insert_query = """
                INSERT INTO info (mbti, score, UsageTime)
                VALUES (%s, %s, %s)
            """
            
            # 准备参数
            insert_values = (data['mbti'], data['sum'], data['elapsedTimeInSeconds'])
            # 执行插入操作
            cursor.execute(insert_query, insert_values)
            # 提交事务
            connection.commit()
    except pymysql.MySQLError as error:
        print(f"Error: {error}")
    finally:
        if connection:
            connection.close()
    # 假设保存操作成功
    status = 'success'
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8000)
