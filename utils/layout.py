import discord

from discord import ui
from utils.maps import ACTION_EMOTES

class SimpleAction(discord.ui.LayoutView):
    def __init__(self, message_type: str, action_output: str, emote: str = '', player_failure: bool = False, command_failure: bool = False):
        super().__init__(timeout=None)

        if emote == '':
            # A 'player failure' should be used when the player uses a command correctly, 
            # just not where it's supposed to be used - the logic, the player just needs to do something different
            # ex: locking an already locked door, trying to pick up an item with a full inventory
            if player_failure:
                emote = ':exclamation:'
            # A 'command failure' should be used when the player uses a command incorrectly.
            # ex: trying to pick up an item that doesn't exist, trying to look inside of an object that's not a container
            elif command_failure:
                emote = ':question:'
            else:
                emote = ACTION_EMOTES.get(message_type, '')

        container = ui.Container(accent_color = 0x9a316c)
        container.add_item(ui.TextDisplay(f"{emote} {action_output}"))
        self.add_item(container)