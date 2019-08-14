class OctopusMachines:

    def __init__(self, plugin, interface):
        self.plugin = plugin
        self.interface = interface
        
    def send_machines(self, msg, args):
        machines = self.interface.get_machines(msg)
        machine_names = [
            machine['Name'] for machine in machines
        ]
        self._send_card(msg, machine_names)

    def find_machines_by_name(self, msg, machine_names):
        machines = self.interface.get_machines(msg)
        machine_ids = [
            machine['Id'] for machine in machines 
            if machine['Name'].lower() in machine_names
        ]
        return machine_ids

    def _send_card(self, msg, machine_names):
        body = '\n'.join(machine_names)
        self.plugin.send_card(body=body, in_reply_to=msg)