from errbot import BotPlugin, botcmd, arg_botcmd, webhook
import datetime

class Playground(BotPlugin):
    """
    A plugin testing playground
    """

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def example(self, message, args):
        """A command which simply returns 'Example'"""
        return "Example"

    @arg_botcmd('name', type=str)
    @arg_botcmd('--favorite-number', type=int, unpack_args=False)
    def hello(self, message, args):
        """
        A command which says hello to someone.

        If you include --favorite-number, it will also tell you their
        favorite number.
        """
        if args.favorite_number is None:
            return f'Hello {args.name}.'
        else:
            return f'Hello {args.name}, I hear your favorite number is {args.favorite_number}.'
        
    @arg_botcmd('--secret', dest='secret', type=str)
    def howareyou(self, message, secret=None):
        print(secret)
        if secret == "open_seasame":
            return "Secret!"
        return "I'm great!"
    
    @botcmd
    def show_date(self, mesasge, args):

        return datetime.datetime.today().strftime('%Y-%m-%d')
    
    @botcmd
    def show_time(self, message, args):
        return datetime.datetime.now().time()
