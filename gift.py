from redbot.core import bank, commands, errors, checks
from redbot.core.utils.chat_formatting import box, humanize_number
from discord.ext.commands.errors import BadArgument
from redbot.core.errors import BalanceTooHigh
import discord

class Gift(commands.Cog):
    @checks.mod()
    @commands.command(name="gift")
    async def gift(self, ctx: commands.Context, amount, to: discord.Member):
        """
        Gift a user glits:
        - `[p]gift 100 @Diva Maid` Gives 100 Glits to Diva Maid
        """
        amount = int(amount)
        author = ctx.author
        currency = await bank.get_currency_name(ctx.guild)
        msg = ("{author} gave {num} {currency} to {user}!.").format(
            author=author.display_name,
            num=humanize_number(amount),
            currency=currency,
            user=to.display_name,
)
        try:
            await bank.deposit_credits(to, amount)
        except errors.BalanceTooHigh as exc:
                await bank.set_balance(author, exc.max_balance)
                await ctx.send(
                    (
                        "You've reached the maximum amount of {currency}! "
                        "Please spend some more \N{GRIMACING FACE}\n\n"
                        "You already have {new_balance} {currency}."
                    ).format(
                        currency=currency, new_balance=humanize_number(exc.max_balance)
                    )
                )
                return
        else:
            await ctx.send(msg)
