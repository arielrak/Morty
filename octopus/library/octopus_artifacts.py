class OctopusArtifacts:

    def __init__(self, plugin, interface):
        self.plugin = plugin
        self.interface = interface

    def send_artifacts(self, msg, task_id):
        artifacts = self.interface.get_artifacts(msg, task_id)
        for artifact in artifacts:
            filename = artifact[0]
            contents = artifact[1]
            self.plugin.send_card(title=filename, body=contents, in_reply_to=msg)