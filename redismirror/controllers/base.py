from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
import sys
import redis

VERSION_BANNER = """
Mirror Redis Traffic to another redis node %s
%s
""" % (
    get_version(),
    get_version_banner(),
)


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


class Base(Controller):
    class Meta:
        label = "base"

        # text displayed at the top of --help output
        description = "Mirror Redis Traffic to another redis node"

        # text displayed at the bottom of --help output
        epilog = "Usage: redis-cli monitor | redismirror run"

        # controller level arguments. ex: 'redismirror --version'
        arguments = [
            ### add a version banner
            (["-v", "--version"], {"action": "version", "version": VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="use option --run",
        arguments=[
            ### add a sample foo option under subcommand namespace
            (
                ["-r", "--run"],
                {"help": "show avaliable options", "action": "store", "dest": "foo"},
            ),
        ],
    )
    def run(self):
        """Example sub-command."""
        rd = makeConnection("localhost")
        getSTDOUT(rd)