import csv


def prepare_csv_data(data: dict, key: str, columns: list) -> list:
    csv_data = []
    for name, properties in get_data(data, key).items():
        row = []
        for column in columns:
            if column == 'name':
                row.append(name)
                continue
            if column not in properties:
                row.append('')
            else:
                row.append(properties[column])
        csv_data.append(row)
    return csv_data


def get_data(data: dict, key: str) -> dict:
    return safeget(data, key.split('.'))


def safeget(dct, keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def output_csv(columns: list, rows: list, output) -> None:
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)
