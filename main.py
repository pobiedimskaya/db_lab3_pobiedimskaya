import psycopg2
import matplotlib.pyplot as plt

username = 'postgres'
password = 'postgres'
database = 'lab2'
host = 'localhost'
port = '5432'


query_1 = '''
CREATE VIEW HousesByYear AS
SELECT 
		year_built, 
		COUNT(house_id) houses_amount 
FROM houses 
GROUP BY 1 
ORDER BY 1
'''

query_2 = '''
CREATE VIEW HousesByDistrict AS
SELECT  
		neighborhood_name,
		COUNT(house_id) houses_amount 
FROM houses h
JOIN neighborhoods n
ON h.neighborhood_id = n.neighborhood_id
GROUP BY 1 
ORDER BY 1
'''

query_3 = '''
CREATE VIEW PriceByYear AS
SELECT  
		CAST(AVG(sale_price) AS int) avg_price,
		year_built 
FROM houses h
JOIN sales s
ON h.sale_id = s.sale_id
GROUP BY 2 
ORDER BY 2
'''

con = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with con:
    cur = con.cursor()

    fig, (bar, pie, graph) = plt.subplots(1, 3)

    cur.execute('DROP VIEW IF EXISTS HousesByYear')
    cur.execute(query_1)
    cur.execute('SELECT * FROM HousesByYear')

    year_built = []
    houses_amount = []
    for row in cur:
        year_built.append(row[0])
        houses_amount.append(row[1])

    bar.set_title('Кількість будинків, побудованих у кожний рік')
    bar.set_xlabel('Рік')
    bar.set_ylabel('Кількість будинків')
    bar.bar(year_built, houses_amount)
    bar.set_xticklabels(year_built)

    cur.execute('DROP VIEW IF EXISTS HousesByDistrict')
    cur.execute(query_2)
    cur.execute('SELECT * FROM HousesByDistrict')
    neighborhood_name = []
    houses_amount = []
    for row in cur:
        neighborhood_name.append(row[0])
        houses_amount.append(row[1])
    pie.set_title('Кількість будинків в залежності від району')
    pie.pie(houses_amount, labels=neighborhood_name, autopct='%1.1f%%')

    cur.execute('DROP VIEW IF EXISTS PriceByYear')
    cur.execute(query_3)
    cur.execute('SELECT * FROM PriceByYear')
    avg_price = []
    year_built = []
    for row in cur:
        avg_price.append(row[0])
        year_built.append(row[1])
    graph.plot(year_built, avg_price)
    graph.set_xlabel('Рік побудови')
    graph.set_ylabel('Ціна')
    graph.set_title('Ціна в залежності від року побудови')
    for i, j in zip(year_built, avg_price):
        graph.annotate(i, xy=(i, j))

    plt.show()

