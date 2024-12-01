import GlobalSettings
from WordsAndSymbols.Symbol import Symbol

class EmptySymbol(Symbol):
    def __init__(self):
        super().__init__(GlobalSettings.emptySymbol, Id=GlobalSettings.emptySymbolID, IsIdentity=False,IsForbidden=False,Multicharacter=False)