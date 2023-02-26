import happybase
connection = happybase.Connection('localhost', 9090)
tables = ['rawData', 'lateData', 'aggregatedData']

tablesExisted = connection.tables()

for table in tables:
    if table in tablesExisted:
        try:
            connection.delete_table(table, disable=True)
        except:
            print(f'Table {table} does not exist')
            pass
    else :
        print(f'Table {table} does not exist')
        try:
            connection.create_table(table, { 'cf': dict() } )
            print(f'Table {table} created')
        except:
            print(f'Table {table} already exists')
            pass
