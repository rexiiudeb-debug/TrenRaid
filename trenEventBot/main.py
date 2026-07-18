import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Zsynchronizowano {len(synced)} komend.")
    except Exception as e:
        print(e)


class EventView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Dołącz", style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "✅ Dołączyłeś do eventu!",
            ephemeral=True
        )

    @discord.ui.button(label="❌ Opuść", style=discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "❌ Opuściłeś event!",
            ephemeral=True
        )

    @discord.ui.button(label="📋 Lista", style=discord.ButtonStyle.blurple)
    async def lista(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Na razie lista jest pusta.",
            ephemeral=True
        )


@bot.tree.command(name="event", description="Tworzy nowy event")
@app_commands.describe(
    godzina="Godzina rozpoczęcia",
    limit="Limit graczy"
)
async def event(
    interaction: discord.Interaction,
    godzina: str,
    limit: int
):

    embed = discord.Embed(
        title="🎮 EVENT UNTURNED",
        color=0x2ecc71
    )

    embed.add_field(
        name="🕗 Godzina",
        value=godzina,
        inline=False
    )

    embed.add_field(
        name="👥 Uczestnicy",
        value=f"0/{limit}",
        inline=False
    )

    embed.add_field(
        name="📋 Lista",
        value="Brak uczestników",
        inline=False
    )

    await interaction.response.send_message(
        embed=embed,
        view=EventView()
    )


bot.run(TOKEN)