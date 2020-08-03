import psycopg2, json, re, os

def parse(s):
    # s looks like "postgres://<username>:<password>@<host>/<dbname>"
    query = re.search(r"postgres://(.+):(.+)@(.*)/(.*)", s)
    keys = ['user','password','host','database']
    return {keys[i]:query.group(i+1) for i in range(len(keys))}

def create_db():
    with open('login.json', 'r') as f: login = json.load(f)
    login = parse(os.getenv('DATABASE_URL'))
    login["port"] = 5432

    conn = psycopg2.connect(database=login['database'], user=login['user'], password=login['password'], host=login['host'], port=login['port'])

if __name__ == "__main__":
    create_db()