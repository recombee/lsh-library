from .ABCDataConnect import DataConnect

"""Class for getting data from CSV file."""
class DataCSV(DataConnect):

    """Return data as list of tuples (userid, itemid, rating) from infile in conf_dict"""
    def get_data(self, conf_dic):
        fileread = open(conf_dic["infile"], "r")
        userid = None
        itemid = None
        ratting = None
        for i, column in enumerate(fileread.readline()[:-1].split(sep=',')):
            if column == "userid":
                userid = i
            if column == "itemid":
                itemid = i
            if column == "rating":
                ratting = i

        data = []
        for i in fileread:
            data.append((i[:-1].split(sep=",")[userid],i[:-1].split(sep=",")[itemid],float(i[:-1].split(sep=",")[ratting])))

        return data




