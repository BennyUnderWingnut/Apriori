import apriori

# Train model and write to file

# support = minimum number of lines containing a group of items
# needed to consider the group appears frequently

# a line of data is valid only if
# min_set_size <= number of items in the line <= max_sey_size

AP = apriori.APriori(data='./test_datasets/transactions.dat',
                     out='./test_datasets/result.txt')
AP.find_frequent(support=50, min_set_size=2, max_set_size=3)

# Read trained data from file

# wanted_items = [items needing to be found]

# detected_items = [items detected by other procedures]
'''
AP.read_data(data_file='./test_datasets/result.txt')
frequent_list = AP.get_frequent_list_of(
    wanted_items=[36], detected_items=[38, 39])
print(frequent_list[36])
'''