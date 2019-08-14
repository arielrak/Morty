class OctopusTasks:

    def __init__(self, plugin, interface):
        self.plugin = plugin
        self.interface = interface
    
    def send_tasks(self, msg, args):
        limit = None
        if args != "":
            limit = args
        task_list = self.interface.get_tasks(msg, limit)
        self._send_cards(msg, task_list)

    def send_task_by_id(self, msg, args):
        task_id = 'ServerTasks-' + args
        task_info = self.interface.get_task(msg, task_id)
        self._send_cards(msg, [task_info])

    def _send_cards(self, msg, tasks):
        for task_info in tasks:
            color = self._get_color(task_info)
            self.plugin.send_card(
                body=self._format_task(task_info),
                color=color,
                in_reply_to=msg
            )

    def _get_color(self, task_info):
        if task_info['ErrorMessage']:
            return 'red'
        elif task_info['IsCompleted']:
            return 'green'
        else:
            return 'orange'

    def _format_task(self, task_info):
        description = task_info['Description']
        is_completed = task_info['IsCompleted']
        finished_successfully = task_info['FinishedSuccessfully']
        error = task_info['ErrorMessage']
        task_id = task_info['Id']

        if not is_completed:
            status = 'Incomplete'
        if is_completed and finished_successfully:
            status = 'Complete'
        if is_completed and not finished_successfully:
            status = 'Failed'

        string_builder = []
        string_builder.append('*{}*: {}'.format(task_id, description))
        string_builder.append('• Status: ' + status)

        if error:
            string_builder.append('>{}'.format(error.replace('\n', '\n>')))

        return '\n'.join(string_builder)