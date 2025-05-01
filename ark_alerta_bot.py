import discord
import valve.source.a2s
import asyncio
import time

# Tu token del bot de Discord
DISCORD_BOT_TOKEN = "MTM2NzUxNjA5NTEwMzM2OTIzNg.GGpXT6.xBv5AocxISgH8kxMV-xNQA866kY8J4zvLpDbVM"

# ID del canal donde el bot enviará los mensajes
DISCORD_CHANNEL_ID = 1367495176788119572

# Dirección de tu servidor ARK
SERVER_ADDRESS = ("188.213.7.147", 27021)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

jugadores_anteriores = {}  # Usaremos un diccionario para guardar el tiempo de conexión

@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")
    canal = client.get_channel(DISCORD_CHANNEL_ID)

    global jugadores_anteriores

    while True:
        try:
            with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
                players = server.players()
                jugadores_actuales = {p["name"]: p["duration"] for p in players["players"]}

                # Detectamos nuevos jugadores (conexión)
                nuevos = jugadores_actuales.keys() - jugadores_anteriores.keys()

                # Detectamos jugadores que se han ido (desconexión)
                desconectados = jugadores_anteriores.keys() - jugadores_actuales.keys()

                # Enviar mensajes para nuevos jugadores (entraron)
                for jugador in nuevos:
                    if jugador:
                        mensaje = f"🚨 **Enemigo detectado:** `{jugador}` se conectó a ARK"
                        await canal.send(mensaje)

                # Enviar mensajes para jugadores que se desconectaron
                for jugador in desconectados:
                    if jugador:
                        tiempo_conectado = jugadores_anteriores[jugador]
                        mensaje = f"👋 **Jugador desconectado:** `{jugador}` se desconectó después de {int(tiempo_conectado)} segundos en el servidor."
                        await canal.send(mensaje)

                # Actualizamos el diccionario de jugadores
                jugadores_anteriores = jugadores_actuales

        except Exception as e:
            print("Error al consultar el servidor:", e)

        await asyncio.sleep(30)

client.run(DISCORD_BOT_TOKEN)
