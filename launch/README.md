# Launch Scripts for a Tutorons server

## Configuring your machine

First, install a recent version of Ansible.
Then, make a local `aws-credential.json` file in this directory.
This JSON file should have these contents, substituting in your own credentials:

    {
        "aws_access_key_id": <access-key-id>,
        "aws_secret_access_key": <secret-access-key>
    }

## Running the scripts

To deploy to the Tutorons server, run:

    ./deploy

Useful tags, that can be specified with the `--tags` argument, include:
* `updatecode`: fetch the code and restart web application
* `pythonpkgs`: update the Python dependencies
* `scripts`: run setup scripts
* `processes`: reload the supervisord processes the web app depends on
