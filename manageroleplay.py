import discord, traceback, random, re, os
from datetime import datetime, timedelta, timezone

EMBED_COLOR = 0x2ECC69

token = os.environ["DISCORD_BOT_TOKEN"]

global user_id
global text_channel

user_id = int(os.environ["USER_ID"])
text_channel = int(os.environ["DISCORD_MAIN_CHANNEL"])

JST = timezone(timedelta(hours=+9), 'JST')

# 空白で区切られたメッセージのn番目を取り出す
def command(message, n=0):
    try:
        return message.split(' ')[n]
    except IndexError:
        return ''

class MyClient(discord.Client):
    async def send2developer(self, msg):
        developer = self.get_user(user_id)
        dm = await developer.create_dm()
        await dm.send(msg)

    async def on_ready(self):
        """ 起動時のイベントハンドラ """
        msg = f'Logged on as {self.user}!'
        await self.send2developer(msg)

    #メンバーのステータスが変わったら通知する処理
    #async def on_member_update(self, before, after):
        #if before.status != after.status:
            #time = str(datetime.now(JST).strftime("%Y/%m/%d %H:%M:%S"))
            #msg = "@everyone" + time + " " + after.display_name + " さんが " + str(after.status) + " になりました"
            #await self.get_channel(text_channel).send(msg)

    #ダイス
    # メッセージを受信するごとに実行される
    async def on_message(self, message):
        # BOTとメッセージの送り主が同じ人なら処理しない
        if self.user == message.author:
            return

        cmd_1 = command(message.content)

        # 辞書に格納
        m = re.match("(?P<num>\d+)d(?P<max>\d+)(\+(?P<base>\d+))?(<=(?P<cond>\d+))?", cmd_1)

        if m:
            # 辞書から抽出
            d = m.groupdict()
            num = int(d['num'])
            maxval = int(d['max'])
            # キーは存在してるっぽい。Noneを返してくる
            # base = d.get('base', 0)
            base = d.get('base')

            val = 0
            # ベースが存在したら加える
            if base is not None:
                val = int(base)

            if num == 0 or maxval == 0:
                # エラー処理
                await self.send_message(message.channel, "0以外を指定してください")
                return

        disp = '[ '

        # ダイスを振る
        for i in range(0, num):
            rnd = random.randrange(maxval)+1
            val += rnd
            disp += f'{rnd:,} + '
        disp = disp[0:-3]

        # print(val)

        if base is not None:
            disp += f' + ({int(base):,}) ]= {val:,}'
        else:
            disp += f' ]= {val:,}'

        embed = discord.Embed(title="ダイス", description=cmd_1[1:], color=EMBED_COLOR)
        embed.add_field(name="出目", value=disp, inline=False)
        await message.channel.send(message.channel, embed=embed)

# TOKEN にアクセストークンを入れてください
MyClient().run(token)
