from cement import App, CaughtSignal, Controller, ex, get_version
from handler import *

VERSION = (1, 0, 0, "alpha", 0)

VERSION_BANNER = (
    """
redis mirror v%s
"""
    % get_version()
)


class Base(Controller):
    class Meta:
        label = "base"

        arguments = [
            ### add a version banner
            (["-v", "--version"], {"action": "version", "version": VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="",
    )
    def mirror(self):
        rd = makeConnection("localhost")
        getSTDOUT(rd)


class MyApp(App):
    class Meta:
        # application label
        label = "x"

        # register handlers
        handlers = [Base]

        # call sys.exit() on close
        close_on_exit = True


def main():
    with MyApp() as app:
        try:
            app.run()
        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % e)
            app.exit_code = 0


if __name__ == "__main__":
    main()
