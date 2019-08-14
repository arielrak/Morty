To start errbot as a service:
1. Edit the ExecStart variable in slackbot.service so that it points to /path/to/errbot-venv/bin/errbot
2. Edit WorkingDirectory to /path/to/errbot-venv
3. Copy slackbot.service to /etc/systemd/system
4. Change the permissions of slackbot.service to 664.
5. sudo systemctl start slackbot
