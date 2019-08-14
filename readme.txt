To start errbot as a service:
1. Edit the ExecStart variable in slackbot.service so that it points to the start_bot file in this folder.
1a. Set the permissions of start_bot to 777.
2. Edit start_bot file to point to the activation script of the virtual environment, and the errbot command in errbot-root
3. Copy the slackbot.service file to the directory /etc/systemd/system
3a. Set the permissions of slackbot.service to 664.
4. The service can be run through: sudo systemctl start slackbot
5. It can be stopped through: sudo systemctl stop slackbot
6. The status can be viewed through: systemctl status slackbot
