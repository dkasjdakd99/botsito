import discord
from discord.ext import commands
from discord import app_commands
import os
import logging

logger = logging.getLogger(__name__)

CANAL_VERIFICACION = int(os.getenv("CANAL_VERIFICACION"))
ROL_USUARIO = int(os.getenv("ROL_USUARIO"))
# URL de la imagen/gif de bienvenida (podés poner una URL directa a un .gif o .png)
IMAGEN_BIENVENIDA_URL = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3lvd2N3ZDRpbTE1bnVpc3puYnM2ZDZseWlsbWJyeTY0NzJhdmUwbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/DIYVI7Iz4dmnu/giphy.gif"


class BotonVerificacion(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ Verificarme",
        style=discord.ButtonStyle.success,
        custom_id="verificacion:boton"
    )
    async def verificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            rol = interaction.guild.get_role(ROL_USUARIO)
            if rol is None:
                await interaction.response.send_message(
                    "Error de configuración: no se encontró el rol de usuario.", ephemeral=True
                )
                return

            if rol in interaction.user.roles:
                await interaction.response.send_message(
                    "Ya estás verificado.", ephemeral=True
                )
                return

            await interaction.user.add_roles(rol)
            await interaction.response.send_message(
                "✅ ¡Verificado! Ya puedes acceder al servidor.", ephemeral=True
            )

        except discord.Forbidden:
            logger.error("Sin permisos para asignar el rol de verificación.")
            await interaction.response.send_message(
                "No tengo permisos para asignarte el rol. Contacta a un administrador.", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error en verificar: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message("Ocurrió un error al verificarte.", ephemeral=True)
            else:
                await interaction.followup.send("Ocurrió un error al verificarte.", ephemeral=True)


class Verificacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(BotonVerificacion())

    @app_commands.command(name="setup_verificacion", description="Envía el mensaje de verificación")
    @app_commands.default_permissions(administrator=True)  # Oculta el comando en el menú para quienes no son admin
    @app_commands.checks.has_permissions(administrator=True)  # Chequeo real, por si el default fue modificado
    async def setup_verificacion(self, interaction: discord.Interaction):
        try:
            canal = self.bot.get_channel(CANAL_VERIFICACION)
            if canal is None:
                await interaction.response.send_message(
                    "No se encontró el canal de verificación. Revisa la configuración.", ephemeral=True
                )
                return

            embed = discord.Embed(
                title="﹒﹒sistema de verificación﹐ ❀",
                description="hola! haz click en el botón de abajo para poder acceder al resto de los canales ;)",
                color=discord.Color.green()
            )
            embed.set_image(url=IMAGEN_BIENVENIDA_URL)

            await canal.send(embed=embed, view=BotonVerificacion())
            await interaction.response.send_message(
                "✅ Mensaje de verificación enviado.", ephemeral=True
            )

        except Exception as e:
            logger.error(f"Error en setup_verificacion: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message("Ocurrió un error.", ephemeral=True)
            else:
                await interaction.followup.send("Ocurrió un error.", ephemeral=True)

    @setup_verificacion.error
    async def setup_verificacion_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "🚫 No tenés permiso para usar este comando (solo administradores).",
                ephemeral=True,
            )
        else:
            raise error


async def setup(bot):
    await bot.add_cog(Verificacion(bot))
