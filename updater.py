#! /usr/bin/env python3

import argparse
import ipify
import godaddy
import timestamp

parser = argparse.ArgumentParser(
    description="Check current domain A record and update if necessary"
)
parser.add_argument("domain", help="The domain to check and update", type=str)
parser.add_argument("api_key", help="GoDaddy API key", type=str)
parser.add_argument("--ttl", help="DNS TTL", default=600, type=int)
parser.add_argument("--timeout", help="Request timeout", default=10, type=int)
parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
args = parser.parse_args()

ipify_connector = ipify.IPify(timeout=args.timeout, verbose=args.verbose)
godaddy_connector = godaddy.GoDaddy(
    api_key=args.api_key, timeout=args.timeout, verbose=args.verbose)

recordIp = godaddy_connector.get_a_record(domain=args.domain)
currentIp = ipify_connector.get_current_ip()

if currentIp.ip != recordIp.ip:
    if args.verbose:
        print(f"{timestamp.TimeStamp.get_timestamp()} Updating {
              args.domain} A record to {currentIp.ip}")

    godaddy_connector.update_a_record(
        domain=args.domain,
        ip=currentIp,
        ttl=args.ttl
    )
else:
    if args.verbose:
        print(timestamp.TimeStamp.get_timestamp(), "No update required")
