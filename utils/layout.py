import discord

from discord import ui
from utils.maps import ACTION_EMOTES

class SimpleAction(discord.ui.LayoutView):
    def __init__(self, message_type: str, action_output: str, emote: str = '', failure: bool = False):
        super().__init__(timeout=None)

        if not emote:
            if failure:
                emote = ':no_entry_sign'
            else:
                emote = ACTION_EMOTES.get(message_type, '')

        container = ui.Container(accent_color = 0x9a316c)
        container.add_item(ui.TextDisplay(f"{emote} {action_output}"))
        self.add_item(container)

# class CV2(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot
    
#     @app_commands.command(name = "faketake")
#     @app_commands.describe(player_name = "The name of the player.")
#     @app_commands.describe(item_name = "The name of the item.")
#     @app_commands.describe(weight = "The item's weight.")
#     @app_commands.describe(wearable = "Whether or not the item is wearable.")
#     @app_commands.describe(desc = "The description of the item.")
#     async def layout(self, interaction: discord.Interaction, player_name: str, item_name: str, weight: int, wearable: bool, desc: str):
#         await interaction.response.send_message(view = Layout(player_name, item_name, weight, wearable, desc))

# async def setup(bot: commands.Bot):
#     await bot.add_cog(CV2(bot))