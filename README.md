# Mirror Redis Traffic to another redis node

# redis-mirror
Realtime Redis Traffic Mirror to another instance, this script read the STDOUT from `redis-cli monitor` command and mirror keys to another instance.

## Use Case/Note
In some production/development cases, you need to mirror Redis traffic to another node in order to do some investigation or debugging.
* This script does not set `TTL` to mirrored key since you need it for debugging.
* For now, this script support `set`,`hset` I will add the other command soon, or if you have a time, please create a pull request :). 


## TO DO:
1. Add the most common redis command to mirror script.
2. Add TTL as an option in mirrored redis instance, plus add an option to expand the origin `TTL`.
3. Support cluster to a single redis instance or Or vice versa.
4. Add more option such as `DB` Name, `Host`, `Port`...etc.
5. Improve mirrored value without any modification.
6. Add option to dump all keys name to file for further analysis.

## Useages
```Bash
redis-cli monitor | python redismirror.py 
```


## Installation

```
$ pip install -r requirements.txt

$ pip install setup.py
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run redismirror cli application

$ redismirror --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Redis Mirror `,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it redismirror --help
```



## Extra
To Generate sample data for your test use the below command:
```Bash
cd tests/Generator/;bash SampleDataInserter.sh
```


The following commands are also not logged:

* AUTH
* EXEC
* HELLO
* QUIT


Cost of running MONITOR
Because MONITOR streams back all commands, its use comes at a cost. The following (totally unscientific) benchmark numbers illustrate what the cost of running MONITOR can be.

Benchmark result without MONITOR running:


```Bash
$ src/redis-benchmark -c 10 -n 100000 -q
PING_INLINE: 101936.80 requests per second
PING_BULK: 102880.66 requests per second
SET: 95419.85 requests per second
GET: 104275.29 requests per second
INCR: 93283.58 requests per second
```
Benchmark result with MONITOR running (redis-cli monitor > /dev/null):
```Bash
$ src/redis-benchmark -c 10 -n 100000 -q
PING_INLINE: 58479.53 requests per second
PING_BULK: 59136.61 requests per second
SET: 41823.50 requests per second
GET: 45330.91 requests per second
INCR: 41771.09 requests per second
```
In this particular case, running a single MONITOR client can reduce the throughput by more than 50%. Running more MONITOR clients will reduce throughput even more.
