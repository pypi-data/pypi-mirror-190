import xlwings as xw
from pathlib import Path
from argparse import ArgumentParser, RawDescriptionHelpFormatter

DOC = '''
  xlstyle applies formats from a source sheet to a target sheet in Excel

  Call as:
  xlstyle src.xlsx tgt.xlsx
  xlstyle src.xlsx tgt.xlsx -o tgt2.xlsx
  xlstyle s.xlsx t.xlsx --sheet=2,3  # s.xlsx 2nd sheet -> t.xlsx 3rd sheet
  xlstyle src.xlsx tgt.xlsx --rng "A:B"
'''.strip()

def main():
    args = arg_parse()
    wb1 = xw.Book(args.src_file)
    wb2 = xw.Book(args.tgt_file)

    if args.sheet is None:
        apply_workbook(wb1, wb2, rng=args.rng)
    else:
        apply_worksheet(wb1, wb2, rng=args.rng, sheet_idx=args.sheet)
    
    wb2.save(args.output)
    
    # Close excel windows
    # wb1.close()
    # wb2.close()
    app = xw.apps.active
    app.quit()


def arg_parse():
    cli = ArgumentParser(prog = "xlstyle", description=DOC, 
                         formatter_class=RawDescriptionHelpFormatter)
    cli.add_argument("src_file", help="File holding formats to be copied")
    cli.add_argument("tgt_file", help="File to apply formats to")
    cli.add_argument("--rng", dest="rng", default="1:65536",
                     help='Range to apply, e.g. "A:D", "B1:AD200"')
    cli.add_argument("-o", "--output", dest="output", help="Output filepath")
    cli.add_argument("--sheet", dest="sheet", help="Source and target workbook sheet index")
    args = cli.parse_args()
    
    args.src_file = Path(args.src_file)
    args.tgt_file = Path(args.tgt_file)
    exts = [ '.xlsx', '.xls', '.xlsm', '.xlsb' ]
    if args.src_file.suffix not in exts:
        raise Exception(f"Invalid source file, needs to be one of {', '.join(exts)}")
    if args.output is None and args.tgt_file.suffix not in exts:
        args.output = args.tgt_file.parent / f"{args.tgt_file.stem}.xlsx"
    return args


def apply_workbook(wb1, wb2, rng):
    # 1. Same num of worksheets
    len_wb2 = len(wb2.sheets)
    if len(wb1.sheets) == len_wb2:
        for i in range(len_wb2):
            ws1 = wb1.sheets[i]
            ws2 = wb2.sheets[i]
            format_sheet(src=ws1, tgt=ws2, rng=rng)
    # 2. Only one sheet in src
    elif len(wb1.sheets) == 1:
        for i in range(len_wb2):
            ws2 = wb2.sheets[i]
            format_sheet(src=wb1.sheets[0], tgt=ws2, rng=rng)
    # 3. Diff num of worksheets -> apply first
    else:
        ws1 = wb1.sheets[0]
        ws2 = wb2.sheets[0]
        format_sheet(src=ws1, tgt=ws2, rng=rng)


def apply_worksheet(wb1, wb2, rng, sheet_idx="1,2"):
    idx = [ int(i) - 1 for i in sheet_idx.split(",") ]
    ws1 = wb1.sheets[idx[0]]
    ws2 = wb2.sheets[idx[1]]
    format_sheet(src=ws1, tgt=ws2, rng=rng)


def format_sheet(src, tgt, rng):
    src.range(rng).copy()                  # Copy style to clipboard
    tgt.range(rng).paste(paste="formats")  # Paste to target


if __name__ == '__main__':
    main()


# #%%
# import xlwings as xw
# from pathlib import Path

# ws1 = xw.Book("src.xlsx").sheets[0]
# ws2 = xw.Book("tgt.xlsx").sheets[0]

# def format_sheet(src, tgt, rng):
#     src.range(rng).copy()                  # Copy style to clipboard
#     tgt.range(rng).paste(paste="formats")  # Paste to target

# format_sheet(ws1, ws2, rng=None)

# %%
# tgt, src = "data/tables.tsv", "data/item analysis.xls"
# tgt_sheet, src_sheet = 0, 0
# rng = "A:R"
# out = "tables.xlsx"

# # Load sheets
# target = xw.Book(tgt)
# style = xw.Book(src)
# src_sheet = style.sheets[src_sheet]
# tgt_sheet = target.sheets[tgt_sheet]

# # Copy style from src to tgt
# src = src_sheet.range(rng)
# src.copy()
# tgt_sheet.range(rng).paste(paste="formats")

# # Save new workbook
# target.save(path=out)
# target.close()
# style.close()