import happybase
connection = happybase.Connection('localhost', 9090)
tables = ['rawData', 'lateData', 'aggregatedData']

tablesExisted = connection.tables()
tablesExisted = [table.decode('utf-8') for table in tablesExisted]

for table in tables:
    if table in tablesExisted:
        try:
            connection.delete_table(table, disable=True)
            print(f'Table {table} deleted.')
            try:
                # the minimum versions we want is 3
                # we will add one in case of an error occurs.
                connection.create_table(table, { 'cf': dict(max_versions=4) } )
                print(f'Table {table} created.')
            except:
                print(f'Table {table} already exists. Thish should not happen.')
                pass

        except:
            print(f'Table {table} cannot be deleted')
            pass
    else:
        print(f'Table {table} does not exist')
        try:
            # the minimum versions we want is 3
            # we will add one in case of an error occurs.
            connection.create_table(table, { 'cf': dict(max_versions=4) } )
            print(f'Table {table} created')
        except:
            print(f'Table {table} already exists')
            pass
