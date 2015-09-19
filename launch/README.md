# Launch Scripts for a Tutorons server

To deploy to the Tutorons server, run:

    ansible-playbook -i hosts webserver.yml

Useful tags include:
* `updatecode`: fetch the code and restart web application
* `pythonpkgs`: update the Python dependencies
* `scripts`: run setup scripts
* `processes`: reload the supervisord processes the web app depends on
