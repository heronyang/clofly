# Logger

To carefully log the user actions and system messages for maintainence and debugging purpose, we will use the [Sentry](https://sentry.io/) as our log aggregater and server. The installation of the Sentry is shown below.

## Prerequisite

1. `Docker` v1.13.1+
2. `Docker-compose` v1.11.1+

If you haven't installed them, you may run the bash script `sudo ./pre_install.sh` under root to install the docker engines.

##Installation

1. Copy the repo using `git clone https://github.com/getsentry/onpremise.git`.
2. Run `docker-compose run --rm web config generate-secret-key` and put the `SENTRY_SECRET_KEY` into `docker_compose.yml`
3. Run `sudo ./install.sh`. During intallation, you will be promted to create the superuser on the commandline. During this step, the redis docker and pstgres docker will also be run and built.

## Run the server
1. You can access the web UI at `http://localhost:9000` by default.  

