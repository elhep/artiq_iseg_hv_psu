#!/usr/bin/env python3

import argparse
import asyncio
import sys

from sipyco import common_args
from sipyco.pc_rpc import simple_server_loop
from artiq_iseg_hv_psu.driver import ArtiqIsegHvPsu, ArtiqIsegHvPsuSim 


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device_ip", default=None)
    parser.add_argument(
        "--simulation",
        action="store_true",
        help="Put the driver in simulation mode, even if " "--device_ip is used.",
    )
    common_args.simple_network_args(parser, 3280)
    common_args.verbosity_args(parser)
    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)

    if not args.simulation and args.device_ip is None:
        print(
            "You need to specify either --simulation or -d/--device_ip "
            "argument. Use --help for more information."
        )
        sys.exit(1)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        if args.simulation:
            dev = ArtiqIsegHvPsuSim()
        else:
            dev = ArtiqIsegHvPsu(args.device_ip)
        try:
            simple_server_loop(
                {"artiq_iseg_hv_psu": dev},
                common_args.bind_address_from_args(args),
                args.port,
                loop=loop,
            )
        finally:
            dev.close()
    finally:
        loop.close()


if __name__ == "__main__":
    main()
