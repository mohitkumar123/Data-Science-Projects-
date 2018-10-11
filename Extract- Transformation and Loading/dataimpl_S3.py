#encoding=utf-8

import pymysql
import boto3
import sys

''' connect to s3 '''
s3 = boto3.resource('s3')
bucket = s3.Bucket('s3 bucket name')

''' connect to RDS '''
host = "rds host"
port = 3306
user = "username"
password = "password"
conn = pymysql.connect(host, user=user,
        port=port, passwd=password, use_unicode=True, charset='utf8')

''' mydb database '''
cur = conn.cursor()
cur.execute('DROP DATABASE IF EXISTS mydb')
cur.execute('''
    CREATE DATABASE mydb''')
cur.execute('USE mydb')

for obj in bucket.objects.all():
    key = obj.key
    ''' aisles table '''
    if key == 'aisles.csv':
        cur.execute('DROP TABLE IF EXISTS aisles')
        cur.execute('''
                CREATE TABLE aisles (aisle_id TEXT, aisle TEXT)''')
        body = obj.get()['Body'].read()
        content = body
        lines = []
        for line in content.split("\n"):
            lines.append(line)
        print('Copying '+ str(len(lines)-2) + ' lines...')
        for num in range(len(lines)-1):
            if num == 0:
                continue
            item = lines[num].split(',')
            cur.execute('''INSERT INTO aisles (aisle_id, aisle)
                        VALUES (%s,%s)''', (item[0],item[1]))
            conn.commit()
        print('Copy successfully!')
    # ''' departments table '''
    # if key == 'departments.csv':
    #     cur.execute('DROP TABLE IF EXISTS departments')
    #     cur.execute('''
    #         CREATE TABLE departments (department_id TEXT, department TEXT)''')
        # cur.execute('SELECT COUNT(*) FROM orders')
        # rows = cur.fetchall()
        # # # conn.commit()
        # print(type(rows[0][0]),rows[0][0])
    #     print(numoflines)
    #     body = obj.get()['Body'].read()
    #     content = body
    #     # .decode("utf-8")
    #     lines = []
    #     for line in content.split("\n"):
    #         lines.append(line)
    #     print('Copying '+ str(len(lines)-2) + ' lines...')
    #     for num in range(len(lines)-1):
    #         if num == 0:
    #             continue
    #         item = lines[num].split(',')
    #         cur.execute('''INSERT INTO departments (department_id, department)
    #                 VALUES (%s, %s)''', (item[0],item[1]))
    #         conn.commit()
    #     print('Copy successfully!')
    # ''' order products train table '''
    # if key == 'order_products_train.csv':
    #     cur.execute('DROP TABLE IF EXISTS order_products_train')
    #     cur.execute('''
    #         CREATE TABLE order_products_train (order_id TEXT, product_id TEXT,
    #                 add_to_cart_order TEXT, reordered TEXT)''')
        # body = obj.get()['Body'].read()
        # content = body
        # #.decode("utf-8")
        # lines = []
        # for line in content.split("\n"):
        #     lines.append(line)
        # print('Copying '+ str(len(lines)-2) + ' lines...')
    #     for num in range(len(lines)-1):
    #         if num == 0:
    #             continue
    #         item = lines[num].split(',')
    #         cur.execute('''INSERT INTO order_products_train (order_id,
    #                 product_id, add_to_cart_order, reordered)
    #                 VALUES (%s, %s, %s, %s)''',
    #                 (item[0], item[1], item[2], item[3]))
            # conn.commit()
            # if num % 1000 == 0:
            #     print('Copied '+ str(num)+' lines...')
        # print('Copy successfully!')
    # ''' orders table '''
    # if key == 'orders.csv':
    #     cur.execute('DROP TABLE IF EXISTS orders')
    #     cur.execute('''
    #         CREATE TABLE orders (order_id TEXT, user_id TEXT, eval_set TEXT,
    #                 order_number TEXT, order_dow TEXT, order_hour_of_day TEXT,
    #                 days_since_prior_order TEXT)''')
    #     body = obj.get()['Body'].read()
    #     content = body
    #     lines = []
    #     for line in content.split("\n"):
    #         lines.append(line)
    #     print('Copying '+ str(len(lines)-2) + ' lines...')
    #     for num in range(len(lines)-1):
    #         if num == 0:
    #             continue
    #         item = lines[num].split(',')
    #         cur.execute('''INSERT INTO orders (order_id, user_id, eval_set,
    #                 order_number, order_dow, order_hour_of_day,
    #                 days_since_prior_order)
    #                 VALUES (%s, %s, %s, %s, %s, %s, %s)''',
    #                 (item[0], item[1], item[2], item[3],
    #                 item[4], item[5], item[6]))
    #         conn.commit()
    #         if num % 1000 == 0:
    #             print('Copied '+ str(num)+' lines...')
    #     print('Copy successfully!')
    # ''' products table '''
    # if key == 'products.csv':
    #     cur.execute('DROP TABLE IF EXISTS products')
    #     cur.execute('''
    #         CREATE TABLE products (product_id TEXT, product_name TEXT,
    #                 aisle_id TEXT, department_id TEXT)''')
        # cur.execute('SELECT COUNT(*) FROM products')
        # rows = cur.fetchall()
        # print(rows[0][0])
        # body = obj.get()['Body'].read()
        # content = body
        # lines = []
        # for line in content.split("\n"):
        #     lines.append(line)
        # print('Copying '+ str(len(lines)-2) + ' lines...')
        # for num in range(len(lines)-1):
    #         if num == 0:
    #             continue
            # if num == 1:
            #     sline = lines[num].split('\"')
            #     print(sline)
                # item0 = sline[0].split(',')
                # item1 = sline[1]
                # item2 = sline[2].split(',')

            # cur.execute('''INSERT INTO products (product_id, product_name,
                    # aisle_id, department_id) VALUES (%s, %s, %s, %s)''',
                    # (item0[0], item1, item2[1], item2[2]))
    #         conn.commit()
    #         if num % 100 == 0:
    #             print('Copied '+ str(num)+' lines...')
    #     print('Copy successfully!')
cur.close()
