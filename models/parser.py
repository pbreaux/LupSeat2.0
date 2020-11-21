import argparse
import string

def parse_args():
    parser = argparse.ArgumentParser(description="Assign seats to students automatically.")
    parser.add_argument("student", help="CSV file containing student list")
    parser.add_argument("seats", help="Yaml file containing room seating info")
    parser.add_argument("--partner", help="CSV file student partner history")
    parser.add_argument("--out", help="Output file", default="out.txt")
    parser.add_argument("--fmt", help="Output format string", default="{sid}")
    parser.add_argument("--gout", help="Output image file", default="out.jpg")
    parser.add_argument("--seed", help="Seed")
    return parser.parse_args()

class SliceFormatter(string.Formatter):
    def get_value(self, key, args, kwds):
        if '|' in key:
            try:
                key, indexes = key.split('|')
                split_indexes = indexes.split(',')

                if len(split_indexes) == 1:
                    # For singular slice
                    index_itr = map(int, [int(split_indexes[0]), int(split_indexes[0])+1])
                elif len(split_indexes) == 2:
                    # For dual ended slice
                    index_itr = map(int, split_indexes)
                else:
                    raise Exception("Slice format incorrect {}".format(key))

                return kwds[key][slice(*index_itr)]
            except KeyError:
                return kwds.get(key, 'Missing')
        return super(SliceFormatter, self).get_value(key, args, kwds)
