from errbot import BotPlugin, botcmd, arg_botcmd, webhook, re_botcmd
import re

class Cookiecabot(BotPlugin):
    """
    Generate cookies
    """
        
    @re_botcmd(pattern=r"Give me cookies",prefixed=False, flags=re.IGNORECASE)
    def hand_out_cookies(self, msg, match):
        """
        Gives cookies to people who ask me nicely.

        """
        yield "Here's a cookie for you, {}".format(msg.frm)
        return