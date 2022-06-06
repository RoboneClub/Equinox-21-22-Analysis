import csv

class CsvHandler:
    def get_records(self, filename: str) -> list:
        with open(filename, mode='r') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            records = []
            for record in dict_reader:
                records.append(record)
        return records