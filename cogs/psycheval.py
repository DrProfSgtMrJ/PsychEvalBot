import asyncio
from discord import Message
from discord.ext import commands

from ai.ai import generate_questions



class PsychEvalCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="evaluate", help="Start your psychological evaluation.")
    async def evaluate(self, ctx: commands.Context):

        response = []
        def check(message: Message) -> bool:
            return message.author == ctx.author and message.channel == ctx.channel

        # Placeholder for actual evaluation logic
        num_questions = 10  # Example: number of questions to generate
        try:
            questions = await generate_questions(num_questions)
            if not questions:
                await ctx.send("Failed to generate questions. Please try again later.")
                return
        except Exception as e:
            await ctx.send(f"An error occurred while generating questions: {e}")
            return

        try:
            for i, question in enumerate(questions):
                await ctx.send(f"Question {i + 1}: {question}")
                msg = await self.bot.wait_for("message", check=check, timeout=120.0)
                response.append(msg.content)
        except Exception as e:
            await ctx.send(f"An error occurred while sending questions: {e}")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Please start the evaluation again.")
            return
        await ctx.send("Thank you for completing the evaluation!")
        print(f"User {ctx.author} responses: {response}")  # For debugging purposes