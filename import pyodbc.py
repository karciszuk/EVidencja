import pyodbc

# Define your connection string
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=QRICE;"
    "DATABASE=cepik;"
    "Trusted_Connection=yes;"
)

# Create a connection to the SQL Server
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Example of inserting data
for vehicle in vehicles:
    cursor.execute("""
        INSERT INTO VehiclesTable (Field1, Field2, ...)
        VALUES (?, ?, ...)
    """, vehicle['field1'], vehicle['field2'], ...)

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()