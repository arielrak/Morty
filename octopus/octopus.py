from errbot import BotPlugin, botcmd

from library.octopus_interface import OctopusInterface
from library.octopus_permissions import OctopusPermissions
from library.octopus_names import OctopusNames
from library.octopus_machines import OctopusMachines
from library.octopus_tasks import OctopusTasks
from library.octopus_templates import OctopusTemplates
from library.octopus_predefined import OctopusPredefinedTemplates 
from library.octopus_artifacts import OctopusArtifacts
from client.client_config import client_url, standard_token, admin_token

class OctopusPlugin(BotPlugin):
    
    def activate(self):
        super(OctopusPlugin, self).activate()
        base_url = client_url + '/octopus'
        self.interface = OctopusInterface(
            self, 
            base_url=base_url,
            standard_token=standard_token,
            admin_token=admin_token
        )
        self.permissions = OctopusPermissions(self)
        self.names = OctopusNames(self, self.interface)
        self.machines = OctopusMachines(self, self.interface)
        self.tasks = OctopusTasks(self, self.interface)
        self.templates = OctopusTemplates(self.interface, self.machines)
        self.predefined = OctopusPredefinedTemplates(self.interface, self.templates)
        self.artifacts = OctopusArtifacts(self, self.interface)

    @botcmd(split_args_with=',')
    def octopus_predefined_run(self, msg, args):
        """
        Runs an Octopus step template with predefined parameter settings.
        Settings defined in oc_config.py
        !octopus predefined run <TEMPLATE NAME>, <SETTING NAME>
        """
        return self.predefined.run(msg, args)

    @botcmd
    def octopus_predefined_get(self, msg, args):
        '''
        Get a list of predefined parameter settings for a template.
        !octopus predefined get <TEMPLATE NAME>
        '''
        return self.predefined.send_settings(msg, args)

    @botcmd
    def octopus_run(self, msg, args):
        """
        Runs an Octopus step template script.
        !octopus run <TEMPLATE NAME/TEMPLATE ID NUMBER>
        Set values for parameters using the !param <VALUE> command.
        Once all parameters are set, run the template using the !deploy to command.
        This command can be cancelled at anytime using the !cancel command.
        """
        return self.templates.run(msg, args)
        
    @botcmd(flow_only = True)
    def cancel(self, msg, args):
        '''Cancels a request in progress.'''
        return "Task cancelled."
    
    @botcmd(flow_only = True)
    def param(self, msg, args):
        '''Set a parameter value through: !param <VALUE>'''
        return self.templates.param(msg, args)

    @botcmd(flow_only = True, split_args_with=',')
    def deploy_to(self, msg, args):
        '''
        Confirm that the given parameters are correct and run the script on the specified machine
        !deploy to <MACHINE_NAMES>
        For multiple target deployments, separate machine names with a comma
        '''
        return self.templates.confirm(msg, args)

    @botcmd
    def octopus_artifacts(self, msg, args):
        '''
        Sends links to the artifacts associated with a given task.
        !octopus artifacts <TASK ID NUMBER>
        '''
        task_id = args
        self.artifacts.send_artifacts(msg, task_id)

    @botcmd
    def octopus_machines(self, msg, args):
        """
        Get a list of the names of all deployment target machines.
        """
        self.machines.send_machines(msg, args)

    @botcmd
    def octopus_names(self, msg, args):
        """
        Get a list of the names of the step templates.
        By default, only fetches templates that are neither blacklisted nor ignored
        !octopus names
        !octopus names all
        !octopus names blacklisted [only] ("blacklisted only" will only fetch blacklisted templates)
        !octopus names ignored [only]
        """
        self.names.send_names(msg, args)

    @botcmd
    def octopus_tasks(self, msg, args):
        """
        Get the status of the most recent tasks run. Defaults to 10 tasks.
        !octopus tasks <NUMBER OF TASKS TO FETCH>
        """
        self.tasks.send_tasks(msg, args)

    @botcmd
    def octopus_task(self, msg, args):
        """
        Get the status of a specific task.
        !octopus task <TASK ID NUMBER>
        """
        self.tasks.send_task_by_id(msg, args)
        
    @botcmd(admin_only=True, hidden=True)
    def octopus_permissions_add(self, msg, args):
        """
        To add the slack user @john.doe from the permissions list: 
        !octopus permissions add john.doe
        """
        return self.permissions.add_permissions(args)

    @botcmd(admin_only=True, hidden=True)
    def octopus_permissions_get(self, msg, args):
        """
        Gets a list of the users with blacklist permissions.
        """
        return self.permissions.get_permissions()
    
    @botcmd(admin_only=True, hidden=True)
    def octopus_permissions_remove(self, msg, args):
        """
        To remove the slack user @john.doe from the permissions list: 
        !octopus permissions remove john.doe
        """
        return self.permissions.remove_permissions(args)

    @botcmd(admin_only=True, hidden=True)
    def octopus_permissions_clear(self, msg, args):
        """
        If the permissions list becomes corrupted, use this command to clear it out and create a new empty list.
        """
        return self.permissions.clear_permissions()
