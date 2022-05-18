import csv, re, json

# All information is gathered from the California data broker registry
# additional information about a company is not necessary because
# information about data brokers are displayed like gmail
# i.e. text only
# it is then exported to a json file 
# i don't have much time rn

URL_PATTERN = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
EMAIL_PATTERN = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')

def main():
    final_json = {'brokers': []}
    with open('data-brokers.csv') as fp:
        brokers = csv.reader(fp, delimiter=',')
        for i, row in enumerate(brokers):
            if i > 0:
                broker = dict()
                broker['name'] = row[0]
                broker['email'] = re.sub(r' \[at\] ', '@', row[1])
                broker['website_url'] = row[2]

                try: 
                    broker['opt_out_url'] = URL_PATTERN.match(row[4]).group()
                except AttributeError:
                    pass
                try: 
                    broker['email'] = EMAIL_PATTERN.search(row[4]).group()
                except AttributeError:
                    pass
                final_json['brokers'].append(broker)
    with open('data-brokers.json', 'w+') as fp:
        fp.write(json.dumps(final_json))

if __name__ == '__main__':
    main()
