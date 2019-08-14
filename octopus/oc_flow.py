from errbot import botflow, FlowRoot, BotFlow, FLOW_END

class OctopusFlows(BotFlow):

    @botflow
    def script(self, flow: FlowRoot):
        self.start(flow, 'octopus_run')
        self.start(flow, 'octopus_predefined_run')

    def start(self, flow, name):
        request_started = flow.connect(name, auto_trigger=True)
        request_started.connect('cancel')
        request_started.connect('deploy_to')        
        ask_param = request_started.connect('param')
        ask_param.connect(ask_param)
        ask_param.connect('cancel')
        ask_param.connect('deploy_to')