try:
    from .const import (  # isort:skip
        __nameMyEnedis__,
        _formatDateYmd,
        _formatDateYm01,
        _formatDateY0101,
    )

except ImportError:
    from const import (  # type: ignore[no-redef]
        __nameMyEnedis__,
        _formatDateYmd,
        _formatDateYm01,
        _formatDateY0101,
    )

import datetime, logging

log = logging.getLogger(__nameMyEnedis__)
from .myCheckData import myCheckData
from .myDataControl import okDataControl


class myDataEnedis:
    def __init__(self, myCalli, token, version, contrat):
        self.myCalli = myCalli
        self._value = 0
        self._date = None
        self._contrat = contrat
        self._token, self._version = token, version
        self._dateDeb = None
        self._dateFin = None
        self._callOk = None
        self._nbCall = 0
        self._data = None

    def CallgetData(self, dateDeb, dateFin):
        val1, val2 = self.myCalli.getDataPeriod(dateDeb, dateFin)
        return val1, val2

    def getValue(self):
        return self._value

    def getDateFin(self):
        return self._dateFin

    def getDateDeb(self):
        return self._dateDeb

    def getCallOk(self):
        return self._callOk

    def getNbCall(self):
        return self._nbCall

    def updateData(
        self,
        clefFunction,
        horairePossible=True,
        data=None,
        dateDeb=None,
        dateFin=None,
        withControl=False,
        dataControl=None,
    ):
        self._nbCall = 0
        onLance = True
        if withControl:
            if okDataControl(clefFunction, dataControl, dateDeb, dateFin):
                onLance = True
                self._callOk = True
            else:
                if not horairePossible:
                    onLance = False
                    # si horaire non ok, on garde quand meme ce qui était passé en parametre..cas du reboot
                    self._data = data
                else:
                    self._callOk = None
                    data = None  # si on doit mettre à jour .... sauf si on est pas la
        if onLance:
            self._dateDeb = dateDeb
            self._dateFin = dateFin
            log.info(
                "--updateData %s ( du %s au %s ) data:%s--"
                % (clefFunction, dateDeb, dateFin, data)
            )
            self._data = data
            if self._data is None:
                if dateDeb == dateFin:
                    self._value = 0
                else:
                    self._data, callDone = self.CallgetData(dateDeb, dateFin)
                    self._nbCall = 1
                    if (callDone) and (myCheckData().checkData(self._data)):
                        self._value = myCheckData().analyseValue(self._data)
                        self._callOk = True
                    else:
                        self._value = 0
                    self._callOk = callDone
            else:
                callDone = True
                if (callDone) and (myCheckData().checkData(self._data)):
                    self._value = myCheckData().analyseValue(self._data)
                    self._callOk = True
                    self._nbCall = 1
                else:
                    self._value = 0
                self._callOk = callDone
            log.info(
                "with update !! %s ( du %s au %s )--" % (clefFunction, dateDeb, dateFin)
            )
            log.info("updateData : data %s" % (self._data))
        else:
            log.info(
                "noupdate !! %s ( du %s au %s )--" % (clefFunction, dateDeb, dateFin)
            )
            log.info("no updateData : data %s" % (self._data))
        return self._data
