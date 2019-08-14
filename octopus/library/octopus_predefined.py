from .oc_config.oc_config import predefined

class OctopusPredefinedTemplates:
    def __init__(self, interface, templates):
        self.interface = interface
        self.templates = templates

    def run(self, msg, args):
        args = [arg.strip() for arg in args]
        name = args[0]
        settings = args[1]
        parameters = predefined[name][settings]
        template = self.interface.get_template(msg, name=name)
        template_id = template['Id']

        msg.ctx['name'] = name
        msg.ctx['id'] = template_id
        msg.ctx['parameter_dict'] = parameters
        msg.ctx['index'] = 0
        msg.ctx['num_parameters'] = 0

        return self.templates.ask_for_confirmation(msg)
    
    def send_settings(self, msg, args):
        template_name = args
        if template_name not in predefined:
            return "No parameter settings found."
        template_settings = predefined[template_name]
        string_builder = []
        for setting in template_settings:
            string_builder.append("**{}**:".format(setting))
            parameter_dict = template_settings[setting]
            for parameter in parameter_dict:
                string_builder.append(" • {}: *{}*".format(
                    parameter, parameter_dict[parameter]
                ))
        return "\n\n".join(string_builder)