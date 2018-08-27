/* MIT License

Copyright (c) 2018 <ADD UR NAME HERE NAIA>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. */


import discord
from discord.ext.commands import Bot
import asyncio
import random
import datetime

prefix = '..'

client = Bot("..")

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print('-------')
    game = discord.Game(name="Type ..help")
    await client.change_presence(game= game)

@client.command(pass_context=True)
async def ping(ctx):
    return await client.say('Pong! {0}'.format())

@client.command(pass_context = True)
async def clear(ctx, number):
    if not ctx.message.author.server_permissions.administrator:
        return
    msg = []
    number = int(number) + 1
    async for x in client.logs_from(ctx.message.channel, limit = number):
        msg.append(x)
    await client.delete_messages(msg)
    mg = await client.say('**You have deleted {} messages.**'.format(number - 1))

    await asyncio.sleep(3)
    await client.delete_message(mg)

@client.command(pass_context = True)
async def autorole(ctx, role: discord.Role = None, aliases=["ar"]):
    if not role:
        return await client.say("That is not a valid role.")

    if not ctx.message.author.server_permissions.administrator and ctx.message.author.id != "your_id":
        return

    with open("autorole_servers/{}.txt".format(ctx.message.server.id), 'w') as file:
        file.write(role.id)

    emb = discord.Embed(description = "Successfully set **{}** as the auto-role for this server.".format(role.name), color = discord.Color.green())
    return await client.say(embed = emb)

@client.event
async def on_member_join(member):
    import os
    servers = os.listdir("autorole_servers")
    if member.server.id + ".txt" in servers:
        with open("autorole_servers/{}.txt".format(member.server.id)) as file:
            role_id = file.read()

            role = discord.utils.get(member.server.roles, id=role_id)
            if not role:
                return
            await client.add_roles(member, role)

@client.command(pass_context = True)
async def kick(ctx, *, member : discord.Member = None):
    if not ctx.message.author.server_permissions.ban_members:
        return

    if not member:
        return await client.say(ctx.message.author.mention + " **Specify a user to kick!**")
    try:
        await client.kick(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")

    embed = discord.Embed(description = "**%s** has been kicked!"%member.name, color = 0xFF0000)
    return await client.say(embed = embed)

@client.command()
async def help(aliases = ["h"]):
    embed = discord.Embed(title = "Help Commands", color = discord.Color.purple())
    embed.add_field(name = "..admin", value = "Shows the admin commands", inline = False)
    embed.add_field(name = "..sroles help", value = "Commands for self roles", inline=False)
    embed.add_field(name = "..flipcoin", value = "Head or Tails???", inline=False)
    embed.add_field(name= "..invite", value = "Link to invite Dev", inline=False)
    embed.add_field(name = "..server", value = "Shows information about the server", inline=False)
    
    embed.set_footer(text = "Type %saliases"%prefix)
    await client.say(embed = embed)

@client.command(pass_context = True)
async def admin(ctx, *, member : discord.Member = None):
    if not ctx.message.author.server_permissions.administrator:
        return
    embed = discord.Embed(title = "Admin Commands", color = discord.Color.dark_magenta())
    embed.add_field(name = "..kick <@user>", value = "Kicks a specified user from the server", inline=False)
    embed.add_field(name = "..clear <number>", value = "Purges messages from the channel", inline = False)
    embed.add_field(name = "..autorole <@role>", value = "Automatically sets a role as user joins", inline = False)
    embed.add_field(name = "..ban <@user>", value = "Bans a user from the server", inline=False)
    embed.add_field(name = "..unban <user ID>", value = "Unbans a user from the server", inline=False)
    await client.say(embed = embed)

@client.command(pass_context=True)
async def rules(ctx, *, member : discord.Member = None):
    if not ctx.message.author.server_permissions.administrator:
        return

    embed = discord.Embed(title = "Dev's Hideout Rules", color = discord.Color.orange())
    embed.add_field(name = "➤ Respect everyone", value = "Everyone deserves the same amount of respect on this server. If caught being disrespectful, staff will take action.", inline=False)
    embed.add_field(name = "➤ No spamming", value = "Do not spam in any channel. There may be a channel for that.", inline = False)
    embed.add_field(name = "➤ NO ADVERTISING", value = "Advertising is not allowed. This includes sharing Discord servers, youtube/twitch, or any websites. Doing so may result in a ban from this server.", inline = False)
    embed.add_field(name = "➤ Post appropriate content in the respected channels.", value = "General talk goes in #general, pictures goes in #media, bot commands goes in #testing, etc", inline=False)
    embed.add_field(name = "➤ No drama", value = "Please refrain from causing any drama in this server. Take that to the dms.", inline=False)
    embed.add_field(name = "➤ No asking for roles", value = "Asking for your own role or a role higher than the one you're given will result in a kick from the server.", inline=False)
    await client.say(embed = embed)

@client.group(pass_context = True)
async def sroles(ctx):
    message = ctx.message
    if message.content != "%ssroles"%prefix:
        return
    try:
        with open("self_role_servers/%s.txt"%message.server.id) as file:
            data = file.readlines()
            data = '➤'.join(data)
            if not data:
                data = "---None---"
                
            embed = discord.Embed(title = "Self roles list:", description = data, color = 0xFFFFF)
            embed.set_footer(text = "Type %siam <role> to receieve that role!"%prefix)
        return await client.say(embed = embed)
    except Exception as e:
        embed = discord.Embed(title = "Self roles list:", description = "---None---", color = 0xFFFFF)
        return await client.say(embed = embed)

@sroles.command()
async def help():
    embed = discord.Embed(title="Help: Self Roles", color = discord.Color.teal())
    embed.add_field(name="..iam", value = "Assings a self role to the user", inline = False)
    embed.add_field(name = "..iamnot", value = "Removes a self role from the user", inline=False)
    embed.add_field(name="..sroles", value = "Shows the self assignable roles in this server", inline = False)
    await client.say(embed=embed)
    

@client.command(pass_context = True)
async def iam(ctx, *role):
    message = ctx.message
    role = ' '.join(role)
    found = False

    for x in message.server.roles:
        if x.name.lower() == role.lower():
            item = x
            found = True
    if not found:
        embed = discord.Embed(description = "Role **%s** does not exist!"%role, color = discord.Color.red())
        return await client.say(embed = embed)

    try:
        with open("self_role_servers/%s.txt"%message.server.id) as file:
            role_list = file.readlines()
            print(role_list)

            if role.lower() not in [x.lower().strip() for x in role_list]:
                return await client.say(embed = discord.Embed(description = "That is not a self assignable role. Use %ssroles to view the list of self assignable roles"%prefix,
                                                              color = discord.Color.red()))
            await client.add_roles(message.author, item)
            return await client.say(embed = discord.Embed(description = "You now have the **%s** role!"%role, color = 0xFFFFF))

    except Exception as e:
        print("Err was here: " + e)
        if 'No such file or directory' in str(e):
            return await client.say(embed = discord.Embed(description = "That is not a self assignable role. Use %ssroles to view the list of self assignable roles"%prefix,
                                                              color = discord.Color.red()))
        
        else:
            return print(e)

@client.command(pass_context = True)
async def iamnot(ctx, *role):
    message = ctx.message
    role = ' '.join(role)
    found = False

    role = discord.utils.get(message.server.roles, name=role)
    if not role:
        embed = discord.Embed(description = "Role **%s** does not exist in this server!"%role, color = discord.Color.red())
        return await client.say(embed = embed)

    try:
        if role.name.lower() not in [x.name.lower() for x in message.author.roles]:
            return await client.say(embed = discord.Embed(description = "You do not have that role!", color = discord.Color.red()))
        
        with open("self_role_servers/%s.txt"%message.server.id) as file:
            role_list = file.readlines()
            print(role_list)
            if role.name.lower() not in [x.lower().replace("\n", "") for x in role_list]:
                return await client.say(embed = discord.Embed(description = "That is not a self assignable role. Use %ssroles to view the list of self assignable roles"%prefix,
                                                              color = discord.Color.red()))
            await client.remove_roles(message.author, role)
            return await client.say(embed = discord.Embed(description = "**%s** role has now been removed from you!"%role, color = 0xFFFFF))

    except Exception as e:
        print(e)
        if 'No such file or directory' in str(e):
            return await client.say(embed = discord.Embed(description = "That is not a self assignable role. Use %ssroles to view the list of self assignable roles"%prefix,
                                                              color = discord.Color.red()))
        
        else:
            return print(e)

@client.command(pass_context = True, aliases=["fc"])
async def flipcoin(ctx, *, member : discord.Member = None):
    pick = [' heads', ' tails']
    flip = random.choice(pick)
    await client.say(ctx.message.author.mention + flip + '!')

@client.command(pass_context = True, aliases=["inv"])
async def invite(ctx):
    await client.say('**Invite me!** :link: https://discordapp.com/oauth2/authorize?client_id=310278408107982848&scope=bot&permissions=2115501311 :link:')

@client.command(pass_context = True, aliases=["sinfo"])
async def server(ctx):
    server = ctx.message.server;
    roles = [x.name for x in server.role_hierarchy];
    role_length = len(roles);

    embed = discord.Embed(color = 0x0000FF)
    embed.set_thumbnail(url = server.icon_url)
    embed.set_author(name = str(server.name))
    embed.add_field(name = "Member Count", value = server.member_count, inline=True)
    embed.add_field(name = "Server ID", value = str(server.id), inline=True)
    embed.add_field(name = "Server Owner", value = str(server.owner), inline=True)
    embed.add_field(name = "Server Owner ID", value = str(server.owner.id), inline=True)
    embed.add_field(name = "Server Region", value = '%s'%str(server.region), inline=True)
    embed.add_field(name = "Verification Level", value = (server.verification_level), inline=True)
    embed.add_field(name = "Created on", value = server.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"), inline=False)
    await client.say(embed = embed)

@client.command(pass_context = True)
async def ban(ctx, *, member : discord.Member = None):
    if not ctx.message.author.server_permissions.administrator:
        return

    if not member:
        return await client.say(ctx.message.author.mention + " Specify a user to ban!")
    try:
        await client.ban(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")

    embed = discord.Embed(description = "**%s** has been banned!"%member.name, color = 0xFF0000)
    return await client.say(embed = embed)

@client.command(pass_context = True)
async def mute(ctx, member: discord.Member):
    if ctx.member.author.server_permissions.administrator:
        role = disocrd.utils.get(member.server.roles, name = 'Muted')
        await client.add_roles(member, role)
        embed = discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**.".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="Permission Denied.", decription="You do no have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def unban(ctx, userID):
    if not ctx.message.author.server_permissions.administrator:
        return

    if not userID:
        return await client.say(ctx.message.author.mention + " Specify a user's id to unban!")

    try:
        user = await client.get_user_info(userID)
        await client.unban(ctx.message.server, user)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")
        else:
            return await client.say("ERROR UNBANNING: " + str(e))
        

    embed = discord.Embed(description = "**%s** has been unbanned from the server!"%user.name, color = 0xFF0000)
    return await client.say(embed = embed)

@sroles.command(pass_context = True)
async def delete(ctx, *role):
    found = False
    role = ' '.join(role)
    message = ctx.message

    if not role:
        return await client.say("**Correct usage:**\n%ssroles delete <role>")

    for x in message.server.roles:
        if x.name == role:
            item = x
            found = True
    if not found:
        embed = discord.Embed(description = "Role **%s** does not exist!"%role, color = discord.Color.red())
        return await client.say(embed = embed)

    try:
        with open("self_role_servers/%s.txt"%message.server.id, 'r+') as file:
            data = file.readlines()
            data = [x.replace('\n', '') for x in data]

            if role not in data:
                return await client.say(embed = discord.Embed(description = "There is no such role in the list of self roles. Type %ssroles to see"%prefix+
                                        " the list of currently available self assignable roles for this server.", color = discord.Color.red()))
            trash = data.pop(data.index(role))
            file.seek(0)
            file.write('\n'.join(data))
            file.truncate()

            return await client.say(embed = discord.Embed(description = "Successfully deleted role **%s** from self assignable roles!"%role, color = discord.Color.green()))
    except Exception as e:
        if e.strerror == 'No such file or directory':
            return await client.say(embed = discord.Embed(description = "That role has not been added to the list of self assignable roles.", color = discord.Color.red()))

@sroles.command(pass_context = True)
async def add(ctx, *role):
    found = False
    role = ' '.join(role)
    message = ctx.message

    if not role:
        return await client.say("**Correct usage:**\n%ssroles delete <role>")
    
    for x in message.server.roles:
        if x.name == role:
            item = x
            found = True
            
    if not found:
        embed = discord.Embed(description = "Role **%s** does not exist!"%role, color = discord.Color.red())
        return await client.say(embed = embed)

    try:
        with open("self_role_servers/%s.txt"%message.server.id, 'a') as file:
            file.write("\n" + role)
            
    except Exception as e:
        if e.strerror == 'No such file or directory':
            import os
            os.mkdir("self_role_servers")
            with open("self_role_servers/%s.txt"%message.server.id, 'a') as file:
                file.write("\n" + role)
                
        else:
            return print("ERR: " + e)
            
    embed = discord.Embed(description = "Successfully added role **%s** to the list of self assignable roles!"%role, color = discord.Color.green())
    return await client.say(embed = embed)

@client.command(pass_context = True)
async def aliases(ctx):
    embed = discord.Embed(title="Aliases", color = discord.Color.dark_green())
    embed.add_field(name="..flipcoin", value = "..fc", inline = False)
    embed.add_field(name="..autorole", value = "..ar", inline = True)
    embed.add_field(name="..invite", value = "..inv", inline =False)
    await client.say(embed = embed)

@client.command()
async def allcommands():
    if not ctx.message.author.server_permissions.administrator:
        return
    embed = discord.Embed(title="All Commands", color = discord.Color.to_tuple())
    embed.add_field(name = "..ping", value = None, inline = False)
    embed.add_field(name = "..clear", value = None, inline =False)
    embed.add_field(name = "..autorole", value = None, inline=False)
    embed.add_field(name = "..")
    await client.say(embed = embed)

@client.command(pass_context = True, aliases = ["ui"])
async def userinfo(ctx, *, member : discord.Member = None):
    message = ctx.message
    user = message.mentions[0]

    embed = discord.Embed(color = 0xFF0000)
    embed.set_author(name= str(user.name), icon_url = user.avatar_url)
    embed.add_field(name="Nickname", value = user.nick, inline=True)
    embed.add_field(name = "User ID", value = str(user.id), inline=True)
    embed.add_field(name = "Status", value = str(member.status), inline=False)
    embed.add_field(name = "Joined Guild", value = user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S"), inline = False)
    embed.add_field(name = "Joined Discord", value = user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S"), inline = True)
    await client.say(embed = embed)

@client.command(pass_context = True, aliases=['av'])
async def avatar(ctx, *, member: discord.Member = None):
    icon_url = user.avatar_url
    if ".gif" in icon_url:
        av += "&f=.gif"
    embed = discord.Embed(icon_url, color=0xffffff)
    embed.set_author(name=str(member))
    embed.set_image(url = member.avatar_url)
    await client.say(embed=em)
    
@client.command(pass_context = True)
async def user(ctx, *, member: discord.Member = None):
    message = ctx.message
    user = message.mentions[0]
    
    embed = discord.Embed(color = discord.Color.blue())
    embed.set_image(url = user.avatar_url)
    embed.set_author(name = str(user.name), icon_url = user.avatar_url)
    embed.add_field(name = "Joined Guild", value = user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S"), inline = False)
    embed.add_field(name = "Joined Discord", value = user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S"), inline = True)
    embed.add_field(name = "User ID", value = str(user.id), inline=True)
    embed.add_field(name = "Status", value = member.status, inline=True)
    await client.say(embed = embed)
   
client.run('Bot Token')
