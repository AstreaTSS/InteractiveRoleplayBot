import typing

from discord.ext import commands
from discord import app_commands
import discord

import utils.data as data
import utils.helpers as helpers
import utils.autocompletes as autocompletes

class LockGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="lock", description="Lock an object or exit.")

    #region /lock object
    @app_commands.command(name = "object", description = "Lock an object in the current room using a key from your inventory.")
    @app_commands.describe(object_name = "The name of the object you wish to lock.")
    @app_commands.describe(key_name = "The name of the item in your inventory that can lock the object.")
    @app_commands.autocomplete(object_name=autocompletes.object_autocomplete, key_name=autocompletes.user_items_autocomplete)
    async def lockobject(self, interaction: discord.Interaction, object_name: str, key_name: str):
        # Get the player and room class objects for this interaction
        player = helpers.get_player_from_id(interaction.user.id)
        current_room = helpers.get_room_from_id(interaction.channel_id)

        # Validate the interaction and handle smart autocomplete cases
        if await helpers.check_valid_player(interaction, player):
            return
        if await helpers.handle_smart_autocomplete(interaction, key_name, object_name):
            return
        searched_obj = await helpers.check_obj_container(interaction, current_room, object_name, player, False, False)
        if searched_obj is None:
            return

        # Defer the response while processing the code
        await interaction.response.defer(thinking=True)
        
        # Locking logic, send confirmation message
        return await helpers.set_lock(interaction, searched_obj, True, player, player.get_items(), key_name, "lockobject")
    #endregion
    #region /lock exit
    @app_commands.command(name = "exit", description = "Locks an exit connected to the current room using a key from your inventory.")
    @app_commands.describe(exit_name = "The name of the exit you wish to lock.")
    @app_commands.describe(key_name = "The name of the item in your inventory that can lock the exit.")
    @app_commands.autocomplete(exit_name=autocompletes.exit_name_autocomplete, key_name=autocompletes.user_items_autocomplete)
    async def lockexit(self, interaction: discord.Interaction, exit_name: str, key_name: str):
        player = helpers.get_player_from_id(interaction.user.id)
        current_room = helpers.get_room_from_id(interaction.channel_id)

        # Validate the interaction
        if await helpers.check_valid_player(interaction, player):
            return        
        
        # Get the exits
        exit = await helpers.get_exit(interaction, current_room, exit_name)
        if exit is None:
            return
        exit_room = helpers.get_room_from_name(exit_name)
        
        # Defer the response while processing the code
        await interaction.response.defer(thinking=True)

        # Locking logic, send confirmation message
        return await helpers.set_lock(interaction, exit, True, player, player.get_items(), key_name, "lockexit", current_room, exit_room)
    #endregion

class UnlockGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="unlock", description="Unlock an object or exit.")

    #region /unlock object
    @app_commands.command(name = "object", description = "Unlock an object in the current room using a key from your inventory.")
    @app_commands.describe(object_name = "The name of the object you wish to unlock.")
    @app_commands.describe(key_name = "The name of the item in your inventory that can unlock the object.")
    @app_commands.autocomplete(object_name=autocompletes.object_autocomplete, key_name=autocompletes.user_items_autocomplete)
    async def unlockobject(self, interaction: discord.Interaction, object_name: str, key_name: str):
        # Get the player and room class objects for this interaction
        player = helpers.get_player_from_id(interaction.user.id)
        current_room = helpers.get_room_from_id(interaction.channel_id)

        # Validate the interaction and handle smart autocomplete cases
        if await helpers.check_valid_player(interaction, player):
            return
        if await helpers.handle_smart_autocomplete(interaction, key_name, object_name):
            return
        searched_obj = await helpers.check_obj_container(interaction, current_room, object_name, player, False, False)
        if searched_obj is None:
            return

        # Defer the response while processing the code
        await interaction.response.defer(thinking=True)
        
        # Unlocking logic, send confirmation message
        return await helpers.set_lock(interaction, searched_obj, False, player, player.get_items(), key_name, "unlockobject")
        return
    #endregion
    #region /unlock exit
    @app_commands.command(name = "exit", description = "Unlock an exit connected to the current room using a key from your inventory.")
    @app_commands.describe(exit_name = "The name of the exit you wish to unlock.")
    @app_commands.describe(key_name = "The name of the item in your inventory that can unlock the exit.")
    @app_commands.autocomplete(exit_name=autocompletes.exit_name_autocomplete, key_name=autocompletes.user_items_autocomplete)
    async def unlockexit(self, interaction: discord.Interaction, exit_name: str, key_name: str):
        player = helpers.get_player_from_id(interaction.user.id)
        current_room = helpers.get_room_from_id(interaction.channel_id)

        # Validate the interaction
        if await helpers.check_valid_player(interaction, player):
            return        
        
        # Get the exits
        exit = await helpers.get_exit(interaction, current_room, exit_name)
        if exit is None:
            return
        exit_room = helpers.get_room_from_name(exit_name)
        
        # Defer the response while processing the code
        await interaction.response.defer(thinking=True)

        # Unlocking logic, send confirmation message
        return await helpers.set_lock(interaction, exit, False, player, player.get_items(), key_name, "unlockexit", current_room, exit_room)
    #endregion

class LockCMDs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.tree.add_command(LockGroup())
        self.bot.tree.add_command(UnlockGroup())

async def setup(bot: commands.Bot):
    await bot.add_cog(LockCMDs(bot))