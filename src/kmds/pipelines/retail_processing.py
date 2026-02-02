from prefect import flow, task
import pandas as pd



@task(log_prints=True)
def load_data_file(dataset_df:pd.DataFrame):
    print(f"Loaded dataset")
    return dataset_df

@task(log_prints=True)
def apply_noise_filter_1(dataset_df:pd.DataFrame):
    valid_cust = ~dataset_df["Customer ID"].isna()
    valid_desc = ~dataset_df["Description"].isna()
    valid_stock_code = ~dataset_df["Description"].isna()
    noise_filter_1 = valid_cust & valid_desc
    dataset_df = dataset_df[noise_filter_1].reset_index(drop=True)
    return dataset_df

def good_quantity_record_check(x):
    try:
        f_x = float(x)
        if f_x > 0:
            return True
        else:
            return False # returned purchase
    except :
        return False

@task(log_prints=True)
def apply_noise_filter_2(dataset_df: pd.DataFrame):
    good_quantity_records = dataset_df["Quantity"].apply(good_quantity_record_check)
    dataset_df = dataset_df[good_quantity_records]
    dataset_df = dataset_df.reset_index(drop=True)
    return dataset_df

@task(log_prints=True)
def apply_noise_filter_3(dataset_df: pd.DataFrame):
    return_or_bank_charges = (dataset_df.Price == "BANK CHARGES") | (dataset_df.Price == "ADJUST")
    valid_purchases = ~ return_or_bank_charges
    dataset_df = dataset_df[valid_purchases]
    dataset_df = dataset_df.reset_index(drop=True)
    return dataset_df

def not_test_product(x):
    if "TEST" in x:
        return False
    elif x in ["ADJUST", "BANK CHARGES", "C2", "M"]:
        return False
    else:
        return True

@task(log_prints=True)
def apply_noise_filter_4(dataset_df: pd.DataFrame):
    valid_products = dataset_df["StockCode"].apply(not_test_product)
    dataset_df = dataset_df[valid_products]
    dataset_df = dataset_df.reset_index(drop=True)
    return dataset_df

@task(log_prints=True)
def transform_1(dataset_df: pd.DataFrame):
    attr_types = {"Invoice": str, "StockCode": str, "Description": str,\
             "Quantity": float, "InvoiceDate": 'datetime64[ns]', "Price": float,\
             "Customer ID": str, "Country": str}
    dataset_df = dataset_df.astype(attr_types)
    Q1_2010 = (dataset_df["InvoiceDate"].dt.year == 2010) & (dataset_df["InvoiceDate"].dt.quarter == 1)
    dataset_df = dataset_df[Q1_2010]
    dataset_df = dataset_df.reset_index(drop=True)
    return dataset_df

@task(log_prints=True)
def transform_2(dataset_df: pd.DataFrame):
    dataset_df["item_total"] = dataset_df["Quantity"] * dataset_df["Price"]
    dsbysc = dataset_df.groupby([dataset_df.InvoiceDate.dt.day_of_year, dataset_df.StockCode])
    dsbysc = dsbysc["item_total"].sum().to_frame().reset_index()
    dfQ1_PA = dsbysc.pivot(index="InvoiceDate", columns="StockCode", values="item_total").fillna(0)
    
    return dfQ1_PA


@flow(name="retail_pipleline")
def retail_pipeline():
    DATA_DIR = "../../data"
    fp1 = DATA_DIR + "/" + "online_retail_II.csv"
    fp2 = DATA_DIR + "/" + "retail_q1_sales_2010_summary.csv"
    plist = [load_data_file, apply_noise_filter_1,\
             apply_noise_filter_2, apply_noise_filter_3,\
             apply_noise_filter_4]
    df = pd.read_csv(fp1)
    print("Running processing steps...")
    for f in plist:
        df = f(df)
    tlist = [transform_1, transform_2]
    print("Running transform steps...")
    for f in tlist:
        df = f(df)
    print("Done data prep!. Writing results to disk...")
    df.to_csv(fp2, index=False)

    return
    


# run the flow!
if __name__=="__main__":
    retail_pipeline()