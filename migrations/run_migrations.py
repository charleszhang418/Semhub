import os
import mysql.connector

if __name__ == '__main__':
    confirmation = input('Run all migrations (y/n)?...')
    if confirmation != 'y':
        exit()

    file_names = sorted([f for f in os.listdir() if f.endswith('.sql')])
    # TODO: use dot env
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="semhub"
    )

    cur = con.cursor()
    for file_name in file_names:
        with open(file_name, 'r') as sql_file:
            commands = cur.execute(sql_file.read(), multi=True)
            # need to loop through res iterator to actually run the commands
            for command in commands:
                print(command)
            con.commit()
