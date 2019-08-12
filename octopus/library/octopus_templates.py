class OctopusTemplates:
    
    def __init__(self, interface, machines):
        self.interface = interface
        self.machines = machines

    def run(self, msg, args):  # a command callable with !octopus
        args = args.strip()
        if args.isdigit():
            template_id = "ActionTemplates-" + args
            return self._run_command(msg, template_id=template_id)
        else:
            name = args
            return self._run_command(msg, name=name)

    def param(self, msg, args):
        if not self._parameters_needed(msg):
            return "No more parameters needed."
        parameter = self._get_current_parameter(msg)
        name = parameter['Name']
        value = args
        self._add_parameter(msg, name, value)
        return self._get_next_step(msg)

    def confirm(self, msg, args):
        if self._parameters_needed(msg):
            return "Parameters still needed. Task cancelled."
        machine_names = [machine.strip().lower() for machine in args]
        msg.ctx['machines'] = self.machines.find_machines_by_name(msg, machine_names)
        task_info = self._make_request(msg)
        if 'Id' not in task_info:
            return task_info['message']
        task_id = task_info['Id']
        return "Template running as " + task_id

    def _run_command(self, msg, name=None, template_id=None):
        template = self.interface.get_template(msg, template_id=template_id, name=name)
        self._build_context(msg, template)
        return self._get_next_step(msg)

    def _get_next_step(self, msg):
        if self._parameters_needed(msg):
            return self._ask_for_next_parameter(msg)
        else:
            return self.ask_for_confirmation(msg)

    def ask_for_confirmation(self, msg):
        name = msg.ctx['name']
        string_builder = []
        string_builder.append("Run **{}**?".format(name))
        parameter_dict = msg.ctx['parameter_dict']
        for parameter in parameter_dict:
            string_builder.append("**{}**: *{}*".format(
                parameter,
                parameter_dict[parameter]
            ))
        return "\n\n".join(string_builder)

    def _build_context(self, msg, template):
        msg.ctx['name'] = template['Name']
        msg.ctx['id'] = template['Id']
        msg.ctx['parameter_list'] = template['Parameters']
        msg.ctx['num_parameters'] = len(template['Parameters'])
        msg.ctx['index'] = 0
        msg.ctx['parameter_dict'] = {}

    def _parameters_needed(self, msg):
        index = msg.ctx['index']
        num_parameters = msg.ctx['num_parameters']
        return index < num_parameters

    def _ask_for_next_parameter(self, msg):
        parameter = self._get_current_parameter(msg)
        label = parameter['Label']
        info = parameter['HelpText']
        return "Input value for parameter **{}**: *{}*".format(
            label,
            info
        )

    def _make_request(self, msg):
        name = msg.ctx['name']
        template_id = msg.ctx['id']
        parameters = msg.ctx['parameter_dict']
        machines = msg.ctx['machines']
        return self.interface.post_request(msg, name, template_id, parameters, machines)

    def _get_current_parameter(self, msg):
        index = msg.ctx['index']
        parameter_list = msg.ctx['parameter_list']
        return parameter_list[index]

    def _add_parameter(self, msg, name, value):
        msg.ctx['parameter_dict'][name] = value
        msg.ctx['index'] += 1