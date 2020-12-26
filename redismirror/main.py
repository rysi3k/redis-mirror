from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import RedisMirrorError
from .controllers.base import Base


class RedisMirror(App):
    """Redis Mirror  primary application."""

    class Meta:
        label = "redismirror"

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            "colorlog",
        ]

        # set the log handler
        log_handler = "colorlog"

        # register handlers
        handlers = [Base]


class RedisMirrorTest(TestApp, RedisMirror):
    """A sub-class of RedisMirror that is better suited for testing."""

    class Meta:
        label = "redismirror"


def main():
    with RedisMirror() as app:
        try:
            app.run()

        except AssertionError as e:
            print("AssertionError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except RedisMirrorError as e:
            print("RedisMirrorError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % e)
            app.exit_code = 0


if __name__ == "__main__":
    main()
