import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

dataset = [["사과", "치즈", "생수"],
           ["생수", "호두", "치즈", "고등어"],
           ["수박", "사과", "생수"],
           ["생수", "호두", "치즈", "옥수수"]]

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
df_apr = apriori(df, use_colnames=True)
print(df_apr)
