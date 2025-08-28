"""Benchmarking the new regex implementation against the old one."""

import argparse
import time
from words import Words
from words.words_regex import WordsRegexSet


regexes: list[str] = {'.EUPI', '...G', 'ESIO', 'I...YT', 'EGPO', '..FG',
    'O.MGGI', 'O...TI', 'N.O..R', '.LQUA', 'ETTO', 'I...TT', '..Q.G',
    'T...I', 'ESTO', '..IVI', 'I..UTA', '..QSA', '.OOZI', 'O.CGGI',
    'EGTO', '....T', '..DIG', 'ECIO', 'EPIO', '..NUO', 'EFTO', 'O.NGGI',
    '.FAG', 'ECPO', 'N.O..L', 'TORNI', 'EPTO', '...TG', '..SM', '.AGUO',
    '..QMA', '.....A', '..EG', 'O.HGGI', '...LAI', 'EBIO', '..OAT',
    'O..LGI', '.UUPI', '..ENG', '.ILG.', '..ZM', '..LM', '.OIG', '...GG',
    'I...FT', '.IQG.', '..VG', '.I.N.', '.DIG', 'TINNI', '.AESE', 'T.UNI',
    'W....', 'EETO', '..QUA', '.I.W.', 'I...FR', 'I...IM', '..UZI', '..OIG',
    '..TAT', '.CAG', '..VAT', 'O.....', 'O..GGI', 'L....', 'N.O..D', '...VG',
    'ELPO', 'N...', '...L', '..OM', '.VAG', 'I...', '..GIG', '..QBA', 'EFPO',
    'T...A', '.OIMAI', '..AM', 'C...RO', 'T.SNI', '.....O', 'EITO', 'N.E...',
    '.OQUA', 'Y............', '...CT', '.AOZI', 'N.O..V', '.AOAT', '.HOAT',
    'EUTO', '.ROAT', '...DG', '..EIG', 'ENPO', 'A............', 'O.DGGI',
    '.HAG', '.....U', '.UESE', '..PAT', '..OZI', 'C...EO', '.LAG', '..Q.A',
    '..ILAI', 'T.LNI', 'I...FM', 'Y...', 'Z............', '.JIG', '.IIG.',
    '..RG', '....O', '...RG', 'HI..', 'U............', '..TUO', '...EG',
    '.AILAI', '.RESE', 'I...UT', '.IUG.', 'TONNI', 'I...YA', 'O..AGI',
    'P...', '...T', '.EOAT', 'ESPO', 'ETIO', 'T.RNI', '.LIG', '...MAI',
    '.BAG', 'I....M', 'EIIO', 'E....O', '..AVI', '.I.Y.', 'N.O..B', 
    'T.CNI', '..RM', '...R', 'T.MNI', '..PM', '.FIG', 'ECTO', '.VIG',
    'O.QGGI', 'L...', '.IUPI', '..UEI', 'L............', 'T.BNI', 'EDIO',
    '..MG', 'E.NO', 'T.ANI', '.LILAI', 'P............', '.TAG', 'EZTO',
    'I....O', '.IILAI', 'E.EO', 'EZIO', '..HG', 'N.O..T', '.IAG', '...SE',
    '..ASE', '.I.R.', '....OI', 'A....O', '.ING.', 'E.AO', 'I...PR', '..AAT',
    'I...GT', 'EMTO', '....E', 'O..ZGI', 'I...TR', 'I..ATA', '..OEI', 'I...NR',
    'N.O...', '..QRA', 'O.FGGI', 'E.OO', 'H...', 'TENNI', '.EESE', 'C...', '..GUO',
    '...I', 'E.VO', '...C', '..CUO', '..GG', '..IEI', '...IG', '...XG', '.RIMAI',
    'EGIO', '.UOAT', '..BUO', 'E............', 'T.GNI', '..PG', '.TIG',
    '..LG', '..ZG', '...SO', 'S....', '..DAT', '..BM', '.UGUO', '.OILAI',
    '.RUPI', '.....I', '.LESE', '.IFG.', '.UIG', '.IESE', 'F.....', '.LIMAI',
    'O.TGGI', '..API', 'N.O..G', '...N', 'N.U...', 'O.VGGI', 'T.PNI', 'O..EGI',
    '...MI', '..Q.H', 'T.VNI', 'N.O..M', '.AIG', 'I...ST', 'C...IO', 'I.....',
    '..ANI', '..QOA', '..AEI', 'O...CI', '.LUPI', '..QGA', 'O.LGGI', 'TURNI',
    'E.PO', '...DT', 'T.INI', '...MG', '.GIG', '.UQUA', '..GM', 'A.....',
    'E.GO', 'S............', '.IDG.', '.KIG', '...A', '..DM', '..LIG', 
    'B...',
    '.HIG', '..TM', '.RQUA', '.BIG', '.OESE', '.....R', '.PAG', '.IVG.', '.IIMAI',
    'I....B', 'I...OR', 'F....', '..IAT', '.UILAI', '.AUPI', '...ST', '.LOAT',
    'O.BGGI', '...MT', 'C....', '.OGUO', 'A...', 'O..UGI', 'O..RGI', 'B............',
    '..UPI', '..NM', '...EI', '.ISG.', 'E..O', '.DAG', '.UAG', '.MIG', 'ELTO',
    '....EI', '.IPG.', 'C....O', '.SAG', '...AT', 'C...NO', '.QIG', '..EAT',
    'O.AGGI', '.RILAI', 'ENIO', 'O.UGGI', '...ZI', 'D............', 'T...E',
    'T...', '...M', '.IIG', 'R....', '..QNA', 'O...LI', 'T..NI', '..SG', 'O.OGGI',
    '...SG', '.GAG', 'E.IO', '.EILAI', '...NI', '..IM', 'O.KGGI', 'I...YR', '..GAT',
    '..BG', 'D...', '..Q.D', 'O..CGI', '...SA', '.AING', '....', '.EQUA', 'U...',
    'E.TO', '..OUO', '.EAG', 'EATO', '..QLA', 'G...', 'TYRNI', 'C...LO', '.NIG', 'O..MGI',
    'E.HO', '..UUO', '..SUO', '.I.G.', '...EOI', '.I.T.', '....I', 'O...GI', '.AIMAI',
    '..LUO', '..OG', 'N............', '.EGUO', 'I....A', 'N.O..S', '..UNI', '..QFA',
    '..USE', 'I...TA', '....G', 'C............', 'O.GGGI', '..DG', '...TT',
    'O............', '..Q.E', '..AG', '..ONG', '.HING', 'O...', 'H............',
    '.EING', '...II', '..CAT', 'HO..', '..NAT', '..EM', 'I............', 'V............',
    '.IMG.', '....AI', 'HE..', 'N.O..F', 'TANNI', '..ESE', '.IOZI', 'C...OO', 'O...AI',
    'F...', '.RIG', 'T............', '....R', '.....E', '.XIG', 'ENTO', '.MAG', '.HIMAI', 
    '...VI', 'I...SM', '.I.A.', 'TUNNI', 'N.O..C', '...O', 'TARNI', 'F............', '..OAG',
    '.ZIG', '.IGG.', 'T.TNI', '.I.L.', '..ING', 'N.A...', 'EVTO', 'O.PGGI', 'N.O..U', 'R...',
    '...UO', '.UIMAI', '...LG', '......', '..Q.I', '..QEA', '.NAG', '..IG', 'EDPO', 'V...',
    'EAIO', '..VM', 'C...KO', 'J...', '.AAG', 'T.ZNI', '.PIG', '.UOZI', '.QAG', 'TERNI',
    'O..TGI', 'R............', '.ROZI', '..ONI', '.IRG.', '..MIG', 'EAPO', 'I....T',
    'M............', 'EOPO', '..IMAI', '.RAG', '..ISE', 'P.....', 'N.O..E', '...AG',
    'I....R', '.OUPI', 'N.O..Z', '...NG', '....A', '..AZI', '..OPI', 'E..I', 'T.FNI',
    '..Q.N', 'EOIO', '.IXG.', '.WIG', '....L', 'HU..', 'I...IR', 'G............', 'EOTO',
    '..UVI', '.CIG', 'E..C', 'C...AO', 'E.LO', 'EFIO', 'I...OT', 'O.IGGI', 'N.O..N', '..NG',
    '.AQUA', '..IAG', 'C...PO', '..FM', 'M....', 'I...GR', 'O..NGI', 'E.....', '.HILAI', '..IIG',
    'HA..', 'EIPO', '...PI', '.ICG.', '.FOAT', '..DUO', 'I...BR', '..QTA', '.....', '..TG', '.SIG',
    'E.MO', 'C...DO', 'K...', 'ELIO', 'O..PGI', 'ERTO', 'ERPO', '.IBG.', '..CG', 'E.BO', '.EIG',
    'EDTO', 'I...PT', '..AIG', '..UG', '..LAT', '.IQUA', '.EOZI', 'N.O..P', 'T.NNI', 'E.RO',
    'O.EGGI', 'I...OM', '..RAT', 'O..VGI', 'TIRNI', '...KG', '.IGUO', '....II', 'O..SGI',
    '.LOZI', '.IOG.', '.ITG.', 'ETPO', '.IING', '.ZILAI', 'EMIO', '.SESE', '.OOAT', '.IOAT',
    '.OAG', 'M...', 'EZPO', '..MM', '..CM', 'E...', 'S...', 'E.DO', 'T....', '..INI', '.EIMAI',
    '...ZG'}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark regex implementations with a word list.")
    parser.add_argument('--words', type=str, default='words.txt', help='Path to words.txt file')
    args = parser.parse_args()

    words = Words(args.words, 100, True)
    start = time.perf_counter()
    for regex in regexes:
        result = words.get_words_with_regex(regex, len(regex))
    end = time.perf_counter()
    print(f"Elapsed: {end - start:.2f} seconds")
    print("----- Backup -----")
    words_bkp = WordsRegexSet(args.words, 100, True)
    start_bkp = time.perf_counter()
    for regex in regexes:
        result_bkp = words_bkp.get_words_with_regex(regex, len(regex))
    end_bkp = time.perf_counter()
    print(f"Elapsed: {end_bkp - start_bkp:.2f} seconds")
