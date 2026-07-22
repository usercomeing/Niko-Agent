from __future__ import annotations

import sys

from niko_agent.cli import build_agent, build_arg_parser
from niko_agent.tui.app import NikoTuiApp


def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.prompt:
        print("niko does not accept one-shot prompts in TUI mode; type the prompt in the app.", file=sys.stderr)
        return 2
    agent = build_agent(args)
    NikoTuiApp(agent).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
