# UPDATE May 13th 2024
GoDaddy have updated the terms of use for their Management and DNS APIs. Usage is limited to accounts with 10 or more domains and/or an active Premium Discount Domain Club plan.

Unfortunately this means GoDaddy is no longer a viable Domain provider for the authors of this project.

This repo will be **archived** and there will be no further updates.

If you're looking for a simple DDNS system, you can check out our new repo for [PorkBunDDNS](https://github.com/UnlimitedLtd/PorkBunDDNS).


# Original README
># GoDaddyDDNS &#128640;
>Check your machine's current public IP address using https://ipify.org and update a GoDaddy DNS A record accordingly
>
>## Developer Guide
>
> is a `poetry` controlled package. To develop and test ensure that you already have `poetry` installed.
>
>From the root run `poetry install`
>
>To run the pre-commit against all files `poetry run pre-commit run --all-files`
>
>To run the updater and have it print out the help page > poetry `poetry run python updater.py -h`
