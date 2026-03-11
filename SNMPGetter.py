import asyncio
import json
from pysnmp.hlapi.v3arch.asyncio import *
import Logger
import GlobalInfo

async def GetOIDInfo(IP, OID, error):
    if GlobalInfo.Info.extLog : Logger.logger.info(f"Попытка соединения с {IP}")

    try:  
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            SnmpEngine(),
            CommunityData('public', mpModel=1),
            await UdpTransportTarget.create((IP, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(OID))
        )

        if GlobalInfo.Info.log:
            if errorIndication:
                Logger.logger.error(f"ОШИБКА СЕТИ: {errorIndication} у {IP}")
            elif errorStatus:
                Logger.logger.error(f"ОШИБКА SNMP: {errorStatus.prettyPrint()} у {IP}")
            elif GlobalInfo.Info.extLog:
                Logger.logger.info("-"*30)
                Logger.logger.info(f"Соединение успешно, отправка OID: |{OID}| на {IP}")
                Logger.logger.info("-"*30)
                for varBind in varBinds:
                    Logger.logger.info("="*30)
                    Logger.logger.info(f"Ответ от {IP}: |{varBind[1].prettyPrint()}|")
                    Logger.logger.info("="*30)
        bind = None
        for varBind in varBinds:
            bind = varBind[1]
        if error:
            errors = [errorIndication, errorStatus, errorIndex]
            return errors, bind
        return bind

    except Exception as e:
        Logger.logger.error(f"ОШИБКА: {e}")
