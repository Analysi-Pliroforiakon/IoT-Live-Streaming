import happybase
connection = happybase.Connection('localhost', 9090)
tables = ['raw', 'late', 'aggregated']
for table in tables:
    try:
        connection.delete_table(table, disable=True)
    except:
        print(f'Table {table} does not exist')
        pass

for table in tables:
    try:
        connection.create_table(table, { 'f': dict() } )
        print(f'Table {table} created')
    except:
        print(f'Table {table} already exists')
        pass