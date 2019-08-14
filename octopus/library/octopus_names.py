from .oc_config.oc_config import blacklisted, ignored

class OctopusNames:

    def __init__(self, plugin, interface):
        self.plugin = plugin
        self.interface = interface

    def send_names(self, msg, args):
        filter_functions = self._create_name_filters(args)
        name_list = self._get_and_filter_names(msg, filter_functions)
        self._send_card(msg, name_list)
        
    def _create_name_filters(self, args):
        arg_list = args.split()
        filter_functions = []
        if 'only' not in arg_list:
            filter_functions.append(
                lambda name: name[0] not in blacklisted and name[0] not in ignored
            )
        if 'all' in arg_list:
            filter_functions.append(lambda name: True)
        if 'blacklisted' in arg_list:
            filter_functions.append(lambda name: name[0] in blacklisted)
        if 'ignored' in arg_list:
            filter_functions.append(lambda name: name[0] in ignored)
        return filter_functions

    def _get_and_filter_names(self, msg, filter_functions):
        name_list = self.interface.get_names(msg)
        name_list = [
            name for name in name_list 
            if self._keep_name(name, filter_functions)
        ]
        return name_list

    def _keep_name(self, name, filter_functions):
        for filter_function in filter_functions:
            if filter_function(name):
                return True
        return False

    def _send_card(self, msg, name_list):
        string_builder = [
            "*{}*: {}".format(name[0], name[1])
            for name in name_list
        ]
        body = '\n'.join(string_builder)
        self.plugin.send_card(body=body, in_reply_to=msg)