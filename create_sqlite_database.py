import sqlite3
conn = sqlite3.connect('coached_validate.db')
c = conn.cursor()

c.execute('''CREATE TABLE targets
                 (idx text, entry_name text, status text, protein_names text, gene_names text, organism text, length int)''')


