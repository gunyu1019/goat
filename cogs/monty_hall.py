import random

import discord
from discord.ext import interaction


class MontyHall:
    def __init__(self, client):
        self.client = client

    @interaction.command(name="몬티홀", description="This is MontyHall.")
    @interaction.option(
        name="시행_횟수",
        description="시행할 횟수를 입력해주세요.",
        min_value=0, max_value=1000
    )
    async def monty_hall(
            self,
            ctx: interaction.ApplicationContext,
            trials: int = 1
    ):
        success = 0
        failed = 0
        embed = discord.Embed(
            title="\U0001F410 MontyHall",
            colour=0x007dff
        )
        components = []
        for loop_index in range(trials):
            car_position = random.randint(0, 2)
            doors = [0, 0, 0]
            doors[car_position] = 1

            embed = discord.Embed(
                title="\U0001F410 MontyHall",
                description="이 3개의 버튼 속에는 1개의 자동차와, 2개의 염소가 들어있습니다.",
                colour=0x007dff
            )
            embed.add_field(
                name="상태",
                value=f"시행 횟수: {loop_index + 1}회/{trials}회",
                inline=True
            )
            embed.add_field(
                name="결과",
                value=f"성공 횟수: {success}회\n"
                      f"실패 횟수: {failed}회\n"
                      f"성공 확률: {round((success / (failed + success) if failed + success > 0 else 1) * 100, 2)}%",
                inline=True
            )
            components = interaction.ActionRow(components=[
                interaction.Button(
                    style=1,
                    emoji=discord.PartialEmoji(name="\U00000031\U0000FE0F\U000020E3"),
                    disabled=True,
                    custom_id='door1'
                ),
                interaction.Button(
                    style=1,
                    emoji=discord.PartialEmoji(name="\U00000032\U0000FE0F\U000020E3"),
                    disabled=True,
                    custom_id='door2'
                ),
                interaction.Button(
                    style=1,
                    emoji=discord.PartialEmoji(name="\U00000033\U0000FE0F\U000020E3"),
                    disabled=True,
                    custom_id='door3'
                )
            ])
            if not ctx.responded:
                await ctx.send(embed=embed, components=[components])
            else:
                await ctx.edit(embed=embed, components=[components])

            player_choices = random.randint(0, 2)
            await ctx.edit(embed=embed, components=[components])
            doors[player_choices] += 2

            position = doors.index(0)
            components.components[position].style = 2
            components.components[position].disabled = True
            embed.description += (
                f"\n만약 {position + 1} 번째 문에 염소가 있다면, 당신은 무엇을 선택하실껍니까\n"
                "지금의 선택을 유지하실건가요? 아니면 또 다른 문을 고를 것인가요?"
            )
            await ctx.edit(embed=embed, components=[components])
            new_player_choices = None
            if (position == 0 and player_choices == 2) or (position == 2 and player_choices == 0):
                new_player_choices = 1
            elif (position == 1 and player_choices == 2) or (position == 2 and player_choices == 1):
                new_player_choices = 0
            elif (position == 0 and player_choices == 1) or (position == 1 and player_choices == 0):
                new_player_choices = 2
            components.components[car_position].style = 3
            if new_player_choices == car_position:
                embed.description += "\n축하합니다. 자동차를 찾으셨습니다!"
                success += 1
            else:
                embed.description += "\n아쉽게도 자동차를 찾기 못했습니다!"
                components.components[new_player_choices].style = 4
                failed += 1
            await ctx.edit(embed=embed, components=[components])
        embed.set_field_at(
            index=1,
            name=embed.fields[1].name,
            value=f"성공 횟수: {success}회\n"
                  f"실패 횟수: {failed}회\n"
                  f"성공 확률: {round((success / (failed + success) if failed + success > 0 else 1) * 100, 2)}%",
            inline=True
        )
        await ctx.edit(embed=embed, components=[components])
        return


def setup(client):
    client.add_interaction_cog(MontyHall(client))
