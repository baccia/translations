import argparse
import csv
from typing import Dict, List

import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("muscat_output_file", help="File to output generated by migrate_muscat_translations")
    parser.add_argument("output_csv", help="csvfile to create")
    args = parser.parse_args()

    trans: Dict = yaml.full_load(open(args.muscat_output_file, 'r'))
    out_fields: List = ["field", "subfield", "translation_key"]

    with open(args.output_csv, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=out_fields)
        writer.writeheader()

        for fieldname, value in trans.items():
            d = {
                "field": fieldname,
                "subfield": None,
                "translation_key": value.get("label")
            }
            writer.writerow(d)

            # If there are subfields in this record, write those to the CSV as well.
            if subf := value.get("fields"):
                for subn, subv in subf.items():
                    s = {
                        "field": fieldname,
                        "subfield": subn,
                        "translation_key": subv.get("label")
                    }
                    writer.writerow(s)
