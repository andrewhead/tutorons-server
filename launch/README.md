# Launch Scripts for a Tutorons server

## Running the scripts

To provision and deploy the Tutorons server, run:

    ./deploy

Useful tasks include:

    ./deploy --tags updatecode  # update the server
    ./deploy --tags pythonpkgs  # update the Python dependencies
    ./deploy --tags processes   # reload the supervisord processes the web app depends on
    ./deploy --tags scripts     # run the setup scripts

You will want to run these partial tasks when you can, as they'll take less time than the full deploy process.
Additional tags for other tasks are available.
These can be found in the `roles/webserver/tasks/main.yml` file.
You can also see them listed by running `./deploy --tags <some-invalid-tag>`.

## Getting Started

First, install a recent version of Ansible.
If you are on OSX, I recommend using `pip install ansible` instead of Homebrew---you are likely to get a more recent version.

Next, get an account with [Amazon Web Services](https://aws.amazon.com/console/).
You can use an existing Amazon.com existing account, but will have to enter additional registration information.
Give the e-mail address that you gave to Amazon.com to a project admin, and have them grant you S3 access.

Then, make a local `aws-credentials.json` file in this directory.
This JSON file should have these contents, substituting in your own credentials:

    {
        "aws_access_key_id": <access-key-id>,
        "aws_secret_access_key": <secret-access-key>
    }

These credentials can be found in the "Access Keys" section of the "Security Credentials" page.
You can get to this page by clicking on your name at the top-right corner of the Amazon Management Console.

Finally, you need SSH access to tutorons.com.
Generate SSH keys on your machine.
Then provide the public key (e.g., `id_rsa.pub`) to a project admin.
The project admin will add this to the `authorized_keys` for the server.

Once this is complete, follow the steps at the top of this document to update the server.
