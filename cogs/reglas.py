import discord
from discord import app_commands
from discord.ext import commands

# ⚙️ CONFIGURACIÓN
# Editá el texto de cada regla acá abajo
REGLAS = [
    "﹒﹒__#001__ ➜ sé amable. no se tolerará el acoso, los insultos, la discriminación ni los discursos de odio. queremos que este sea un espacio agradable para todos! >-<",
    "﹒﹒__#002__ ➜ queda estrictamente prohibido compartir imágenes, videos o texto con contenido explícito, sangriento o sexual." ,
    "﹒﹒__#003__ ➜ cada canal tiene un propósito, usalos correctamente!",
    "﹒﹒__#004__ ➜ evita enviar mensajes repetitivos y/o con mayúsculas excesivas. tampoco hagas promoción de tus redes o servidores sin permiso del staff.",
    "﹒﹒__#005__ ➜ evita las discusiones en los canales públicos. las diferencias personales se resuelven en privado. ",
    "﹒﹒__#006__ ➜ es obligatorio seguir a la monita, no se discute. <a:gatobaile:1522089458558828574>",
]
# URL de la imagen/gif de bienvenida (podés poner una URL directa a un .gif o .png)
IMAGEN_BIENVENIDA_URL = "https://i.imgur.com/XWufGs8.gif"


class Reglas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def construir_embed(self) -> discord.Embed:
        """Arma el embed de reglas a partir de la lista REGLAS."""
        descripcion = "\n\n".join(
            f"**{i}.** {regla}" for i, regla in enumerate(REGLAS, start=1)
        )

        embed = discord.Embed(
            title="﹒﹒reglas del servidor﹐ ❀",
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
