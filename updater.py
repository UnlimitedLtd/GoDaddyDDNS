#! /usr/bin/env python3

import argparse
import concurrent.futures
import logging

import godaddyddns.godaddy as godaddy
import godaddyddns.ipify as ipify

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


logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %H:%M:%S",
)

logger = logging.getLogger(__name__)

if args.verbose:
    logger.setLevel(logging.DEBUG)

ipify_connector = ipify.IPify(
    timeout=args.timeout,
)

godaddy_connector = godaddy.GoDaddy(
    api_key=args.api_key,
    api_secret=args.api_secret,
    timeout=args.timeout,
)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    record_task = executor.submit(godaddy_connector.get_a_record, domain=args.domain)
    current_task = executor.submit(ipify_connector.get_current_ip)

    record = record_task.result()
    current = current_task.result()

logger.debug("Domain: %s, A Record IP: %s", args.domain, record.ip)

logger.debug("Current Machine IP: %s", current.ip)


if current.ip != record.ip:
    logger.debug("Updating %s A record to %s", args.domain, current.ip)
    godaddy_connector.update_a_record(domain=args.domain, ip=current.ip, ttl=args.ttl)
else:
    logger.debug("No update required")
