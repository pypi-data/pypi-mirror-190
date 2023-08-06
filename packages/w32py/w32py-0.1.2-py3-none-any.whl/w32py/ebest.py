from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable

from loguru import logger
from win32com.client import EventsProxy

from w32py.win import dispatchWithEvents, pumpWaitingMessages


class CALLBACK:
    OnDisconnect: list[Callable[[], None]] = []
    OnReceiveData: list[Callable[[dict[str, Any]], None]] = []
    OnReceiveRealData: list[Callable[[dict[str, Any]], None]] = []


class SESSION_STATUS(Enum):
    DISCONNECT = auto()
    LOGIN_SUCCEEDED = auto()
    LOGIN_FAILED = auto()


class XASessionEvents:
    def __init__(self) -> None:
        self.__debug = False
        self.__status = SESSION_STATUS.DISCONNECT

    def init(self, *, debug: bool = False) -> None:
        self.__debug = debug
        self.__status = SESSION_STATUS.DISCONNECT

    def __disconnect(self) -> None:
        self.DisconnectServer()  # type: ignore
        self.__status = SESSION_STATUS.DISCONNECT

    def __lastError(self, prefix: str) -> str:
        nErrCode: int = self.GetLastError()  # type: ignore
        strErrMsg: str = self.GetErrorMessage(nErrCode)  # type: ignore
        return f"{prefix}, {nErrCode}, {strErrMsg}"

    def login(
        self,
        szID: str,
        szPwd: str,
        szCertPwd: str,
        *,
        nServerType: int = 0,
        szServerIP: str = "hts.ebestsec.co.kr",
        nServerPort: int = 20001,
    ) -> str:
        self.__disconnect()
        bConnect: bool = self.ConnectServer(  # type: ignore
            szServerIP,
            nServerPort,
        )
        if not bConnect:
            return self.__lastError("ConnectServer")

        bLogin: bool = self.Login(  # type: ignore
            szID,
            szPwd,
            szCertPwd,
            nServerType,
            False,
        )
        if not bLogin:
            return self.__lastError("Login")

        while self.__status == SESSION_STATUS.DISCONNECT:
            pumpWaitingMessages()

        if self.__status == SESSION_STATUS.LOGIN_SUCCEEDED:
            return ""
        return "LOGIN_FAILED"

    def OnLogin(self, szCode: str, szMsg: str) -> None:
        if self.__debug:
            logger.debug(f"{szCode}, {szMsg}")

        if szCode == "0000":
            self.__status = SESSION_STATUS.LOGIN_SUCCEEDED
            return

        logger.error(f"{szCode}, {szMsg}")
        self.__status = SESSION_STATUS.LOGIN_FAILED

    def OnLogout(self) -> None:
        logger.error("")
        self.__disconnect()
        for OnDisconnect in CALLBACK.OnDisconnect:
            OnDisconnect()

    def OnDisconnect(self) -> None:
        logger.error("")
        self.__disconnect()
        for OnDisconnect in CALLBACK.OnDisconnect:
            OnDisconnect()


def parse_field(line: str) -> dict[str, Any]:
    cols = line.split(",")
    return {
        "name": cols[1].strip(),
        "desc": cols[0].strip(),
        "type": cols[3].strip(),
        "size": cols[4].strip(),
    }


def parse_lines(lines: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    lines = list(
        filter(lambda x: x, map(lambda x: x.strip().replace(";", ""), lines))
    )
    for i, line in enumerate(lines):
        if ".Func" in line or ".Feed" in line:
            parsed["desc"] = line.split(",")[1].strip()
        elif line == "begin":
            latest_begin = i
        elif line == "end":
            block_info = lines[latest_begin - 1].split(",")
            block_info2 = block_info[2]
            if block_info2 not in parsed:
                parsed[block_info2] = {}
            parsed[block_info2][block_info[0]] = {
                "occurs": "occurs" in block_info,
                "fields": list(map(parse_field, lines[latest_begin + 1 : i])),
            }
    return parsed


def parse_res(p: Path) -> dict[str, Any]:
    with open(p, "rt", encoding="cp949") as fp:
        return parse_lines(fp.readlines())


class XAQueryEvents:
    def __init__(self) -> None:
        self.__debug = False
        self.__tr = ""
        self.__meta: dict[str, Any] = {}
        self.__received = False

    def init(self, p: Path, *, debug: bool = False) -> None:
        self.__debug = debug
        self.__tr = f"{p.stem}"
        self.__meta = parse_res(p)
        self.__received = False
        self.ResFileName = f"{p}"

    def __lastError(self, prefix: str) -> str:
        nErrCode: int = self.GetLastError()  # type: ignore
        strErrMsg: str = self.GetErrorMessage(nErrCode)  # type: ignore
        return f"{prefix}, {nErrCode}, {strErrMsg}"

    def request(self, requestQuery: dict[str, Any]) -> str:
        if self.__debug:
            logger.debug(f"{requestQuery}")

        requestBlock = requestQuery["block"]
        for szBlockName, v in self.__meta["input"].items():
            fields = v["fields"]

            def setBlock(
                block: dict[str, Any], *, nOccursIndex: int = 0
            ) -> str:
                for field in fields:
                    field_name = field["name"]
                    val = block.get(field_name)
                    if val is None:
                        return (
                            f"InvalidField, {szBlockName}"
                            f", {field_name}, {nOccursIndex}"
                        )
                    field_type = field["type"]
                    if field_type == "long":
                        if not isinstance(val, int):
                            return (
                                f"InvalidFieldType, {szBlockName}"
                                f", {field_name}, {nOccursIndex}"
                                f", {field_type}, {type(val)}"
                                f", {val}"
                            )
                    elif field_type in {"double", "float"}:
                        if not isinstance(val, float):
                            return (
                                f"InvalidFieldType, {szBlockName}"
                                f", {field_name}, {nOccursIndex}"
                                f", {field_type}, {type(val)}"
                                f", {val}"
                            )
                    else:
                        if not isinstance(val, str):
                            return (
                                f"InvalidFieldType, {szBlockName}"
                                f", {field_name}, {nOccursIndex}"
                                f", {field_type}, {type(val)}"
                                f", {val}"
                            )
                    self.SetFieldData(  # type: ignore
                        szBlockName, field_name, nOccursIndex, val
                    )
                return ""

            if v["occurs"]:
                blocks = requestBlock.get(szBlockName)
                if blocks is None:
                    return f"InvalidBlock, {szBlockName}"
                if not isinstance(blocks, list):
                    return f"InvalidBlockType, {szBlockName}, list, {type(blocks)}"
                for i, block in enumerate(blocks):
                    if not isinstance(block, dict):
                        return f"InvalidBlockType, {szBlockName}, {i}, dict, {type(block)}"
                    err = setBlock(block)
                    if err:
                        return err
            else:
                block = requestBlock.get(szBlockName)
                if block is None:
                    return f"InvalidBlock, {szBlockName}"
                if not isinstance(block, dict):
                    return (
                        f"InvalidBlockType, {szBlockName}, dict, {type(block)}"
                    )
                err = setBlock(block)
                if err:
                    return err

        rc: int = self.Request(requestQuery["cont"])  # type: ignore
        if rc < 0:
            return self.__lastError("Request")

        while not self.__received:
            pumpWaitingMessages()
        return ""

    def OnReceiveData(self, szTrCode: str) -> None:
        block: dict[str, Any] = {}
        for szBlockName, v in self.__meta["output"].items():
            fields = v["fields"]

            def getBlock(*, nRecordIndex: int = 0) -> dict[str, Any]:
                block: dict[str, Any] = {}
                for field in fields:
                    field_name = field["name"]
                    data = self.GetFieldData(  # type: ignore
                        szBlockName, field_name, nRecordIndex
                    )
                    field_type = field["type"]
                    if field_type == "long":
                        if data == "-":
                            block[field_name] = 0
                        else:
                            block[field_name] = int(data or 0)
                    elif field_type in {"double", "float"}:
                        block[field_name] = float(data or 0.0)
                    else:
                        block[field_name] = f"{data}"
                return block

            if v["occurs"]:
                l = []
                n = self.GetBlockCount(szBlockName)  # type: ignore
                for i in range(n):
                    l.append(getBlock(nRecordIndex=i))
                block[szBlockName] = l
            else:
                block[szBlockName] = getBlock()
        responseQuery = {
            "err": "",
            "tr": szTrCode,
            "block": block,
        }
        if self.__debug:
            logger.debug(f"{responseQuery}")
        self.__received = True
        for OnReceiveData in CALLBACK.OnReceiveData:
            OnReceiveData(responseQuery)

    def OnReceiveMessage(
        self, bIsSystemError: int, nMessageCode: str, szMessage: str
    ) -> None:
        if self.__debug:
            logger.debug(f"{bIsSystemError}, {nMessageCode}, {szMessage}")

        if bIsSystemError == 0 and nMessageCode[0] == "0":
            return

        responseQuery = {
            "err": f"{bIsSystemError}, {nMessageCode}, {szMessage}",
            "tr": self.__tr,
            "block": {},
        }
        self.__received = True
        for OnReceiveData in CALLBACK.OnReceiveData:
            OnReceiveData(responseQuery)


class XARealEvents:
    def __init__(self) -> None:
        self.__debug = False
        self.__tr = ""
        self.__meta: dict[str, Any] = {}
        self.__keys: set[str] = set()

    def init(self, p: Path, *, debug: bool = False) -> None:
        self.__debug = debug
        self.__tr = f"{p.stem}"
        self.__meta = parse_res(p)
        self.__keys = set()
        self.ResFileName = f"{p}"

    def advise(self, requestReal: dict[str, Any]) -> str:
        if self.__debug:
            logger.debug(f"{requestReal}")

        key = requestReal["key"]
        if key in self.__keys:
            return ""

        if key:
            self.SetFieldData(  # type: ignore
                "InBlock",
                self.__meta["input"]["InBlock"]["fields"][0]["name"],
                key,
            )
        self.AdviseRealData()  # type: ignore
        self.__keys.add(key)
        return ""

    def unadvise(self, requestReal: dict[str, Any]) -> str:
        if self.__debug:
            logger.debug(f"{requestReal}")

        key = requestReal["key"]
        if key not in self.__keys:
            return ""

        if key:
            self.UnadviseRealDataWithKey(key)  # type: ignore
        else:
            self.UnadviseRealData()  # type: ignore
        self.__keys.remove(key)
        return ""

    def OnReceiveRealData(self, szTrCode: str) -> None:
        block = {}
        for szBlockName, v in self.__meta["output"].items():
            fields = v["fields"]

            def getBlock() -> dict[str, Any]:
                block = {}
                for field in fields:
                    field_name = field["name"]
                    data = self.GetFieldData(  # type: ignore
                        szBlockName,
                        field_name,
                    )
                    field_type = field["type"]
                    if field_type == "long":
                        if data == "-":
                            block[field_name] = 0
                        else:
                            block[field_name] = int(data or 0)
                    elif field_type in {"double", "float"}:
                        block[field_name] = float(data or 0.0)  # type: ignore
                    else:
                        block[field_name] = f"{data}"  # type: ignore
                return block

            block[szBlockName] = getBlock()
        if self.__meta["input"]["InBlock"]:
            field_name = self.__meta["input"]["InBlock"]["fields"][0]["name"]
            key = block["OutBlock"][field_name]
        else:
            key = ""
        responseReal = {
            "err": "",
            "tr": szTrCode,
            "key": key,
            "block": block,
        }
        if self.__debug:
            logger.debug(f"{responseReal}")
        for OnReceiveRealData in CALLBACK.OnReceiveRealData:
            OnReceiveRealData(responseReal)


class Meta:
    def __init__(
        self, *, path: str = "C:/eBEST/xingAPI/Res", debug: bool = False
    ) -> None:
        self.__debug = debug
        self.__path = Path(path)
        self.__XASession = dispatchWithEvents(
            "XA_Session.XASession", XASessionEvents
        )
        self.__XASession.init(debug=self.__debug)
        self.__XAQueryDict: dict[str, EventsProxy] = {}
        self.__XARealDict: dict[str, EventsProxy] = {}

    def __enter__(self) -> Any:
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.__XASession.DisconnectServer()

    def exists(self, szTrCode: str) -> tuple[bool, Path]:
        p = self.__path / f"{szTrCode}.res"
        return p.exists(), p

    def getXASession(self) -> EventsProxy:
        return self.__XASession

    def getXAQuery(self, szTrCode: str) -> EventsProxy | None:
        obj = self.__XAQueryDict.get(szTrCode)
        if obj is None:
            b, p = self.exists(szTrCode)
            if not b:
                return None
            obj = dispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
            obj.init(p, debug=self.__debug)
            self.__XAQueryDict[szTrCode] = obj
        return obj

    def getXAReal(self, szTrCode: str) -> EventsProxy | None:
        obj = self.__XARealDict.get(szTrCode)
        if obj is None:
            b, p = self.exists(szTrCode)
            if not b:
                return None
            obj = dispatchWithEvents("XA_DataSet.XAReal", XARealEvents)
            obj.init(p, debug=self.__debug)
            self.__XARealDict[szTrCode] = obj
        return obj

    def login(
        self,
        szID: str,
        szPwd: str,
        szCertPwd: str,
        *,
        nServerType: int = 0,
        szServerIP: str = "hts.ebestsec.co.kr",
        nServerPort: int = 20001,
    ) -> str:
        obj = self.getXASession()
        return obj.login(  # type: ignore
            szID,
            szPwd,
            szCertPwd,
            nServerType=nServerType,
            szServerIP=szServerIP,
            nServerPort=nServerPort,
        )

    def query(self, requestQuery: dict[str, Any]) -> str:
        tr = requestQuery["tr"]
        obj = self.getXAQuery(tr)
        if obj is None:
            return f"FileNotFound, {tr}.res"
        return obj.request(requestQuery)  # type: ignore

    def advise(self, requestReal: dict[str, Any]) -> str:
        tr = requestReal["tr"]
        obj = self.getXAReal(tr)
        if obj is None:
            return f"FileNotFound, {tr}.res"
        return obj.advise(requestReal)  # type: ignore

    def unadvise(self, requestReal: dict[str, Any]) -> str:
        tr = requestReal["tr"]
        obj = self.getXAReal(tr)
        if obj is None:
            return f"FileNotFound, {tr}.res"
        return obj.unadvise(requestReal)  # type: ignore
