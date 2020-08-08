from typing import Any, Dict, Optional

from pydantic import BaseModel

Data_T = Dict[str, Any]


class MessageModelBase(BaseModel):
    class Config:
        orm_mode = True

    def __getitem__(self, key: str) -> Any:
        return dict(self)[key]


class MessageDataBase(MessageModelBase):
    MsgType: str
    Content: str
    MsgSeq: int
    RedBaginfo: Optional[Data_T] = None


class MessageBase(MessageModelBase):
    CurrentQQ: int
    WebConnId: str


class GroupMessageData(MessageDataBase):
    FromGroupId: int
    FromGroupName: str

    FromUserId: int
    FromNickName: str

    MsgRandom: int


class GroupMessage(MessageBase):
    Data: GroupMessageData


class FriendMessageData(MessageDataBase):
    FromUin: int
    ToUin: int


class FriendMessage(MessageBase):
    Data: FriendMessageData


class EventMessageData(MessageDataBase):
    FromUin: int
    ToUin: int


class EventDataStructure(MessageModelBase):
    EventName: str
    EventData: Data_T
    EventMsg: EventMessageData


class EventMessage(MessageBase):
    Data: EventDataStructure
