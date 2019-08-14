To start the client server as a service:
1. Edit the ExecStart variable in octopus.service so that it points to the start_client_service file in this folder.
2. Edit start_client_service file to point to the activation script of the virtual environment, and the main.py file in this folder.
3. Copy the octopus.service file to the directory /etc/systemd/system
4. The service can be run through: sudo systemctl start octopus
5. It can be stopped through: sudo systemctl stop octopus
6. The status can be viewed through: systemctl status octopus
