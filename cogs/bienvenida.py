import os
import discord
from discord import app_commands
from discord.ext import commands

# ⚙️ CONFIGURACIÓN
# ID del canal donde se enviará el mensaje de bienvenida
CANAL_BIENVENIDA_ID = os.getenv("CANAL_BIENVENIDA")
# ID del canal de reglas (para mencionarlo dentro del mensaje)
CANAL_REGLAS_ID = os.getenv("CANAL_REGLAS")
# URL de la imagen/gif de bienvenida (podés poner una URL directa a un .gif o .png)
IMAGEN_BIENVENIDA_URL = "https://i.imgur.com/XWufGs8.gif"


class Bienvenida(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def construir_embed(self, member: discord.Member) -> discord.Embed:
        """Arma el embed de bienvenida para un miembro dado. Reutilizado
        tanto por on_member_join como por el comando /prueba_bienvenida."""
        # Mención al canal de reglas (si está configurado, si no, texto plano)
        mencion_reglas = f"<#{CANAL_REGLAS_ID}>" if CANAL_REGLAS_ID else "nuestras reglas"

        # Cantidad de miembros actuales del servidor
        total_miembros = member.guild.member_count

        embed = discord.Embed(
            title="Bienvenid@ a monitos! ( ˶ˆᗜˆ˵ )",
            description=(
                f"Hola {member.mention}! Recuerda leer {mencion_reglas} "
                f"para evitar ser sancionad@. Esperamos que pases un buen rato "
                f"en nuestro servidor 😊"
            ),
            color=discord.Color.purple(),
        )
        embed.set_image(url=IMAGEN_BIENVENIDA_URL)
        embed.set_footer(
            text=f" ahora somos {total_miembros} usuarios! :o",
            icon_url=member.guild.icon.url if member.guild.icon else None,
        )
        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Validar que el canal esté configurado
        if not CANAL_BIENVENIDA_ID:
            print("⚠️ CANAL_BIENVENIDA no está configurado en el .env")
            return

        canal = self.bot.get_channel(int(CANAL_BIENVENIDA_ID))
        if canal is None:
            print(f"⚠️ No se encontró el canal con ID {CANAL_BIENVENIDA_ID}")
            return

        embed = self.construir_embed(member)
        await canal.send(embed=embed)

    @app_commands.command(
        name="prueba_bienvenida",
        description="Envía un mensaje de bienvenida de prueba en este canal",
    )
    @app_commands.default_permissions(administrator=True)  
    @app_commands.checks.has_permissions(administrator=True)
    async def prueba_bienvenida(self, interaction: discord.Interaction):
        # Usamos al usuario que ejecuta el comando como "miembro de prueba"
        embed = self.construir_embed(interaction.user)

        # Respondemos primero de forma efímera (solo la ve quien usó el comando)
        await interaction.response.send_message(
            "✅ Enviando mensaje de prueba...", ephemeral=True
        )
        # Y mandamos el embed real al canal, visible para todos
        await interaction.channel.send(embed=embed)
        
    @prueba_bienvenida.error
    async def reglas_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
            if isinstance(error, app_commands.MissingPermissions):
                await interaction.response.send_message(
                    "🚫 No tenés permiso para usar este comando (solo administradores).",
                    ephemeral=True,
            )
            else:
                raise error

async def setup(bot: commands.Bot):
    await bot.add_cog(Bienvenida(bot))
