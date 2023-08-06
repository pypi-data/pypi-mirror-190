import asyncio

from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, GroupMessageEvent, PrivateMessageEvent, PRIVATE, Message
import nonebot
from nonebot.params import ArgStr, CommandArg
from nonebot import on_message, on_command
from pathlib import Path
from transformers import GPT2TokenizerFast
import os
import json
import asyncio

from .model import get_chat_response
from .config import Config

# 文档操作----------------------------------------------------------------------------


STATE_OK = True
STATE_ERROR = False


def write_data(path: Path, data: list) -> bool:
    try:
        if data:
            flag = 0
            for info in data:
                if flag == 0:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(' '.join(info))
                    flag = 1
                elif flag == 1:
                    with open(path, 'a', encoding='utf-8') as f:
                        f.write('\n' + (' '.join(info)))
        else:
            with open(path, 'w') as f:
                f.write('')
        return STATE_OK
    except Exception as e:
        logger.error(e)
        return STATE_ERROR


def read_data(path: Path) -> (bool, list):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.readlines()
        infos = [x.split() for x in data]

        return STATE_OK, infos
    except Exception as e:
        logger.error(e)
        return STATE_ERROR, []

# 配置地址----------------------------------------------------------


api_key = "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"

global_config = nonebot.get_driver().config
gpt3_config = Config.parse_obj(global_config.dict())
chatgpt3_path = gpt3_config.chatgpt3_path


if chatgpt3_path == Path():
    chatgpt3_path = chatgpt3_path / \
        os.path.dirname(os.path.abspath(__file__))


tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# 注册响应器------------------------------------------------------------


gpt3 = on_message(permission=PRIVATE, priority=10)
set_background = on_command("设置背景", priority=5, block=True)
# delete_background = on_command("删除背景", priority=5, block=True)
chat_gpt3 = on_command("开始聊天", priority=4, block=True, aliases={"开始对话"})


# 设置背景---------------------------------------------------------------------------------------------

@set_background.handle()
async def _(state:T_State, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if msg:
        state["bot_name"] = msg

@set_background.got("bot_name", prompt="请输入您要设置背景的机器人的名称，如 上官雨筝")
async def _(state:T_State, bot_name:str = ArgStr("bot_name")):
    await asyncio.sleep(1)
    await set_background.send(f"当前设置机器人名称为{bot_name}")

@set_background.got("master_name", prompt="请输入当前您在背景中的名称")
async def _(state:T_State, master_name:str = ArgStr("master_name")):
    await asyncio.sleep(1)
    state["master_name"] = master_name
    await set_background.send(f"当前您的名称设置为{master_name}")

@set_background.got("bot_info", prompt="请输入当前您设定的聊天背景,尽量注意标点符号，并且限制字数为200字")
async def _(event:MessageEvent, state:T_State, bot_info:str = ArgStr("bot_info")):
    await asyncio.sleep(1)
    background = {
        "bot_name":state["bot_name"],
        "master_name":state["master_name"],
        "bot_info":bot_info
    }
    with open(os.path.join(chatgpt3_path, f"{event.user_id}_background.json"), "w", encoding="utf-8") as f:
        f.write(str(background))
    await set_background.finish("设置背景成功！")


# 私聊会话---------------------------------------------------------------------------------------------

@gpt3.handle()
async def _(event: PrivateMessageEvent, msg: Message = CommandArg()):
    user_id = str(event.user_id)
    if os.path.exists(
        os.path.join(
            chatgpt3_path,
            f"{user_id}_background.json")):
        with open(os.path.join(chatgpt3_path, f"{user_id}_background.json"), "r", encoding="utf-8") as f:
            background_json = json.loads(f.read())
    else:
        await gpt3.finish("您暂未使用人格，请先设置")
    if os.path.exists(
        os.path.join(
            chatgpt3_path,
            f"{user_id}_conversation.txt")):
        with open(os.path.join(chatgpt3_path, f"{user_id}_conversation.txt"), "r", encoding="utf-8") as f:
            conversation = eval(f.read())
    else:
        f = open(
            os.path.join(
                chatgpt3_path,
                f"{user_id}_conversation.txt"),
            "w",
            encoding="utf-8")
        f.close()
        conversation = []
    bot_name = background_json["bot_name"]
    background = background_json["bot_info"]
    master_name = background_json["master_name"]
    start_sequence = f"\n{bot_name}:"
    restart_sequence = f"\n{master_name}: "
    if len(conversation):
        prompt = background + "".join(conversation) + msg
    else:
        prompt = background + restart_sequence + msg + start_sequence
    resp, flag = get_chat_response(
        api_key, prompt, start_sequence, bot_name, master_name)
    if flag:
        conversation.append(f"{msg}{start_sequence}{resp}{restart_sequence}")
        if len(conversation) > 10:
            conversation.pop(0)
            with open(os.path.join(chatgpt3_path, f"{user_id}_conversation.txt"), "w", encoding="utf-8") as f:
                f.write(str(conversation))
        await gpt3.finish(resp)
    else:
        logger.error(resp)


@chat_gpt3.handle()
async def _(event: MessageEvent, state: T_State):
    state["user_id"] = str(event.user_id)
    user_id = str(event.user_id)
    if os.path.exists(
            os.path.join(
                chatgpt3_path,
                f"{user_id}_background.json")):
        with open(os.path.join(chatgpt3_path, f"{user_id}_background.json"), "r", encoding="utf-8") as f:
            background_json = json.loads(f.read())
    else:
        await gpt3.finish("您暂未使用人格，请先设置")
    if os.path.exists(
            os.path.join(
                chatgpt3_path,
                f"{user_id}_conversation.txt")):
        with open(os.path.join(chatgpt3_path, f"{user_id}_conversation.txt"), "r", encoding="utf-8") as f:
            conversation = eval(f.read())
    else:
        f = open(
            os.path.join(
                chatgpt3_path,
                f"{user_id}_conversation.txt"),
            "w",
            encoding="utf-8")
        f.close()
        conversation = []
    state["bot_name"] = background_json["bot_name"]
    state["background"] = background_json["bot_info"]
    state["master_name"] = background_json["master_name"]
    state["conversation"] = conversation


@chat_gpt3.got("prompt")
async def _(event: MessageEvent, state: T_State, msg: Message = ArgStr("prompt")):
    if msg in ["算了", "取消", "结束对话", "对话结束", "聊天结束", "结束聊天"]:
        await chat_gpt3.finish("聊天结束")
    bot_name = state["bot_name"]
    master_name = state["master_name"]
    conversation = state["conversation"]
    if msg in ["重置会话", "重置聊天", "聊天重置", "会话重置"]:
        conversation = []
    background = state["background"]
    start_sequence = f"\n{bot_name}:"
    restart_sequence = f"\n{master_name}: "
    if len(conversation):
        prompt = background + "".join(conversation) + msg
    else:
        prompt = background + restart_sequence + msg + start_sequence
    resp, flag = get_chat_response(
        api_key, prompt, start_sequence, bot_name, master_name)
    if flag:
        len_prompt = len(tokenizer.encode(prompt))
        conversation.append(f"{msg}{start_sequence}{resp}{restart_sequence}")
        if len(conversation) > 12 or len_prompt > 4096:
            conversation.pop(0)
        await chat_gpt3.reject_arg("prompt", prompt=resp)
    else:
        logger.error(resp)
        await chat_gpt3.reject_arg("prompt", prompt="我刚刚没听清你说什么，能再说一次吗")
