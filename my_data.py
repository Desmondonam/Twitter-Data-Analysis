import pandas as pd
import psycopg2
from psycopg2 import Error
from decouple import config

postgres_user, postgres_pass = config('postgres_user'), config('postgres_pass')
# print(postgres_user, postgres_pass)

def DBConnect(dbName=None):
   
    try:
        conn = psycopg2.connect(host='localhost',
                                user=postgres_user,
                                password=postgres_pass,
                                database=dbName,
                                port="3060")

        cur = conn.cursor()
        conn.autocommit = True
        print('Connection Established')

    except (Exception, Error) as error:
        print(error)
        conn, cur = None, None

    return conn, cur


def createDB(dbName: str) -> None:
    
    try:
        postgres_db = config('postgres_user')
        # print(postgres_db)
        conn, cur = DBConnect(postgres_db)
        sql = f"CREATE DATABASE {dbName};"
        cur.execute(sql)
        cur.close()

    except (Exception, Error) as e:
        print(e)

def createTables(dbName: str) -> None:
   
    conn, cur = DBConnect(dbName)
    sqlFile = 'database2.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')

    for command in sqlCommands:
        try:
            res = cur.execute(command)
            response = "Table created sucessfuly"
        except Exception as ex:
            print("Command skipped: ", command)
            response = "Table Not Created"
            print(ex)
    conn.commit()
    cur.close()

    return print(response)

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
   
    cols_2_drop = ['Unnamed: 0', 'timestamp']
    try:
        df = df.drop(columns=cols_2_drop, axis=1)
        df = df.fillna(0)
    except KeyError as e:
        print("Error:", e)

    return df


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
   
    conn, cur = DBConnect(dbName)

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} (created_at, source, clean_text, language, favorite_count,retweet_count, 
                                                polarity, subjectivity, original_author, followers_count,  
                                                friends_count,sensitivity,hashtags, user_mentions, place)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[5]), (row[6]), row[7], row[8], row[9], row[10], row[11], row[12],
                row[13], row[14], row[15])

        try:
            # run SQL command
            cur.execute(sqlQuery, data)
            conn.commit()
            print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return

def db_execute_fetch(*args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:
   
    connection, cursor1 = DBConnect(**kwargs)
    if many:
        cursor1.executemany(*args)
    else:
        cursor1.execute(*args)

    #column names
    field_names = [i[0] for i in cursor1.description]

    #column values
    res = cursor1.fetchall()

    #row count and show info
    nrow = cursor1.rowcount
    if tablename:
        print(f"{nrow} records fetched from {tablename} table")

    cursor1.close()
    connection.close()

    # return result
    if rdf:
        return pd.DataFrame(res, columns=field_names)
    else:
        return res


if __name__ == "__main__":
    createDB(dbName='tweets')
    # emojiDB(dbName='tweets')
    createTables(dbName='tweets')

    df = pd.read_csv('clean_tweet.csv')
    print(df.head())

    insert_to_tweet_table(dbName='tweets', df=df, table_name='Tweeter')