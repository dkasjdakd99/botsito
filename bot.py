import os
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
# Importar la vista para registrarla en el inicio
from cogs.verificacion import BotonVerificacion


TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ No se encontró DISCORD_TOKEN. Revisa tu archivo .env")

# Configuración de los permisos (Intents) obligatorios
intents = discord.Intents.default()
intents.message_content = True  
intents.members = True          


class MiBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Carga de cogs con manejo de errores individual
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'⚙️ Cog {filename} cargado exitosamente.')
                except Exception as e:
                    print(f'❌ Error cargando {filename}: {e}')

       
        self.add_view(BotonVerificacion())
        print("✅ Vista de verificación registrada como persistente.")

        
        try:
            synced = await self.tree.sync()
            print(f"🔄 Sincronizados {len(synced)} comando(s) de barra globalmente.")
        except Exception as e:
            print(f"❌ Error al sincronizar comandos: {e}")


bot = MiBot()


@bot.event
async def on_ready():
    print(f'------------------------------------')
    print(f'🤖 ¡Bot conectado con éxito!')
    print(f'👤 Nombre: {bot.user.name}#{bot.user.discriminator}')
    print(f'🆔 ID: {bot.user.id}')
    print(f'------------------------------------')


async def main():
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot detenido manualmente.")