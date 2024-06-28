from sqlalchemy import Column, Integer, String, BigInteger, MetaData, create_engine, text

engine = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                       ':3306/salessystem')

connection = engine.connect()

query = "SELECT * FROM lista_facturas WHERE emision > '2024-06-25'"
result = connection.execute(text(query))


for row in result:
    print(row)