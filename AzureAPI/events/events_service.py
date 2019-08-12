from typing import Iterable

import json

from abstracts.abstract_api_interface import AbstractAPIInterface


class EventsService:

    def __init__(self, api_service: AbstractAPIInterface):
        self._api_service = api_service

    def get_event(self, args_provided: dict) -> Iterable[str]:
        if args_provided.event_type is None:
            return "Please provide an event ID"

        args_copy_without_eventtype = vars(args_provided).copy()
        args_copy_without_eventtype.pop('event_type', None)
        args_copy_without_eventtype.pop('event_id', None)

        # Some formatting for arguments dict
        new_args_dict = {}
        for key, value in args_copy_without_eventtype.items():
            if key != "timespan":
                new_args_dict["$"+key] = value
            else:
                new_args_dict[key] = value

        # Special case: event_id
        id = args_provided.event_type
        if args_provided.event_id is not None:
            id += "/" + args_provided.event_id
            new_args_dict = None

        raw_json = self._api_service.make_get_request("events", id, new_args_dict)
        return raw_json


    def get_events_metadata(self):

        raw_response = self._api_service.make_get_request("events", "$metadata", None)

        return raw_response