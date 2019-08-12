class OctopusPermissions:

    def __init__(self, plugin):
        self.plugin = plugin

    def add_permissions(self, args):
        if 'admins' not in self.plugin:
            permissions = []
        else:
            permissions = self.plugin['admins']
        permissions.append(args)
        self.plugin['admins'] = permissions
        return "User {} added to the permissions list.".format(args)

    def get_permissions(self):
        return self.plugin['admins']

    def remove_permissions(self, args):
        permissions = self.plugin['admins']
        permissions.remove(args)
        self.plugin['admins'] = permissions
        return "User {} removed from the permissions list.".format(args)

    def clear_permissions(self):
        self.plugin['admins'] = []
        return "All permissions cleared."