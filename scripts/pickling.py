import pickle
from collections import OrderedDict

# write 
weights_rec = (['2022-09-30', '2022-10-31', '2022-11-30', '2022-12-30'], [OrderedDict([('GM', 0.0), ('LMT', 1.0), ('MSFT', 0.0), ('PG', 0.0), ('SPY', 0.0), ('WMT', 0.0)]), OrderedDict([('GM', 0.0), ('LMT', 1.00001), ('MSFT', 0.0), ('PG', 0.0), ('SPY', 0.0), ('WMT', 0.0)]), OrderedDict([('GM', 0.0), ('LMT', 0.98558), ('MSFT', 0.0), ('PG', 0.0), ('SPY', 0.0), ('WMT', 0.01442)]), OrderedDict([('GM', 0.0), ('LMT', 1.0), ('MSFT', 0.0), ('PG', 0.0), ('SPY', 0.0), ('WMT', 0.0)])])
# file = open('weights_record.obj', 'wb')
# pickle.dump(weights_rec, file)
# file.close()

# read
file = open('weights_record.obj', 'rb')
weights = pickle.load(file)
file.close()