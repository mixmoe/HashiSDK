# flake8: noqa: E501
from typing import Any, Dict, Optional, Union

class IOTClientAPI:
    """
    # IOT客户端API类抽象实现

    可以调用这之中已有的方法
    也可以调用自定义方法
    `.`字符用`__`双下划线代替
    """

    def __init__(self, qq: int, address: str, timeout: Optional[int] = None) -> None:
        """
        ## 实例化API对象
        """
        ...

    async def callAction(
        self, action: str, **kwargs
    ) -> Union[Dict[str, Any], str, int, bytes, None]:
        """
        ## 调用API指定方法
        """
        ...

    async def AddQQUser(
        self, *, AddUserUid: int, FromGroupID: int, AddFromSource: int, Content: str
    ):
        """
        ## 添加QQ好友

        - 添加好友 新号老号控制好频率  AddFromSource--来源2011 空间2020 QQ搜索 2004群组 2005讨论组

        ```json
        {
            "AddFromSource": 2004,
            "AddUserUid": 123456789,
            "Content": "加好友，互助浇水",
            "FromGroupID": 123456789
        }
        ```
        """
        ...

    async def AnswerInviteGroup(
        self,
        *,
        Seq: int,
        Type: int,
        MsgTypeStr: str,
        Who: int,
        WhoName: str,
        MsgStatusStr: str,
        Flag_7: int,
        Flag_8: int,
        GroupId: int,
        GroupName: str,
        InviteUin: int,
        InviteName: str,
        Action: int
    ):
        """
        ## 处理群邀请

        - 请求参数来自 WebSocket的推送
            - `{"CurrentPacket":{"WebConnId":"3x1VZ6DlCiNQP1khIB43","Data":{"EventData":{"Seq":1570980892762275,"Type":1,"MsgTypeStr":"邀请加群","Who":123456789,"WhoName":"QQ棒棒冰","MsgStatusStr":"","Flag_7":8192,"Flag_8":512,"GroupId":570065685,"GroupName":"Rust编程语 言社区3群","InviteUin":123456789,"InviteName":"Kar98k","Action":0},"EventMsg":{"FromUin":570065685,"ToUin":123456789,"MsgType":"ON_EVENT_GROUP_INVITED","Content":"邀请加群","RedBaginfo":null},"EventName":"ON_EVENT_GROUP_INVITED"}},"CurrentQQ":123456789}`
            - 11 agree 14 忽略 21 disagree

        ```json
        {
            "Action": 0,
            "Flag_7": 8192,
            "Flag_8": 512,
            "GroupId": 570065685,
            "GroupName": "Rust编程语言社区3群",
            "InviteName": "Kar98k",
            "InviteUin": 123456789,
            "MsgStatusStr": "",
            "MsgTypeStr": "邀请加群",
            "Seq": 1570980892762275,
            "Type": 1,
            "Who": 123456789,
            "WhoName": "QQ棒棒冰"
        }
        ```
        """
        ...

    async def DealFriend(
        self,
        *,
        UserID: int,
        FromType: int,
        Field_9: int,
        Content: str,
        FromGroupId: int,
        FromGroupName: str,
        Action: int
    ):
        """
        ## 处理好友请求

        - 请求参数来自 WebSocket的推送
            - `{"CurrentPacket":{"WebConnId":"fi4LFS7_uy8ORrKDQN5Z","Data":{"EventData":{"UserID":103259869,"FromType":2004,"Field_9":1571036852000000,"Content":"收到好友请求 内容我是QQ大冰来源来自QQ群","FromGroupId":123456789,"FromGroupName":"IOTQQ交流群","Action":2},"EventMsg":{"FromUin":103259869,"ToUin":123456789,"MsgType":"ON_EVENT_FRIEND_ADDED","Content":"收到好友请求 内容我是QQ大冰来源来自QQ群","RedBaginfo":null},"EventName":"ON_EVENT_FRIEND_ADD"}},"CurrentQQ":123456789}`
            - Action 1忽略2同意3拒绝

        ```json
        {
            "Action": 2,
            "Content": "收到好友请求 内容我是QQ大冰来源来自QQ群",
            "Field_9": 1571036852000000,
            "FromGroupId": 123456789,
            "FromGroupName": "IOTQQ交流群",
            "FromType": 2004,
            "UserID": 103259869
        }
        ```
        """
        ...

    async def GetBalance(self, *, Uid: int, Fid: int):
        """
        ## 获取钱包余额相关Key

        -

        ```json
        {
            "Fid": 0,
            "Uid": 0
        }
        ```
        """
        ...

    async def GetGroupList(self, *, NextToken: str):
        """
        ## 获取群列表

        - 获取群列表
            - 首次请求` {"NextToken":""} `第二次请求NextToken请填值
            - 返回json中 TroopList==null 时说明拉取群列表完成

        ```json
        {
            "NextToken": ""
        }
        ```
        """
        ...

    async def GetGroupUserList(self, *, GroupUin: int, LastUin: int):
        """
        ## 获取群成员列表

        - 获取群列表
        - 首次请求 `{"GroupUin":0,"LastUin":0}` 第二次请求NextToken 请填值
        - 返回json 中 LastUin==0 时说明拉取群成员列表完成

        ```json
        {
            "GroupUin": 570065685,
            "LastUin": 0
        }
        ```
        """
        ...

    async def GetQQUserList(self, *, StartIndex: int):
        """
        ## 获取好友列表

        - 获取好友列表
            - 返回json中 StartIndex == Friend_count 说明拉取好友列表完毕 否则 传入StartIndex 继续请求

        ```json
        {
            "StartIndex": 0
        }
        ```
        """
        ...

    async def GetUserCook(self, *, Flag: bool):
        """
        ## 获取QQ相关ck

        - `{"Flag":false}`

        ```json
        {
            "Flag": false
        }
        ```
        """
        ...

    async def GetUserInfo(self, *, UserID: int):
        """
        ## 获取任意用户信息昵称头像等

        - 有频率限制
            - NewTitle ="" 则取消头衔
            - `{"GroupID":123456789,"UserID":123456789,"NewTitle":"666669"}`

        ```json
        {
            "UserID": 123456789
        }
        ```
        """
        ...

    async def GroupMgr(
        self, *, ActionType: int, GroupID: int, ActionUserID: int, Content: str
    ):
        """
        ## QQ群功能包加群拉人..

        - 添加群组 新号老号控制好频率
            - ActionType=8 拉人入群 --> `{"ActionType":8,"GroupID":123456,"ActionUserID":987654,"Content":""}`
            - ActionType=1 加入群聊 --> `{"ActionType":1,"GroupID":123456,"ActionUserID":0,"Content":"你好通过一下"}`
            - ActionType=2 退出群聊 --> `{"ActionType":2,"GroupID":123456,"ActionUserID":0,"Content":""}`
            - ActionType=3 移出群聊 --> `{"ActionType":3,"GroupID":123456,"ActionUserID":0,"Content":""}`

        ```json
        {
            "ActionType": 3,
            "ActionUserID": 123456,
            "Content": "你好通过一下",
            "GroupID": 123456789
        }
        ```
        """
        ...

    async def LogOut(self, *, Flag: bool):
        """
        ## 退出指定QQ

        - `{"Flag":false}`不删除用户配置文件 true 删除用户配置文件

        ```json
        {
            "Flag": false
        }
        ```
        """
        ...

    # 因为方法名重复所以删去
    #
    # async def ModifyGroupCard(
    #     self,
    #     *,
    #     Tittle: str,
    #     Des: str,
    #     RedType: int,
    #     Listid: str,
    #     Authkey: str,
    #     Channel: int,
    #     StingIndex: str,
    #     Token_17_2: str,
    #     Token_17_3: str,
    #     FromUin: int,
    #     FromType: int
    # ):
    #     """
    #         ## 打开RED包

    #         -

    #         ```json
    #         {
    #             "Authkey": "7ed906141524a1edde40714fc8c8510005",
    #             "Channel": 1,
    #             "Des": "赶紧点击拆开吧",
    #             "FromType": 1,
    #             "FromUin": 123456789,
    #             "Listid": "10000448011910163700109887578400",
    #             "RedType": 6,
    #             "StingIndex": "NmE4YzQ3ZjgwOGJkNjc3ODAwODUxMzlhM2VjMmFhZTE=",
    #             "Tittle": "大吉大利",
    #             "Token_17_2": "fZXIb1y5rilopb5j/yImCC0EQNeMDxRe2gtDEOMTFG0=",
    #             "Token_17_3": "YjU0NmVjYTdjY2JhODMwYTljY2EwZjA5M2NhNDZhMGM="
    #         }
    #         ```
    #         """
    #     ...

    async def ModifyGroupCard(self, *, GroupID: int, UserID: int, NewNick: str):
        """
        ## 修改群名片

        - `{"GroupID":123456789,"UserID":123456789,"NewNick":"测试名片999999999"}`

        ```json
        {
            "GroupID": 123456789,
            "NewNick": "8888测试名片999999999",
            "UserID": 123456789
        }
        ```
        """
        ...

    async def OidbSvc__0x570_8(self, *, GroupID: int, ShutUpUserID: int, ShutTime: int):
        """
        ## 通用Call群成员禁言

        - {"GroupID":123456789,"ShutUpUserID":1234567,"ShutTime":0} ShutTime单位为分钟 0 取消禁言

        ```json
        {
            "GroupID": 123456789,
            "ShutTime": 0,
            "ShutUpUserID": 6773509
        }
        ```
        """
        ...

    async def OidbSvc__0x7e5_4(self, *, UserID: int):
        """
        ## 通用Call点赞包

        -

        ```json
        {
            "UserID": 123456789
        }
        ```
        """
        ...

    async def OidbSvc__0x89a_0(self, *, GroupID: int, Switch: int):
        """
        ## 通用Call全群禁言

        - {"GroupID":123456789,"Switch":0} Switch=0关闭全群禁言 Switch=15开启全群禁言

        ```json
        {
            "GroupID": 123456789,
            "Switch": 0
        }
        ```
        """
        ...

    async def OidbSvc__0x8ba_31(self, *, Content: str, Page: int):
        """
        ## 通用Call搜索群组

        - 请求参数来自 WebSocket的推送
            - Action 1忽略2同意3拒绝
            - `{"CurrentPacket":{"WebConnId":"fi4LFS7_uy8ORrKDQN5Z","Data":{"EventData":{"UserID":103259869,"FromType":2004,"Field_9":1571036852000000,"Content":"收到好友请求 内容我是QQ大冰来源来自QQ群","FromGroupId":123456789,"FromGroupName":"IOTQQ交流群","Action":2},"EventMsg":{"FromUin":103259869,"ToUin":123456789,"MsgType":"ON_EVENT_FRIEND_ADDED","Content":"收到好友请求 内容我是QQ大冰来源来自QQ群","RedBaginfo":null},"EventName":"ON_EVENT_FRIEND_ADD"}},"CurrentQQ":123456789}`

        ```json
        {
            "Content": "深圳",
            "Page": 0
        }
        ```
        """
        ...

    async def OidbSvc__0x8fc_2(self, *, GroupID: int, UserID: int, NewTitle: str):
        """
        ## 通用Call设置群头衔

        -

        ```json
        {
            "GroupID": 123456789,
            "NewTitle": "997",
            "UserID": 123456789
        }
        ```
        """
        ...

    async def PbMessageSvc__PbMsgWithDraw(
        self, *, GroupID: int, MsgSeq: int, MsgRandom: int
    ):
        """
        ## 通用Call撤回消息

        -

        ```json
        {
            "GroupID": 123456789,
            "MsgRandom": 1786189853,
            "MsgSeq": 3747
        }
        ```
        """
        ...

    async def PttCenterSvr__ShortVideoDownReq(
        self, *, GroupID: int, VideoUrl: str, VideoMd5: str
    ):
        """
            ## 通用Call获取短视频Url

            -

            ```json
            {
                "GroupID": 123456789,
                "VideoMd5": "Q218V8zrH2PRiWVDYGuRAg==",
                "VideoUrl": "MzA1MTAyMDEwMDA0MzYzMDM0MDIwMTAwMDIwNDAwYTk0NDMzMDIwMzdhMWFmZDAyMDRhNzNlNWI2NTAyMDQ1ZGU5YjcxMzA0MTA0MzZkN2M1N2NjZWIxZjYzZDE4OTY1NDM2MDZiOTEwMjAyMDM3YTFkYjkwMjAxMDAwNDE0MDAwMDAwMDg2NjY5NmM2NTc0Nzk3MDY1MDAwMDAwMDQzMTMwMzAzMw=="
            }
            ```
            """
        ...

    async def QQZan(self, *, UserID: int):
        """
        ## 测试赞

        - `{"Uid":0,"Fid":0}` fid 需要被赞的QQ Uid 触发动作的QQ号 详情看Lua代码

        ```json
        {
            "UserID": 123456789
        }
        ```
        """
        ...

    async def RevokeMsg(self, *, GroupID: int, MsgSeq: int, MsgRandom: int):
        """
        ## 撤回群成员消息

        - `{"GroupID":0,"MsgSeq":0,"MsgRandom":0}`参数来自于 lua  ReceiveGroupMsg  事件  data 数据 data__data, data__data 可 撤回自己发的消息 或管理员权限撤回群成员消息

        ```json
        {
            "GroupID": 123456789,
            "MsgRandom": 2135872681,
            "MsgSeq": 3981
        }
        ```
        """
        ...

    async def SearchGroup(self, *, Content: str, Page: int):
        """
        ## 搜索QQ群组

        - `{"Content":"深圳","Page":0}`

        ```json
        {
            "Content": "深圳",
            "Page": 0
        }
        ```
        """
        ...

    async def SendMsg(
        self,
        *,
        toUser: int,
        sendToType: int,
        sendMsgType: str,
        content: str,
        groupid: int,
        atUser: int,
        replayInfo: Optional[Dict[str, Any]]
    ):
        """
        ## 发送好友文字消息

        - `{"toUser":QQ号或群GroupID,"sendToType":1,"sendMsgType":"TextMsg","content":"你好","groupid":0,"atUser":0}`

        ```json
        {
            "atUser": 0,
            "content": "先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体，陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明，故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言。深追先帝遗诏，臣不胜受恩感激。今当远离，临表涕零，不知所言",
            "groupid": 0,
            "replayInfo": null,
            "sendMsgType": "TextMsg",
            "sendToType": 1,
            "toUser": 123456789
        }
        ```
        """
        ...

    async def SendQzoneRed(
        self,
        *,
        Hb_type: int,
        Total_num: int,
        Amount: int,
        Content: str,
        Answer: str,
        Paypass: str
    ):
        """
        ## 发送QQ空间口令红包

        - `{"Hb_type":1,"Total_num":1,"Amount":1,"Content":"猜猜看","Answer":"","Paypass":"123456"}`
            - hb_type=3 密码红包
            - hb_type=2 设置问题
            - hb_type=1 口令红包

        ```json
        {
            "Amount": 1,
            "Answer": "",
            "Content": "猜猜看",
            "Hb_type": 1,
            "Paypass": "123456",
            "Total_num": 1
        }
        ```
        """
        ...

    async def SendSingleRed(
        self,
        *,
        RevGroupid: int,
        RecvUid: int,
        Amount: int,
        Paypass: str,
        TotalNum: int,
        Wishing: str,
        Skinid: int,
        RecvType: int,
        RedType: int
    ):
        """
        ## 发送群普通红包

        - `{"RevGroupid":123456789,"RecvUid":123456789,"Amount":1,"Paypass":"123456","TotalNum":1,"Wishing":"测试标题","Skinid":1435,"RecvType":3,"RedType":1}`

        ```json
        {
            "Amount": 4,
            "Paypass": "123456",
            "RecvType": 3,
            "RecvUid": 123456789,
            "RedType": 1,
            "RevGroupid": 123456789,
            "Skinid": 1435,
            "TotalNum": 2,
            "Wishing": "普通红包"
        }
        ```
        """
        ...

    async def SetUniqueTitle(self, *, GroupID: int, UserID: int, NewTitle: str):
        """
        ## 设置头衔

        - `{"GroupID":123456789,"UserID":123456789,"NewTitle":"666669"}`
            - 有频率限制
            - NewTitle ="" 则取消头衔

        ```json
        {
            "GroupID": 123456789,
            "NewTitle": "996",
            "UserID": 123456789
        }
        ```
        """
        ...

    async def ShutUp(
        self, *, ShutUpType: int, GroupID: int, ShutUid: int, ShutTime: int
    ):
        """
        ## 禁言群成员或全员禁言

        - `{"ShutUpType":0,"GroupID":群ID,"ShutUid":被禁言UID,"ShutTime":44640(禁言时间单位为分钟)}`
            - ShutUpType==0 禁言群成员
            - ShutTime=0 取消禁言
            - ShutUpType==1 全员禁言
            - ShutUid=15 全员禁言
            - ShutUid=0 关闭全员禁言

        ```json
        {
            "GroupID": 123456789,
            "ShutTime": 0,
            "ShutUid": 0,
            "ShutUpType": 1
        }
        ```
        """
        ...

    async def Transfer(self, *, TransferUid: int, Amount: int, Paypass: str):
        """
            ## 转账

            - `{"TransferUid":123456789,"Amount":1,"Paypass":"123456"}`

            ```json
            {
                "Amount": 1,
                "Paypass": "123456",
                "TransferUid": 123456789
            }
            ```
            """
        ...

    async def friendlist__GetFriendListReq(self, *, StartIndex: int):
        """
        ## 通用Call获取好友列表

        -

        ```json
        {
            "StartIndex": 0
        }
        ```
        """
        ...

    async def friendlist__GetTroopListReqV2(self, *, NextToken: str):
        """
        ## 通用Call群列表

        -

        ```json
        {
            "NextToken": "AwAAAAD/////ADI="
        }
        ```
        """
        ...

    async def friendlist__GetTroopMemberListReq(self, *, GroupUin: int, LastUin: int):
        """
        ## 通用Call群成员

        -

        ```json
        {
            "GroupUin": 397520425,
            "LastUin": 0
        }
        ```
        """
        ...

    async def friendlist__ModifyGroupCardReq(
        self, *, GroupID: int, UserID: int, NewNick: str
    ):
        """
        ## 通用Call修改群名片

        - `{"CurrentPacket":{"WebConnId":"fi4LFS7_uy8ORrKDQN5Z","Data":{"EventData":{"UserID":103259869,"FromType":2004,"Field_9":1571036852000000,"Content":"收到好友请求 内容我是QQ大冰来源来自QQ群","FromGroupId":123456789,"FromGroupName":"IOTQQ交流群","Action":2},"EventMsg":{"FromUin":103259869,"ToUin":123456789,"MsgType":"ON_EVENT_FRIEND_ADDED","Content":"收到好友请求 内容我是QQ大冰来源来自QQ群","RedBaginfo":null},"EventName":"ON_EVENT_FRIEND_ADD"}},"CurrentQQ":123456789}`
            - 请求参数来自 WebSocket的推送
            - Action 1忽略2同意3拒绝

        ```json
        {
            "GroupID": 123456789,
            "NewNick": "0000001",
            "UserID": 123456789
        }
        ```
        """
        ...
