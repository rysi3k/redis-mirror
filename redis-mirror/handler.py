import sys
import redis


def makeConnection(connectionString):
    print("Init connection redis..")
    pool = redis.ConnectionPool(host=connectionString, port=6377, db=0)
    redisConnection = redis.StrictRedis(connection_pool=pool)
    return redisConnection


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
