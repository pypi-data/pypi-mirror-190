import json
import os
from enum import Enum
from string import Template
import requests as req
from requests_toolbelt import MultipartEncoder

__TEMPLATE_PATH = "template/%s"


class MSG_TYPE(Enum):
    """
    消息类型
    """

    # 基础文本 content
    TEXT = 1,

    # 富文本 title rich_content()
    RICH_TEXT = 2,

    # 群名片 chat_id
    GROUP_CARD = 3,

    # 图片
    IMAGE = 4,

    # 卡片消息 content bts(bt_title,href)
    CARD = 5,


def __readTxt(subPath):
    """
    读取模版文件
    """

    path = os.path.abspath(os.path.join(os.getcwd(), "template"))
    print('当前目录:' + path)

    f = open(path+'/%s' % subPath)
    content = f.read()
    f.close()
    return content


def __checkRiceJson(contents):
    if not isinstance(contents, list):
        print('富文本样式下content必须传入列表')
        return False

    if len(contents) == 0:
        print('不能为空节点')
        return False

    for content in contents:

        if not isinstance(content, dict):
            print('富文本content必须为字典集合')
            return False

        tag = content.get('tag')
        text = content.get('text')
        href = content.get('href')
        user_id = content.get('user_id')

        if tag is None:
            print('富文本不能缺少tag节点')
            return False
        else:

            if tag != 'text' and tag != 'a' and tag != 'at':
                print('不支持的节点类型')
                return False

            if tag == 'text' and text is None:
                print('当富文本tag节点为text时，text节点不能为空')
                return False

            elif tag == 'a' and (text is None or href is None):
                print('当富文本tag节点为a时，text节点与href节点均不能为空')
                return False
            elif tag == 'at' and user_id is None:
                print('当富文本tag节点为at时，user_id节点不能为空')
                return False

    return True


def __checkBts(bottons: list):
    for item in bottons:
        if item.get('bt_title') is None:
            print('按钮字典必须包含bt_title')
            return False
    return True


def __buildMsg(msgType: MSG_TYPE, title: str = None, content=None, bottons: list = None):
    """
    构建消息内容
    """
    fly_mod = __readTxt('fly/' + str(msgType))

    if msgType == MSG_TYPE.TEXT:
        if content is None:
            content = ""
        return Template(fly_mod).safe_substitute({'content': content})
    elif msgType == MSG_TYPE.RICH_TEXT:
        if title is None:
            title = '富文本消息'

        if content is None:
            return Template(fly_mod).safe_substitute({'rich_content': '', 'title': title})
        else:
            # 校验格式
            if __checkRiceJson(content):
                subMod = __readTxt('rich_text_sub/RICH_TEXT_CONTENT')
                tmpStr = ''
                # 循环迭代富文本中的节点模版
                for item in content:
                    if item.get('text') is None:
                        item['text'] = ""
                    if item.get('href') is None:
                        item['href'] = ""
                    if item.get('user_id') is None:
                        item['user_id'] = ""

                    tmpStr += Template(subMod).safe_substitute(item) + ','

                if tmpStr.endswith(","):
                    tmpStr = tmpStr[:len(tmpStr) - 1]
                return Template(fly_mod).safe_substitute({'rich_content': tmpStr, 'title': title})
    elif msgType == MSG_TYPE.CARD:
        if title is None:
            title = '卡片消息'
        if content is None:
            content = ""

        bts = ''
        if not bottons is None and len(bottons) > 0:
            if __checkBts(bottons):
                subMod = __readTxt('card_sub/CARD_BT')
                for item in bottons:
                    if item.get('href') is None:
                        item['href'] = ''
                    bts += Template(subMod).safe_substitute(item) + ','
                if bts.endswith(','):
                    bts = bts[:len(bts) - 1]
                return Template(fly_mod).safe_substitute({'content': content, 'title': title, 'bts': bts})
            else:
                return None
    elif msgType == MSG_TYPE.GROUP_CARD:
        return Template(fly_mod).safe_substitute({'chat_id': content})
    elif msgType == MSG_TYPE.IMAGE:
        return Template(fly_mod).safe_substitute({'image_key': content})
    return None


def getToken(app_id, app_secret):
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        resp = req.post(url=url, data=json.dumps({
            'app_id': app_id,
            'app_secret': app_secret
        }), headers=__headers)
        if resp.status_code == 200:
            result = json.loads(resp.text)
            if result.get('code') == 0:
                return result.get('tenant_access_token')
    except:
        return None


def uploadImage(path, token):
    # 获取token
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (open(path, 'rb'))}
    multi_form = MultipartEncoder(form)
    mHeaders = {
        'Authorization': 'Bearer ' + token,  ## 获取tenant_access_token, 需要替换为实际的token
    }
    mHeaders['Content-Type'] = multi_form.content_type

    try:
        response = req.request("POST", url, headers=mHeaders, data=multi_form)
        if response.status_code == 200:
            result = json.loads(response.text)
            if result.get('code') == 0:
                print('图片上传成功')
                return result.get('data')['image_key']
    except:
        print('图片上传失败')
        return None


__useHookUrl = None
__headers = {
    "Content-Type": "application/json; charset=utf-8"
}


def setHookUrl(hookUrl: str):
    global __useHookUrl
    __useHookUrl = hookUrl


# 调用飞书api发送通知
def sendChatMsg(msgType: MSG_TYPE, title: str = None, content=None, bottons: list = None, hookUrl: str = None):
    c = __buildMsg(msgType, title, content, bottons)
    if c is None:
        return [False, '消息内容构建失败']
    else:
        url = __useHookUrl
        if not hookUrl is None:
            url = hookUrl
        if url is None:
            return [False, '请配置机器人的hookUrl']

        resp = req.post(url=url, data=c.encode('UTF-8'), headers=__headers)
        if resp.status_code == 200:
            result = json.loads(resp.text)
            if result.get('code') == 0:
                return [True, 'Success']
            else:
                return [False, result.get('msg')]
        else:
            return [False, '发送异常']


if __name__ == '__main__':
#     '''
#     文本消息
    content = __buildMsg(msgType=MSG_TYPE.TEXT, content='文本消息')
#     富文本消息
#     content = __buildMsg(msgType=MSG_TYPE.RICH_TEXT, content=[
#         {
#             'tag': 'text',
#             'text': '这是文本的内容  ',
#         },
#         {
#             'tag': 'a',
#             'text': '点我查看详情',
#             'href': 'https://github.com/devzwy'
#         },
#         {
#             'tag': 'at',
#             'user_id': '01ao86c2-ed06-4a74-857b-707d5a506bea',
#         }
#     ])
#
#     卡片消息
#     content = __buildMsg(msgType=MSG_TYPE.CARD, title='卡片消息', content='卡片消息内容', bottons=[
#         {
#             'bt_title': '测试按钮 :玫瑰:',
#             'href': 'https://github.com/devzwy'
#         }
#     ])
#     群名片
#     content = __buildMsg(msgType=MSG_TYPE.GROUP_CARD,content='oc_f5b1a7eb27ae2c7b6adc2a74faf339ff')
#
#
#     https://open.feishu.cn/open-apis/bot/v2/hook/1f0bb79e-bf26-4fb3-b122-fb6bc9e5d2bd
#     '''
#
#     # content = __buildMsg(msgType=MSG_TYPE.IMAGE, content=uploadImage('face.png', getToken('cli_a36e2b4c87f1500d',
#     #
#     #                                                                                       'EctNmdDlhwEeEigAWFdp2eowutTFwz0v')))
#
#     setHookUrl('https://open.feishu.cn/open-apis/bot/v2/hook/1f0bb79e-bf26-4fb3-b122-fb6bc9e5d2bd')
#     result = sendChatMsg(msgType=MSG_TYPE.IMAGE, content=uploadImage('face.png', getToken('cli_a36e2b4c87f1500d',
#                                                                                           'EctNmdDlhwEeEigAWFdp2eowutTFwz0v')))
#     if result[0]:
#         print('发送成功')
#     else:
#         print('发送失败,' + result[1])
