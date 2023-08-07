from umls_tools.metathesaurus.metathesaurus_column import MetathesaurusColumn
from umls_tools.umls_file import UmlsFile


class MetathesaurusFile(UmlsFile):

    @property
    def filename(self) -> str:
        return f"{self.name}.RRF"

    MRFILES = "Relation Relation", [
        MetathesaurusColumn.FIL,
        MetathesaurusColumn.DES,
        MetathesaurusColumn.FMT,
        MetathesaurusColumn.CLS,
        MetathesaurusColumn.RWS,
        MetathesaurusColumn.BTS
    ]
    MRCOLS = "Attribute Relation", [
        MetathesaurusColumn.COL,
        MetathesaurusColumn.DES,
        MetathesaurusColumn.REF,
        MetathesaurusColumn.MIN,
        MetathesaurusColumn.AV,
        MetathesaurusColumn.MAX,
        MetathesaurusColumn.FIL,
        MetathesaurusColumn.DTY
    ]
    MRCONSO = "Concept names and sources", [
        MetathesaurusColumn.CUI,
        MetathesaurusColumn.LAT,
        MetathesaurusColumn.TS,
        MetathesaurusColumn.LUI,
        MetathesaurusColumn.STT,
        MetathesaurusColumn.SUI,
        MetathesaurusColumn.ISPREF,
        MetathesaurusColumn.AUI,
        MetathesaurusColumn.SAUI,
        MetathesaurusColumn.SCUI,
        MetathesaurusColumn.SDUI,
        MetathesaurusColumn.SAB,
        MetathesaurusColumn.TTY,
        MetathesaurusColumn.CODE,
        MetathesaurusColumn.STR,
        MetathesaurusColumn.SRL,
        MetathesaurusColumn.SUPPRESS,
        MetathesaurusColumn.CVF
    ]
    MRRANK = "Concept Name Ranking", [
        MetathesaurusColumn.RANK,
        MetathesaurusColumn.SAB,
        MetathesaurusColumn.TTY,
        MetathesaurusColumn.SUPPRESS
    ]
    MRREL = "Related Concepts", [
        MetathesaurusColumn.CUI1,
        MetathesaurusColumn.AUI1,
        MetathesaurusColumn.STYPE1,
        MetathesaurusColumn.REL,
        MetathesaurusColumn.CUI2,
        MetathesaurusColumn.AUI2,
        MetathesaurusColumn.STYPE2,
        MetathesaurusColumn.RELA,
        MetathesaurusColumn.RUI,
        MetathesaurusColumn.SRUI,
        MetathesaurusColumn.SAB,
        MetathesaurusColumn.SL,
        MetathesaurusColumn.RG,
        MetathesaurusColumn.DIR,
        MetathesaurusColumn.SUPPRESS,
        MetathesaurusColumn.CVF
    ]
    MRSTY = "Semantic Types", [
        MetathesaurusColumn.CUI,
        MetathesaurusColumn.TUI,
        MetathesaurusColumn.STN,
        MetathesaurusColumn.STY,
        MetathesaurusColumn.ATUI,
        MetathesaurusColumn.CVF
    ]
