# GoDaddyDDNS &#128640;
Check your machine's current public IP address using https://ipify.org and update a GoDaddy DNS A record accordingly

## Developer Guide

This is a `poetry` controlled package. To develop and test ensure that you already have `poetry` installed.

From the root run `poetry install`

To run the pre-commit against all files `poetry run pre-commit run --all-files`

To run the updater and have it print out the help page using poetry `poetry run python updater.py -h`