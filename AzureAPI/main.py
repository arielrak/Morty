import io
import json
import os

from errbot import BotPlugin, botcmd, arg_botcmd

from api_interface import RequestExecutor
from azureapi_config import keys, apps
from events.events_service import EventsService
from metrics.metrics_service import MetricsService
from query.query_displayer import QueryDisplayer
from query.query_service import QueryService


class Azureapi(BotPlugin):
    """
    Access metrics stored in Azure Insights
    """

    # Triggers on plugin activation
    def activate(self):
        super(Azureapi, self).activate()

        self._slack_key = keys["slack_api_key"]
        self._app_id = list(apps.values())[0]["azure_app_id"]
        self._app_key = list(apps.values())[0]["azure_app_key"]
        self._api_service = RequestExecutor(self._app_id, self._app_key, self._slack_key)
        self._metrics_service = MetricsService(self._api_service)
        self._events_service = EventsService(self._api_service)
        self._query_service = QueryService(self._api_service)
        self._query_displayer = QueryDisplayer()

    def _set_app(self, app_id: str, app_key: str):
        self._app_id = app_id
        self._app_key = app_key
        self._api_service = RequestExecutor(self._app_id, self._app_key, self._slack_key)

    @arg_botcmd('name', type=str, unpack_args=False)
    def change_azure_app(self, msg, args):
        if args.name not in apps:
            yield "App name not in config file!"
        else:
            self._set_app(apps[args.name]["azure_app_id"], apps[args.name]["azure_app_key"])
            yield "Changed app!"

    @arg_botcmd('--app', type=str, unpack_args=False)
    @arg_botcmd('--timespan', type=str, unpack_args=False)
    @arg_botcmd('--interval', type=str, unpack_args=False)
    @arg_botcmd('--aggregation', type=str, unpack_args=False)
    @arg_botcmd('--segment', type=str, unpack_args=False)
    @arg_botcmd('--top', type=str, unpack_args=False)
    @arg_botcmd('--orderby', type=str, unpack_args=False)
    @arg_botcmd('--filter', type=str, unpack_args=False)
    @arg_botcmd('metric_id', type=str, unpack_args=False, default=None)
    def get_azure_metric(self, msg, args):
        """
        Get information about a specific metric
        """

        yield "Let me fetch that for you"

        old_appid = self._app_id
        old_appkey = self._app_key
        if args.app not in apps:
            yield "App name not in config file, proceeding with default."
        else:
            self._set_app(apps[args.name]["azure_app_id"], apps[args.name]["azure_app_key"])
            yield "Proceeding with "+args.app


        args.app = None
        response = self._metrics_service.get_metric(args)
        summary_value = str(self._find(args.metric_id, response))
        if summary_value is None:
            yield "Metric not found"
        else:
            self._handle_response(response, msg, str(args.metric_id) + " : " + summary_value)

        self._set_app(self, old_appid, old_appkey)

    @botcmd
    def get_all_azure_metrics(self, msg, args):
        """
        See all available search metrics for azure insights
        """

        yield "Let me fetch that for you..."

        response = self._metrics_service.get_all_metrics()

        return_list = [key for key, _ in response.items()]
        self.send_card(title="All available metrics",
                       body='\n '.join(return_list),
                       color="green",
                       in_reply_to=msg)

    @arg_botcmd('--app', type=str, unpack_args=False)
    @arg_botcmd('--timespan', type=str, unpack_args=False)
    @arg_botcmd('--filter', type=str, unpack_args=False)
    @arg_botcmd('--search', type=str, unpack_args=False)
    @arg_botcmd('--orderby', type=str, unpack_args=False)
    @arg_botcmd('--select', type=str, unpack_args=False)
    @arg_botcmd('--skip', type=str, unpack_args=False)
    @arg_botcmd('--top', type=str, unpack_args=False)
    @arg_botcmd('--format', type=str, unpack_args=False)
    @arg_botcmd('--count', type=str, unpack_args=False)
    @arg_botcmd('--apply', type=str, unpack_args=False)
    @arg_botcmd('--event_id', type=str, unpack_args=False)
    @arg_botcmd('event_type', type=str, unpack_args=False, default=None)
    def get_azure_event(self, msg, args):
        """
        Get information about a specific event
        """
        yield "Let me fetch that for you"

        old_appid = self._app_id
        old_appkey = self._app_key
        if args.app not in apps:
            yield "App name not in config file, proceeding with default."
        else:
            self._set_app(apps[args.name]["azure_app_id"], apps[args.name]["azure_app_key"])
            yield "Proceeding with " + args.app
        args.app = None

        response = self._events_service.get_event(args)

        self._handle_response(response, msg, args.event_type)

        self._set_app(self, old_appid, old_appkey)

    @botcmd
    def get_azure_events_metadata(self, msg, args):
        """
        Get azure events metadata
        """
        yield "Let me fetch that for you"

        response = str(self._events_service.get_events_metadata())

        self.send_stream_request(msg.frm, io.BytesIO(str.encode(response)), name='response.xml',
                                 stream_type='application/text')

    @arg_botcmd('preset_query_name', type=str, default=None)
    @arg_botcmd('--app', type=str, unpack_args=False)
    @arg_botcmd('--barx', type=str, unpack_args=False)
    @arg_botcmd('--bary', type=str, unpack_args=False)
    @arg_botcmd('--scatterx', type=str, unpack_args=False)
    @arg_botcmd('--scattery', type=str, unpack_args=False)
    @arg_botcmd('--linex', type=str, unpack_args=False)
    @arg_botcmd('--liney', type=str, unpack_args=False)
    def get_azure_preset_query(self, msg, args):
        """
        Make azure insights query from presets
        """
        yield "Let me fetch that for you"

        old_appid = self._app_id
        old_appkey = self._app_key
        if args.app not in apps:
            yield "App name not in config file, proceeding with default."
        else:
            self._set_app(apps[args.name]["azure_app_id"], apps[args.name]["azure_app_key"])
            yield "Proceeding with " + args.app
        args.app = None

        response = self._query_service.get_preset_query(args.preset_query_name)

        self._handle_display(response, msg, args)

        if response is None:
            self.send_card(title=args.preset_query_name,
                           body="No such preset, use 'get azure query presets' to view all",
                           color="red",
                           in_reply_to=msg)
        else:
            self._handle_response(response, msg, args.preset_query_name)

        self._set_app(self, old_appid, old_appkey)

    @arg_botcmd('custom_query', type=str, default=None)
    @arg_botcmd('--app', type=str, unpack_args=False)
    @arg_botcmd('--barx', type=str, unpack_args=False)
    @arg_botcmd('--bary', type=str, unpack_args=False)
    @arg_botcmd('--scatterx', type=str, unpack_args=False)
    @arg_botcmd('--scattery', type=str, unpack_args=False)
    @arg_botcmd('--linex', type=str, unpack_args=False)
    @arg_botcmd('--liney', type=str, unpack_args=False)
    def get_azure_custom_query(self, msg, args):
        """
        Make custom azure insights query
        """
        yield "Let me fetch that for you"

        old_appid = self._app_id
        old_appkey = self._app_key
        if args.app not in apps:
            yield "App name not in config file, proceeding with default."
        else:
            self._set_app(apps[args.name]["azure_app_id"], apps[args.name]["azure_app_key"])
            yield "Proceeding with " + args.app
        args.app = None

        response = self._query_service.get_custom_query(args.custom_query)

        self._handle_display(response, msg, args)
        self._handle_response(response, msg, args.custom_query)

        self._set_app(self, old_appid, old_appkey)

    @botcmd
    def get_azure_query_presets(self, msg, args):
        response = self._query_service.get_all_presets_as_list()
        self.send_card(title="All available presets",
                       body='\n '.join(response),
                       color="green",
                       in_reply_to=msg)

    @arg_botcmd('query', type=str)
    @arg_botcmd('name', type=str)
    def add_azure_preset_query(self, msg, query: str, name: str):
        self._query_service.add_preset(query, name)
        yield "Done"

    def _set_color(self, response):
        if "error" in response:
            color = "red"
        else:
            color = "green"

        return color

    def _handle_response(self, response, msg, title):
        response_string = json.dumps(response, indent=4)
        if len(response_string) > 4000:
            self.send_stream_request(msg.frm, io.BytesIO(str.encode(response_string)), name='response.json',
                                     stream_type='application/text')
            return
        else:
            color = self._set_color(response)
            self.send_card(title=title,
                           body=json.dumps(response, indent=4),
                           color=color,
                           in_reply_to=msg)
            return

    def _handle_display(self, response, msg, args):
        channel = str(msg.frm).split("/")[0].split("#")[1]

        self._query_displayer.make_table(response, "plugins/AzureAPI/images/temp.png")
        self._api_service.send_image(os.path.abspath("plugins/AzureAPI/images/temp.png"), channel)

        if args.barx is not None and args.bary is not None:
            self._query_displayer.make_bargraph(response, "plugins/AzureAPI/images/temp.png", args.barx, args.bary)
            self._api_service.send_image(os.path.abspath("plugins/AzureAPI/images/temp.png"), channel)

        if args.scatterx is not None and args.scattery is not None:
            self._query_displayer.make_scatter(response, "plugins/AzureAPI/images/temp.png", args.scatterx,
                                               args.scattery)
            self._api_service.send_image(os.path.abspath("plugins/AzureAPI/images/temp.png"), channel)

        if args.linex is not None and args.liney is not None:
            self._query_displayer.make_line(response, "plugins/AzureAPI/images/temp.png", args.linex, args.liney)
            self._api_service.send_image(os.path.abspath("plugins/AzureAPI/images/temp.png"), channel)

    # Recursive method for finding the first instance of a key in a nested dict
    # Adapted from Stack Overflow:s https://tinyurl.com/y4qmzdj3
    def _find(self, target_key, dictionary):
        if target_key in dictionary: return dictionary[target_key]
        for _, value in dictionary.items():
            if isinstance(value, dict):
                return self._find(target_key, value)
