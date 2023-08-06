import unittest
from pathlib import Path
from xllib.xlmerge import xlmerge, write_merged_excel

class TestXlmerge(unittest.TestCase):
    files = [ "a.csv", "two-sheets.xlsx", "two-sheets2.xlsx" ]
    files = [ Path(f"test/data/{x}") for x in files ]
    merged_tbl = None

    def test_io(self):
        outfp = Path("test/merged.xlsx")
        self.merged_tbl = xlmerge(inputs=self.files)
        write_merged_excel(self.merged_tbl, outfp)
        self.assertTrue(outfp.exists())
        outfp.unlink()

    def test_sheetnames(self):
        self.test_io()
        ans = [ 'a', '工作表1', '工作表2', '工作表1_1', '工作表2_1' ]
        for nm in self.merged_tbl.keys():
            assert nm == ans.pop(0)

#%%
# lst = [ 1, 2 , 3]
# lst.pop(0)

# %%
if __name__ == '__main__':
    unittest.main()
