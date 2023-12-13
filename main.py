import math


FILE_PATH = 'data.csv'


class Headers:
    order_date = 0
    type = 1
    price = 2
    exclude = 3


def load_data():
    data = []

    with open(FILE_PATH, 'r') as f:
        # skip header row
        f.readline()

        for line in f:
            line = line.strip().split(',')
            data.append(line)

    return data


def transform_prices(data):
    for row in data:
        row[Headers.price] = float(row[Headers.price])


def transform_excluded_individuals(data):
    for row in data:
        if row[Headers.exclude] == '':
            row[Headers.exclude] = []
        else:
            row[Headers.exclude] = row[Headers.exclude].split(';')


def get_name(initial):
    match(initial):
        case 'j':
            return 'jason'
        case 'a':
            return 'alex'
        case 'k':
            return 'kyle'
        case 't':
            return 'tarif'
        case 'h':
            return 'harrison'
        case _:
            raise ValueError(f'Invalid initial: {initial}')


def calculate_meat(dues, contributors, price):
    harrison_percentage = (1/8)

    for contributor in contributors:
        if contributor == 'h':
            dues[contributor] += harrison_percentage * price
        elif 'h' in contributors:
            dues[contributor] += ((1 - harrison_percentage)
                                  * price) / (len(contributors)-1)
        else:
            dues[contributor] += price / len(contributors)


def calculate_tax(dues, contributors, price):
    for contributor in contributors:
        dues[contributor] += price / len(contributors)


def calculate_tip(dues, contributors, price):
    tarif_percentage = (1/10)

    for contributor in contributors:
        if contributor == 't':
            dues[contributor] += tarif_percentage * price
        elif 't' in contributors:
            dues[contributor] += ((1 - tarif_percentage)
                                  * price) / (len(contributors)-1)
        else:
            dues[contributor] += price / len(contributors)


def calculate_normal(dues, contributors, price):
    for contributor in contributors:
        dues[contributor] += price / len(contributors)


def calculate_service_fee(dues, contributors, price):
    tarif_percentage = (1/10)

    for contributor in contributors:
        if contributor == 't':
            dues[contributor] += tarif_percentage * price
        elif 't' in contributors:
            dues[contributor] += ((1 - tarif_percentage)
                                  * price) / (len(contributors)-1)
        else:
            dues[contributor] += price / len(contributors)


def calculate_dues(data):
    dues = {
        'j': 0,
        'a': 0,
        'k': 0,
        't': 0,
        'h': 0,
    }

    for row in data:
        contributors = ['j', 'a', 'k', 't', 'h']

        for excluded in row[Headers.exclude]:
            contributors.remove(excluded)

        match(row[Headers.type]):
            case 'meat':
                calculate_meat(dues, contributors, row[Headers.price])
            case 'tax':
                calculate_tax(dues, contributors, row[Headers.price])
            case 'tip':
                calculate_tip(dues, contributors, row[Headers.price])
            case 'service fee':
                calculate_service_fee(dues, contributors, row[Headers.price])
            case _:
                calculate_normal(dues, contributors, row[Headers.price])

    final_dues = {}

    # round to nearest cent
    for initial, amount in dues.items():
        final_dues[get_name(initial)] = round(amount, 2)

    return final_dues


def main():
    data = load_data()

    transform_prices(data)
    transform_excluded_individuals(data)

    # for row in data:
    #     print(row)

    dues = calculate_dues(data)

    for name, amount in dues.items():
        print(f'{name}: ${amount}')

    print('----------------------------------------')
    print(
        f"Original Total: ${round(sum(row[Headers.price] for row in data), 2)}")
    print(f"Calculated Total: ${round(sum(dues.values()), 2)}")


if __name__ == '__main__':
    main()
