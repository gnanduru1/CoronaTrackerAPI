import io, os, json

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

# for i in features:
#     with open('countries2/'+i+'.json', 'w') as f:
#         json.dump(features[i], f)

# total = 0
# for i in os.listdir('countries2'):
#     with io.open('countries2/'+i, mode='r', encoding='utf-8') as f:
#         total += len(f.read())