import csv
import MySQLdb
import my_settings

from django.db import connection


db_settings = my_settings.DATABASES
options = db_settings['default'].get('OPTIONS', None)

if options and 'read_default_file' in options:
    db = MySQLdb.connect(read_default_file=options['read_default_file'])
else:
    db_default = db_settings['default']
    db = MySQLdb.connect(host= db_default.get('HOST'),
                         user= db_default.get('USER'),
                         passwd= db_default.get('PASSWORD'),
                         db= db_default.get('NAME'))

cursor = db.cursor()


with open('merge_data.csv') as csv_files:
    reader = csv.DictReader(csv_files)

    for row in reader:
        print(f"row == {row['item_id']}")

        sql = f"""INSERT INTO clothes (
            item_id,
            user_gender,
            img_ref,
            page_ref,
            temp_min,
            temp_max
        ) VALUES (
            %(item_id)s,
            %(user_gender)s,
            %(img_ref)s,
            %(page_ref)s,
            %(temp_min)s,
            %(temp_max)s
        )"""

        cursor.execute(sql, row)

db.commit()
db.close()


