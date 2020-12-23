import re
import json
import urllib.request

from twitchio import Message
from twitchio.client import User
from twitchio.ext import commands

#from googletrans import Translator

translator = Translator()

langs = [
    ['ko', 'kr', 'kor', '한글', '한국어', '한국', '대한민국'],  # 한국어
    ['en', 'us', 'eng', '영어', '미국', '미국어'],  # 영어
    ['ja', 'jp', '일본', '일본어', '일어'],  # 일본어
    ['es', '스페인어', '스페인'],  # 스페인어
    ['ru', '러시아', '러시아어'],  # 러시아어
    ['zh-CN', 'cn', 'china', 'zhongguo', '중국', '중국어', '간체', '중국어간체'],  # 중국어 간체
    ['zh-TW', 'tw', '번체', '중국어번체','대만','대만어'],  # 중국어 번체
    ['fr', 'france', '불어', '프랑스어', '프랑스'],  # 프랑스어
    ['it', 'italia', 'italiana' '이탈리아', '이탈리아어'],  # 이탈리아어
    ['vi', 'vn', 'vietnam', 'viet', '베트남어', '베트남'],  # 베트남어
    ['th', 'thai', '태국', '태국어'],  # 태국어
    ['id', 'bahasa', 'indo', 'indonesia', '인도네시아어', '인도네시아'],  # 인도네시아어
]

bits_regex = re.compile(r'cheer([0-9]+\s|([0-9]+$))', flags=re.IGNORECASE)

def remove_twitchEmoji(emote, text):
    eidx = list()
    if emote:
        emotes = emote.split('/')
        for emt in emotes:
            emt = emt.split(':')[1]
            for em in emt.split(','):
                st, nd = em.split('-')
                eidx.append((int(st), int(nd)))
        eidx.sort(reverse=True)
        for st, nd in eidx:
            text = text[:st] + text[nd + 1:]
    return text.strip()

def remove_twitchBits(text):
    global bits_regex
    match = bits_regex.sub('',text)
    return match

class papagoTranslator:
    naver_client_id: str
    naver_client_secret: str

    def __init__(self, id, secret):
        self.naver_client_id = id
        self.naver_client_secret = secret

    def detectLang(self, text):
        encQuery = urllib.parse.quote(text)
        data = "query=" + encQuery
        url = "https://openapi.naver.com/v1/papago/detectLangs"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.naver_client_id)
        request.add_header("X-Naver-Client-Secret", self.naver_client_secret)
        try:
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        except Exception as e:
            print(e)
            print(data.encode("utf-8"))
            return
        #rescode = response.getcode()
        #if (rescode == 200):
        response_body = response.read()
        dict = json.loads(response_body.decode('utf-8'))
        print(dict)
        return dict["langCode"]
        #else:
        #    print("Error Code:" + rescode)tper

    def translateSrcToTarget(self, source, target, text):
        encText = urllib.parse.quote(text)
        data = "source=" + source + "&target=" + target + "&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.naver_client_id)
        request.add_header("X-Naver-Client-Secret", self.naver_client_secret)
        try:
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        except Exception as e:
            print(e)
            print(data.encode("utf-8"))
            return
        #rescode = response.getcode()
        #if (rescode == 200):
        response_body = response.read()
        dict = json.loads(response_body.decode('utf-8'))
        return dict["message"]["result"]["translatedText"]
        #else:
        #    print("Error Code:" + rescode)


class TranslateCommand(commands.AutoCog):

    def __init__(self, bot):
        self.bot = bot
        self.translator = papagoTranslator(bot.settings["naver_client_id"],
                                           bot.settings["naver_client_secret"])
        self.tUsers: set = {'자동_번역할_시청자_ID1'}

        def command_wrapper(self, cmd_name, cmd_aliases):
            @commands.command(name=cmd_name, aliases=cmd_aliases)
            async def translateCommand(self, ctx):
                msg = remove_twitchEmoji(ctx.message.tags['emotes'], ctx.message.content)
                msg = msg[msg.find(' ') + 1:]
                if msg == '':
                    return
                response = self.translator.translateSrcToTarget('ko', cmd_name, msg)
                await ctx.send('{}) {}'.format(cmd_name[:2], response))

            return translateCommand

        for lang in langs[1:]:
            setattr(self, lang[0] + 'translateCommand', command_wrapper(self, lang[0], lang[1:]))

    def _prepare(self, bot):
        pass

    @commands.command(name='ko', aliases=langs[0][1:])
    async def translateKoreanCommand(self, ctx):
        msg = remove_twitchEmoji(ctx.message.tags['emotes'], ctx.message.content)
        msg = msg[msg.find(' ') + 1:]
        if msg == '':
            return
        clang = self.translator.detectLang(msg)
        if clang in ['ko', 'py', 'unk']:
            return
        response = self.translator.translateSrcToTarget(clang, 'ko', msg)
        await ctx.send('{}) {}'.format('ko', response))

    @commands.command(name='translate', aliases=['trans', 'tran', 'ts', '번역', '자동번역'])
    async def AutotranslateCommand(self, ctx, user: str = None):
        if user:
            user = user.lower()
        else:
            user = ctx.author.name.lower()
        if user not in self.tUsers:
            self.tUsers.add(user)
            print(self.tUsers)
            await ctx.send_me(f'(Start auto-translation of {user} )')
        else:
            self.tUsers.remove(user)
            print(self.tUsers)
            await ctx.send_me(f'(End auto-translation of {user} )')

    async def event_message(self, message: Message) -> None:
        if message.author.name in self.tUsers:
            ctx = await self.bot.get_context(message)
            if ctx.prefix:
                return
            msg = remove_twitchEmoji(message.tags['emotes'], message.content)
            msg = remove_twitchBits(msg)
            if msg == '' or msg.find('@') != -1:
                return
            clang = self.translator.detectLang(msg)
            if clang in ['ko', 'py', 'pt','unk']:
                return
            response = self.translator.translateSrcToTarget(clang, 'ko', msg)
            await ctx.send('{}) {}'.format('ko', response))


def prepare(bot):
    bot.add_cog(TranslateCommand(bot))


def breakdown(bot):
    bot.remove_cog(TranslateCommand(bot))
