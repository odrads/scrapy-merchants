import pandas as pd

columns = ['website','name','phone','address','hours_operation','email']
stores = ['taylormade','titleist','srixon','odyssey','callaway','cleveland','cobra']
stores = ['salomon']
for store in stores:
    csvfile = '%s_items.csv' % store
    raw_data = pd.read_csv(csvfile, names=columns, low_memory=False)
    clean_data = raw_data.drop_duplicates()
    cols = clean_data.columns.tolist()

    cols = [cols[1]] + [cols[3]]+ [cols[0]] + [cols[2]]  + [cols[5]] + [cols[4]]
    clean_data = clean_data[cols]
    clean_data.to_csv('clean/%s' % (csvfile), index=False)
