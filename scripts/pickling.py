import pickle
from collections import OrderedDict

# write 
# weights_rec_msr = (['2022-09-30', '2022-10-31', '2022-11-30', '2022-12-30'], [OrderedDict([('GM', 0.0), ('LMT', 1.0), ('MSFT', 0.0), ('PG', 0.0), ('SPY', 0.0), ('WMT', 0.0)]), OrderedDict([('GM', 0.0), ('LMT', 1.00001), ('MSFT', 0.0), ('PG', 0.0), ('SPY', 0.0), ('WMT', 0.0)]), OrderedDict([('GM', 0.0), ('LMT', 0.98558), ('MSFT', 0.0), ('PG', 0.0), ('SPY', 0.0), ('WMT', 0.01442)]), OrderedDict([('GM', 0.0), ('LMT', 1.0), ('MSFT', 0.0), ('PG', 0.0), ('SPY', 0.0), ('WMT', 0.0)])])
# weights_rec_mv = (['2022-09-30', '2022-10-31', '2022-11-30', '2022-12-30'], [OrderedDict([('GM', 0.0), ('LMT', 0.26473), ('MSFT', 0.0), ('PG', 0.28873), ('SPY', 0.27833), ('WMT', 0.16822)]), OrderedDict([('GM', 0.0), ('LMT', 0.2688), ('MSFT', 0.0), ('PG', 0.29738), ('SPY', 0.24964), ('WMT', 0.18419)]), OrderedDict([('GM', 0.0), ('LMT', 0.27888), ('MSFT', 0.0), ('PG', 0.31563), ('SPY', 0.22072), ('WMT', 0.18477)]), OrderedDict([('GM', 0.0), ('LMT', 0.27407), ('MSFT', 0.0), ('PG', 0.33766), ('SPY', 0.20366), ('WMT', 0.1846)])])
weights_rec_hrp = (['2022-09-30', '2022-10-31', '2022-11-30', '2022-12-30'], [OrderedDict([('GM', 0.20463), ('LMT', 0.02343), ('MSFT', 0.0133), ('PG', 0.43396), ('SPY', 0.0121), ('WMT', 0.31257)]), OrderedDict([('GM', 0.24118), ('LMT', 0.02878), ('MSFT', 0.01248), ('PG', 0.35082), ('SPY', 0.01145), ('WMT', 0.35529)]), OrderedDict([('GM', 0.32382), ('LMT', 0.02827), ('MSFT', 0.01358), ('PG', 0.31235), ('SPY', 0.01244), ('WMT', 0.30952)]), OrderedDict([('GM', 0.44564), ('LMT', 0.02732), ('MSFT', 0.01755), ('PG', 0.26513), ('SPY', 0.01469), ('WMT', 0.22968)])])

file = open('hrp_weights_record.obj', 'wb')
pickle.dump(weights_rec_hrp, file)
file.close()

# read
# file = open('weights_record.obj', 'rb')
# weights_rec = pickle.load(file)
# file.close()


