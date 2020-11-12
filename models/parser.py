import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Assign seats to students automatically.")
    parser.add_argument("student", help="CSV file containing student list")
    parser.add_argument("seats", help="Yaml file containing room seating info")
    parser.add_argument("--partner", help="CSV file student partner history")
    parser.add_argument("--out", help="Output file", default="out.txt")
    parser.add_argument("--gout", help="Output image file", default="out.jpg")
    parser.add_argument("--seed", help="Seed")
    return parser.parse_args()
