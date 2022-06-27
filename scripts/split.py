import io, os, json

# Splitting the giant json file into smaller files so frontend can process better

def method_1():
    big_json = {}
    with io.open('countries_110.json', mode='r', encoding='utf-8') as f:
        big_json = json.loads(f.read())

    lst = big_json['features']
    features = {}
    for i in lst:
        # features[i['properties']['NAME_EN']] = i
        try:
            if not i['properties']['NAME_EN']:
                print(i['properties']['NAME'])
            if i['properties']['NAME'] == 'Macedonia':
                print(i['properties']['NAME_EN'])
        except:
            print('errored')

    for i in features:
        with open('countries2/'+i+'.json', 'w') as f:
            json.dump(features[i], f)

    total = 0
    for i in os.listdir('countries2'):
        with io.open('countries2/'+i, mode='r', encoding='utf-8') as f:
            total += len(f.read())

def method_2():
    big_json = {}
    with io.open('global.json', mode='r', encoding='utf-8') as f:
        big_json = json.loads(f.read())

    new_json = {}
    for i in big_json.keys():
        lst = list(big_json[i].items())
        lst = lst[::len(lst)//25 or 1]
        new_json[i] = dict(lst)

    with io.open('global.json', mode='w', encoding='utf-8') as f:
        json.dump(new_json, f)