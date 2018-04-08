# Python 3 Implementation of Apriori algorithm

This program is based on [Aaron Zira's implementation of Apriori algorithm](https://github.com/aaronzira/apriori) and is adapted for use in other python 3 programs

## Dependencies

This program uses [_demjson.py_](https://github.com/dmeranda/demjson/blob/master/demjson.py) to write matrix into file

* Install with

```bash
   pip3 install demjson
```

## Usage

* Initialize and learn frequency using data from file

```python 3
# data: path of data source file
# out: path of output file
AP = apriori.APriori(data='./test_datasets/transactions.dat',
out='./test_datasets/result.txt')

# This function will write Data into output file
AP.find_frequent(support=50, min_set_size=2, max_set_size=3)
```

* Initialize and get learned frequency from previous output file

```python 3
AP.read_data(data_file='./test_datasets/result.txt')

# wanted_items: list of items needing to be found
# detected_items: list of items detected by other procedures
frequent_list = AP.get_frequent_list_of(
    wanted_items=[36], detected_items=[38, 39])
print(frequent_list[36])
```