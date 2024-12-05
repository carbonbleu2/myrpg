import csv

class CSVUtils:
    @staticmethod
    def import_map(file_name):
        terrain_map = []
        with open(file_name) as map:
            layout = csv.reader(map, delimiter=',')
            for row in layout:
                terrain_map.append(list(row))
        return terrain_map