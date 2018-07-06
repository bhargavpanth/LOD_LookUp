from pymongo import MongoClient
import json


def get_all_dataset_names():
    try:
        client = MongoClient('localhost', 27017)
    except Exception as e:
        raise
        print 'Unable to connect to MongoDD - Ensure the collection vocab exists within lodcloud dataset'
    else:
        db = client['lodcloud']
        datasets = db.vocab.distinct("dataset")
        cache_dataset_names(datasets)


def cache_dataset_names(dataset_arr):
    with open('./cache/dataset_dump.json', 'w+') as dataset_dump:
        data = {'datasets': dataset_arr}
        dump = json.dumps(data, indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
        dataset_dump.write(dump)
        print 'dataset names dumped'

def main():
    get_all_dataset_names()

if __name__ == '__main__':
    main()
