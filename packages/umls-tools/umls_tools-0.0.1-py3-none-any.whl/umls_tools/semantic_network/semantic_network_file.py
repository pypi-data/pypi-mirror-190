from umls_tools.semantic_network.semantic_network_column import SemanticNetworkColumn
from umls_tools.umls_file import UmlsFile


class SemanticNetworkFile(UmlsFile):

    @property
    def filename(self) -> str:
        return self.name

    SRDEF = "Basic information about the Semantic Types and Relations", [
        SemanticNetworkColumn.RT,
        SemanticNetworkColumn.UI,
        SemanticNetworkColumn.STY_RL,
        SemanticNetworkColumn.STN_RTN,
        SemanticNetworkColumn.DEF,
        SemanticNetworkColumn.EX,
        SemanticNetworkColumn.UN,
        SemanticNetworkColumn.NH,
        SemanticNetworkColumn.ABR,
        SemanticNetworkColumn.RIN
    ]
    SRFIL = "File Description", [
        SemanticNetworkColumn.FIL,
        SemanticNetworkColumn.DES,
        SemanticNetworkColumn.FMT,
        SemanticNetworkColumn.CLS,
        SemanticNetworkColumn.RWS,
        SemanticNetworkColumn.BTS
    ]
    SRFLD = "Field Description", [
        SemanticNetworkColumn.COL,
        SemanticNetworkColumn.DES,
        SemanticNetworkColumn.REF,
        SemanticNetworkColumn.FIL
    ]
    SRSTR = "Structure of the Network", [
        SemanticNetworkColumn.STY1,
        SemanticNetworkColumn.RL,
        SemanticNetworkColumn.STY2
    ]
    SRSTRE1 = "Fully inherited set of Relations (UIs)", [
        SemanticNetworkColumn.UI1,
        SemanticNetworkColumn.UI2,
        SemanticNetworkColumn.UI3,
    ]
    SRSTRE2 = "Fully inherited set of Relations (Names)", [
        SemanticNetworkColumn.STY_RL1,
        SemanticNetworkColumn.RL,
        SemanticNetworkColumn.STY_RL2,
        SemanticNetworkColumn.LS
    ]
