from pathlib import Path
from pandas import read_csv, read_fwf, read_excel, ExcelWriter
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from .utils import *

DOC = '''
xlmerge merges multiple files into a multi-sheet Excel workbook

  Call as:
  xlmerge a.xlsx b.xlsx            # Output to `merged.xlsx` by default
  xlmerge a.csv b.tsv -o abc.xlsx  # Specify output path with -o
  xlmerge *.csv -o abc.xlsx        # Wildcard (*) works with input file paths
'''.strip()
XL_FILE_EXT = { '.xlsx', '.xls', 'xlsm', 'xlsb' }
TABLE_FILE_EXT = { '.csv', '.tsv', '.txt', *XL_FILE_EXT }


def main():
    """Command line program"""
    args = arg_parse()
    merged_tbl = xlmerge(args.inputs)
    write_merged_excel(merged_tbl, outfp=args.output)
    print(f"Output: {args.output}")


def arg_parse():
    cli = ArgumentParser(prog = "xlmerge", description=DOC, 
                         formatter_class=RawDescriptionHelpFormatter)
    cli.add_argument("-o", "--output", default="merged.xlsx", 
                     dest="output", help="Output filepath")
    cli.add_argument("inputs", nargs="+")
    args = cli.parse_args()
    args.output = Path(args.output)

    # Check output fp
    if args.output.suffix not in XL_FILE_EXT:
        UnexpectedFile(f"Output must be an Excel workbook, NOT `{args.output}`")
    
    # Collect input files (with * and ~)
    inputs = []
    for fps in args.inputs:
        for fp in expandpath(fps):
            if fp.suffix in TABLE_FILE_EXT and fp not in inputs and fp.exists():
                inputs.append(fp)
    if len(inputs) == 0:
        FileNotFound(f"Input file doesn't exist: `{', '.join(args.inputs)}`")
    args.inputs = inputs
    return args


def xlmerge(inputs):
    """Merge multiple Excel/CSV tables into a dictionary of `pd.DataFrame`s.

    Parameters
    ----------
    inputs : list
        A list of `pathlib.Path` objects pointing to the file holding 
        input tables (.xlsx/.csv/.tsv...).

    Returns
    -------
    dict
        A dictionary with pd.DataFrames as values and sheet or file names of
        the input files as keys.
    """
    merged_tbl_dict = {}
    for fp in inputs:
        tbls = read_tables(fp)
        for nm, tbl in tbls.items():
            i = 1; nmo = nm
            while nm in merged_tbl_dict: 
                nm = f"{nmo}_{i}"; i += 1
            merged_tbl_dict[nm] = tbl
    return merged_tbl_dict


def write_merged_excel(merged_tbl_dict, outfp):
    with ExcelWriter(outfp) as writer:  
        for nm, df in merged_tbl_dict.items():
            df.to_excel(writer, sheet_name=nm, header=False, index=False)


def read_tables(fp):
    """Reads and returns tables as a dictionary of dataframes"""
    ext = fp.suffix.lower()
    nm = fp.stem
    if ext == '.csv':   tbl = { nm: read_csv(fp, header=None) }
    elif ext == '.tsv': tbl = { nm: read_csv(fp, sep="\t", header=None) }
    elif ext == '.txt': tbl = { nm: read_fwf(fp) }
    elif ext in TABLE_FILE_EXT: 
        tbl = read_excel(fp, sheet_name=None, header=None)
        if len(tbl) == 1:
            if list(tbl.keys())[0].lower() in ( "sheet1", "工作表1" ):
                tbl = { nm: list(tbl.values())[0] }
    else:
        print(fp, ext)
        raise Exception("Unsupported input file types.")
    return tbl


if __name__ == '__main__':
    main()
