import GlobalSettings
from WordsAndSymbols.Symbol import Symbol

class AnySymbol(Symbol):
    def __init__(self):
        super().__init__(GlobalSettings.anySymbol, Id=GlobalSettings.anySymbolID, IsIdentity=False,IsForbidden=False,Multicharacter=False)