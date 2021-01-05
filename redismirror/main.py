import click
import sys
import redis
import re
from redisCommand import *
# TO DO:
# 1. Add timer to mirror process
# 2. Add auth option
# 3. Support to split it to multi node
# 4. Support all redis command
# 5. Add number of item to mirror limit


@click.command()
@click.option("--host", default="127.0.0.1", help="Destination redis host/IP.")
@click.option("--port", default=6379, help="Destination redis port.")
@click.option("--db", default="0", required=False, help="Destination redis DB.")
@click.option("--auth", required=False, help="Destination redis auth info.")
def main(host, port, db, auth):
    r = makeConnection(host, port, db, auth)
    getSTDOUT(r)


def makeConnection(host, port, db, auth):
    """Function to create redis connection

    Note:
        If the connection failed, the program will exit 1

    Args:
        host (str): redis connection string
        port (int): redis port number
        db (int): redis database name
        auth (str): auth info for redis

    Returns:
        connection: connection object for redis
    """

    pool = redis.ConnectionPool(host=host, port=port, db=db)
    r = redis.StrictRedis(connection_pool=pool)
    try:
        r.ping()
        print("Redis is connected..")
    except Exception as e:
        print(f"Redis connection error ({e})")
        sys.exit(1)
    return r


def getSTDOUT(connection):
    if not sys.stdin.isatty():
        input_stream = sys.stdin
    else:
        print("There is no stdin, check help for more info. exit 1")
        sys.exit(1)
    for line in input_stream:
        try:
            tmpLine = line.split(" ", 5)
            keyType = str(tmpLine[3]).strip('"')
            if keyType == "set":
                setFunc(line, connection)
            elif keyType == "hset":
                hsetFunc(line, connection)
            else:
                print(f"key type ({keyType}) if not supported yet.")
        except:
            print("Skip line | {0} ....".format(line[:100]))


if __name__ == "__main__":
    main()