import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import aiohttp

client = commands.Bot(command_prefix = "_")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game ("Bonjour ! | Préfix : _"))
    print("Enregistré en tant que : ", client.user.name)
    print("ID : ", client.user.id)

@client.command()
async def ping(ctx):
    await ctx.send(f"Votre ping actuel est de : {round(client.latency * 500)}ms")

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount : int):
    if amount <= 1:
        await ctx.send("**Veuillez spécifier un montant plus élevé.**")
        await ctx.channel.purge(0)
        return
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Vous n'êtes pas autorisé à utiliser la commande clear.**")

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member:discord.Member = None, raison = None):
    if member == ctx.message.author:
        await ctx.channel.send("**Vous ne pouvez pas vous bannir vous même**")
        return
    if raison==None:
        raison = "**Raison-non-spécifiée.**"
    if not member:
        await ctx.send("**Veuillez spécifier un membre existant.**")
        return
    await member.ban()
    await ctx.send(f"{member.mention} **s'est fait bannir du serveur, avec pour raison : {raison}.**")
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Vous n'êtes pas autorisé à bannir.**")

@client.command()
@commands.has_permissions(administrator = True)
async def banlist(ctx):
        try:
            banlist = await ctx.guild.bans()
        except discord.errors.Forbidden:
            await ctx.send("**Vous n'avez pas accès à la liste des bannis**")
            return
        bancount = len(banlist)
        display_bans = []
        bans = None
        if bancount == 0:
            await ctx.send("**Il n'y a aucun de bannissements actifs.**")
        else:
            for ban in banlist:
                if len(", ".join(display_bans)) < 1800:
                    display_bans.append(str(ban.user))
                else:
                    bans = ", ".join(display_bans) + Language.get("moderation.banlist_and_more", ctx).format(len(banlist) - len(display_bans))
                    break
        if not bans:
            bans = ", ".join(display_bans)
        await ctx.send(("**Il y a actuellement {} bannissements actifs : **{}").format(bancount, bans))
@banlist.error
async def banlisterror(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Vous n'êtes pas autorisé à afficher la liste des bannis.**")



@client.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, name: str):
        bans = await ctx.message.guild.bans()
        member = discord.utils.get(bans, user__name=name)
        if member:
            await ctx.message.guild.unban(member.user)
            await ctx.send("{0.name}#{0.discriminator} **a été débanni du serveur.**".format(member.user))
            return
        await ctx.send("**Cet utilisateur n'est pas banni.**")

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("**Veuillez spécifer un membre existant.**")
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f"**{member.mention} a bien été mute.**")


@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("**Veuillez spécifier un membre existant.**")
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"**{member.mention} a été unmute.**")
    
@mute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("**Vous n'avez pas l'autorisation de unmute/mute.**")
        return
    

client.run("NjAwNTAxNDk0NTc1Mzk4OTEy.XS0rJw.9p1yglWgZ6OALLBvh6_rGOFgUZY")
