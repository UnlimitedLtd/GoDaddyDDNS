#! /usr/bin/env python3

import argparse
import ipify
import godaddy
import utils

parser = argparse.ArgumentParser(
    description="Check current domain A record and update if necessary"
)
parser.add_argument("domain", help="The domain to check and update", type=str)
parser.add_argument("api_key", help="GoDaddy API key", type=str)
parser.add_argument("api_secret", help="GoDaddy API secret", type=str)
parser.add_argument("--ttl", help="DNS TTL", default=600, type=int)
parser.add_argument("--timeout", help="Request timeout", default=10, type=int)
parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
args = parser.parse_args()

verbose = utils.Verbose(verbose=args.verbose)

ipify_connector = ipify.IPify(timeout=args.timeout, verbose=args.verbose)
godaddy_connector = godaddy.GoDaddy(
    api_key=args.api_key, api_secret=args.api_secret, timeout=args.timeout, verbose=args.verbose)

recordIp = godaddy_connector.get_a_record(domain=args.domain)
verbose.printer(f"{args.domain} A Record IP: {recordIp.ip}")

currentIp = ipify_connector.get_current_ip()
verbose.printer(f"Current Machine IP: {currentIp.ip}")


if currentIp.ip != recordIp.ip:
    verbose.printer(f"Updating {args.domain} A record to {currentIp.ip}")

    godaddy_connector.update_a_record(
        domain=args.domain,
        ip=currentIp,
        ttl=args.ttl
    )
else:
    verbose.printer("No update required")
