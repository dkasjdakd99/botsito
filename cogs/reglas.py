import discord
from discord import app_commands
from discord.ext import commands

# ⚙️ CONFIGURACIÓN
# Editá el texto de cada regla acá abajo
REGLAS = [
    "**Respeta a los demás**: Sé amable. No se tolerará el acoso, los insultos, la discriminación (ya sea por género, orientación, religión, etc.) ni los discursos de odio. Queremos que este sea un espacio agradable para todos",
    "**Se prohibe el contenido +18 (NSFW)**: Queda estrictamente prohibido compartir imágenes, videos o texto con contenido explícito, sangriento o sexual." ,
    "**Usa correctamente los canales**: Cada canal tiene un propósito, usalos correctamente *(recuerda revisar las descripciones! 😉)*. ",
    "**Se prohibe el Spam y las promociones no autorizadas**: Evita llenar los canales con mensajes repetitivos y/o mayúsculas excesivas. Tampoco envíes enlaces de tus redes o servidores sin permiso del staff.",
    "**Se prohibe la toxicidad y el drama**: Evita las discusiones en los canales públicos. Las diferencias personales se resuelven por privado. ",
    "**No compartas contenido ilegal ni peligroso**: No compartas enlaces con riesgo de virus. Mucho menos información personal de otros miembros.",
    "**Sigue a la mona**: Obligatorio. No se discute. <a:gatobaile:1522089458558828574>",
]


class Reglas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def construir_embed(self) -> discord.Embed:
        """Arma el embed de reglas a partir de la lista REGLAS."""
        descripcion = "\n\n".join(
            f"**{i}.** {regla}" for i, regla in enumerate(REGLAS, start=1)
        )

        embed = discord.Embed(
            title="📋 Reglas del servidor",
            description=descripcion,
            color=discord.Color.purple(),
        )
        return embed

    @app_commands.command(
        name="reglas",
        description="Envía el embed con las reglas del servidor en este canal",
    )
    @app_commands.default_permissions(administrator=True)  
    @app_commands.checks.has_permissions(administrator=True)  
    async def reglas(self, interaction: discord.Interaction):
        embed = self.construir_embed()

        # Confirmación efímera para quien ejecuta el comando
        await interaction.response.send_message(
            "✅ Enviando reglas...", ephemeral=True
        )
        # Embed real, visible para todos en el canal
        await interaction.channel.send(embed=embed)

    @reglas.error
    async def reglas_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "🚫 No tenés permiso para usar este comando (solo administradores).",
                ephemeral=True,
            )
        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(Reglas(bot))
