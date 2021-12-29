from discord.ext import commands, ipc
import aiohttp

from .tools import *

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configPath = "../web_data/config.txt"

    @ipc.server.route()
    async def get_config(self,data):

        botid = str(self.bot.user.id)
        try : 
            with open(self.configPath) as json_file:
                old_config = json.load(json_file)
                config = old_config[botid]
        except:
            config = {}

        return config

    @ipc.server.route()
    async def set_config(self,data):
        dic = data.config
        botid = str(self.bot.user.id)

        try :
            with open(self.configPath) as json_file:
                old_config = json.load(json_file)
                config = old_config[botid] 
        except :
            config = {}

        for key,val in dic.items():

            if (key in config and config[key] != val) or key not in config :
                config[key] = val

                if key == "pseudo":
                    await self.bot.user.edit(username=val)

                elif key == "avatar":
                    async with aiohttp.ClientSession() as session:
                        async with session.get(val) as response:
                            img = await response.read()
                            await self.bot.user.edit(avatar=img)

        with open(self.configPath, 'w') as outfile: 
            old_config[botid] = config
            json.dump(old_config, outfile, indent=4)
        
        return config
            
def setup(bot):
    bot.add_cog(Config(bot))