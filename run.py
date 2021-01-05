import click
import sys
import redis

# TO DO:
# 1. Add timer to mirror process
# 2. Add auth option
# 3. Support to split it to multi node
# 4. Support all redis command


def makeConnection(connectionString, port, db):
    print("Init connection redis..")
    pool = redis.ConnectionPool(host=connectionString, port=port, db=db)
    r = redis.StrictRedis(connection_pool=pool)
    try:
        r.ping()
        print("Redis is connected..")
    except Exception as e:
        print(
            f"Error in redis, please check the connection info or the redis it self. {e}"
        )
        sys.exit(1)
    return r


def setFunc(rLine, connection):
    line = rLine.split(" ", 5)
    keyName = line[4].strip('"')
    keyValue = line[5].strip('"')
    try:
        connection.set(keyName, keyValue)
        print(f"Key mirroed sucessfully | {keyName}")
    except Exception as e:
        print(f"Failed to set key | {keyName} | {e}")


def hsetFunc(rLine, connection):
    line = rLine.split(" ", 6)
    keyName = line[4].strip('"')
    hkeyName = line[5].strip('"')
    keyValue = str(line[6].strip('"')).lstrip('"\n')
    try:
        connection.hset(keyName, hkeyName, keyValue)
        print(f"Key mirroed sucessfully | {keyName}")
    except Exception as e:
        print(f"Failed to set key | {keyName} | {hkeyName} | {e} ")


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
            print(f"Skip line | {line}")


@click.command()
@click.option(
    "--host", default="127.0.0.1", help="Location of media file to be converted"
)
@click.option("--port", default=6379, help="Location of media file to be converted")
@click.option("--db", default="0", help="Location of media file to be converted")
@click.option("--auth", required=False, help="Location of media file to be converted")
def main(host, port, db, auth):
    rd = makeConnection(host, port, db)
    getSTDOUT(rd)


if __name__ == "__main__":
    main()