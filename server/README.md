# Clofly - Server

## Prepare

Setup you aws ```credentials``` and ```config``` file under ~/.aws. For deamon, make sure the files are under /root. ```config``` should specify the region, and ```credentials``` should specify aws_access_key_id and aws_secret_access_key.

## Installation

    $ ./install.sh
    $ sudo ln -s /usr/bin/nodejs /usr/bin/node
    $ export NODE_PATH=/usr/local/lib/node_modules/

## Run (Local Test)

    $ ./run.sh
