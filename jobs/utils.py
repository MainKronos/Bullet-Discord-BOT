import asyncio, discord
import config
from datetime import datetime, timedelta
from jobs.bot import bot
import json

async def check_death(): # Controlla se il tempo di attesa di tutte le persone morte è finito
	member_chace = []

	for guild_id in config.KILLED:
		for member_id in config.KILLED[guild_id]:
			killData = check_death_member(guild_id, member_id)
			if isinstance(killData, dict):
				member_chace.append(killData)
	else:
		for killData in member_chace:
			guild_id = killData["guild_id"]
			member_id = killData["member_id"]
			channel_id = killData["channel_id"]

			remove_member_killed(guild_id, member_id)

			await toggle_killed_role(guild_id, member_id) # rimuove il ruolo ☠️┇Dead per ⛩| Holy Quindecimᴵᵗᵃ

			await send_respawn(member_id, channel_id)


async def toggle_killed_role(guild_id, member_id): # aggiunge  o toglie il ruolo ☠️┇Dead per la guild ⛩| Holy Quindecimᴵᵗᵃ
	if guild_id == 792523466040803368: # ⛩| Holy Quindecimᴵᵗᵃ
		await toggle_role(guild_id=guild_id, member_id=member_id, role_id=826176265060483132)

async def toggle_role(guild_id, member_id, role_id): # aggiunge o toglie un ruolo
	guild = bot.get_guild(guild_id)
	member = guild.get_member(member_id)
	kill_role = guild.get_role(role_id)

	if kill_role in member.roles:
		await member.remove_roles(kill_role)
		print(kill_role, "tolto a", member)
	else:
		await member.add_roles(kill_role)
		print(kill_role, "aggiunto a", member)


def remove_member_killed(guild_id, member_id): # Rimuove un membro da dalla lista dei morti
	config.KILLED[guild_id].pop(member_id)

async def send_respawn(member_id, channel_id): # Invia la notifica di respawn
	channel = bot.get_channel(channel_id)

	embed = discord.Embed(
		colour = discord.Colour.teal()
	)
	embed.add_field(name="RESPAWN", value=f"L'utente <@{member_id}> è rinato.", inline=False)
	await channel.send(embed=embed)

def check_death_member(guild_id, member_id): # Controlla se una persona è morta

	if guild_id not in config.KILLED:
		return

	if member_id not in config.KILLED[guild_id]:
		return

	time = config.KILLED[guild_id][member_id]["time"]
	delta = config.KILLED[guild_id][member_id]["delta"]

	if datetime.now() >= (time + delta):
		channel_id = config.KILLED[guild_id][member_id]["channel"]

		return {
			"guild_id": guild_id,
			"member_id": member_id,
			"channel_id": channel_id
		}

### BANNATI ###

def load_banned(): # Carica le persone bannate all'avvio
	with open('json/banned.json', 'r') as f:
		config.BANNED = set(json.loads(f.read()))

def add_banned(ID): # aggiunge una persona bannata
	config.BANNED.add(ID)
	with open('json/banned.json', 'w') as f:
		f.write(json.dumps(list(config.BANNED), indent='\t'))