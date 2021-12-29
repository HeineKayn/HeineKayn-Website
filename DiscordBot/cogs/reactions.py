import discord
from discord.ext import commands

import json

class ReactCog(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        # ----------------- Modifiable
        self.guild = self.bot.get_guild(151453374909382657)
        self.channel = self.guild.get_channel(805086542891843625)

        try : 
            with open('./annexes/reaction.txt') as json_file:
                self.game_emoji_dic = json.load(json_file)

            self.original_id_list = []
            for message_id,_ in self.game_emoji_dic.items() :
                self.original_id_list.append(message_id)

        except : 
            self.game_emoji_dic =  {}
            self.original_id_list = []
            print("erreur, le dictionnaire de réaction n'a pas été trouvé")

        bot.loop.create_task(self.Init_Reaction())
    
    async def Init_Reaction(self):
        await self.bot.wait_until_ready()
        have_access = {}

        for originale_id in self.original_id_list:
            message = await self.channel.fetch_message(int(originale_id))

            for reaction in message.reactions : 

                emoji = reaction.emoji
                user_reacted = await reaction.users().flatten()
                have_access[emoji.name] = [x.id for x in user_reacted]

                channel_name = self.game_emoji_dic[originale_id][emoji.name]
                channel_cible = discord.utils.get(self.guild.channels, name=channel_name) 

                for member in user_reacted :
                    await channel_cible.set_permissions(member, read_messages=True)

        with open('./annexes/have_access.txt', 'w') as outfile:
            json.dump(have_access, outfile, indent=4)

    async def New_React(self,payload,adding):

        # on convertie les id en strin parce que le json aime pas les int dans les fichiers
        reacted_message_id = str(payload.message_id)
        user_id = str(payload.user_id)
        emoji = payload.emoji

        if reacted_message_id in self.original_id_list and emoji.name in self.game_emoji_dic[reacted_message_id].keys() :

            member = self.guild.get_member(int(user_id))
            type_give = self.game_emoji_dic[reacted_message_id]["type"]

            if type_give == "channel" : 
                channel_name = self.game_emoji_dic[reacted_message_id][emoji.name]
                await self.Update_Channel(adding,member,channel_name,emoji)

            elif type_give == "role" :
                # role_name = self.game_emoji_dic[reacted_message_id][emoji.name]
                # Update_Role(adding,member,role_name)
                pass

            else :
                "erreur"

    async def Update_Channel(self,adding,member,channel_name,emoji):

        channel = discord.utils.get(self.guild.channels, name=channel_name) 
        print("adding {}, person {}, channel {}".format(adding,member,channel_name))

        try : 
            with open('./annexes/have_access.txt') as json_file:
                have_access = json.load(json_file)

        except : 
            have_access =  {}

        if adding:
            if member.id not in have_access[emoji.name] :
                have_access[emoji.name].append(member.id)
                await channel.set_permissions(member, read_messages=True)
            else:
                print("déjà le rôle")
        if not adding:
            if member.id in have_access[emoji.name] :
                have_access[emoji.name].remove(member.id)
                await channel.set_permissions(member, read_messages=False)
            else:
                print("n'avait déjà pas")

        with open('./annexes/have_access.txt', 'w') as outfile:
            json.dump(have_access, outfile, indent=4)
                        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        await self.New_React(payload,True)
                
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        await self.New_React(payload,False)

def setup(bot):
    bot.add_cog(ReactCog(bot))