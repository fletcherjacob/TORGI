import sqlite3
import csv
import os
import pandas as pd
import time

def individual_output():
    con = sqlite3.connect(":memory:")
    import_path = ''  ###Import Directory Path
    descrip = ''  ### FileId Category Identifier
    print(import_path)
    x = 0   ####FileId starting number

    for filename in os.listdir(import_path):
        try:

            # Save the full name if ext matches

            if filename.endswith(".gpkg"):
                x = x + 1
                sqlite_file = import_path + filename
                conn = sqlite3.connect(sqlite_file)   #SQLITE connection
                cur = conn.cursor()
                data = cur.execute("SELECT svid, constellation, cn0, agc, local_time FROM sat_data;"  )  ### SQL selection statement
                export_csv = descrip +str(x) + '.csv' #Sets new csv file to variable for writing
                with open(export_csv, 'w') as csvf:
                    writer = csv.writer(csvf)
                    writer.writerow( [ 'svid', 'constellation', 'cn0', 'agc', 'local_time','Attack'])  ### Creats header row for CSV file
                    writer.writerows(data)
                    conn.close()

            output_df = pd.read_csv(export_csv)
            ### Fills in Columns with Static data  to Columns added that were provided via the SQL statement
           
            """Determine Attack via given milisecond epoch time"""
            output_df['Attack'] = (output_df['local_time'] >  1538602800000 & (output_df['local_time'] <  1538604360000))\ 
                                 | (
                        output_df['local_time'] > 1538609760000  & (output_df['local_time'] < 1538610600000))\
                                  | (
                        output_df['local_time'] > 1538617200000 & (output_df['local_time'] <  1538618520000))\
                                  | (
                        output_df['local_time'] > 1538618700000 & (output_df['local_time'] < 1538618940000))\
                                  | (
                        output_df['local_time'] > 1538619420000 & (output_df['local_time'] < 1538620980000))\
                                  | (
                        output_df['local_time'] > 1538621040000 & (output_df['local_time'] < 1538621940000))\
                                  | (
                        output_df['local_time'] > 1538622060000 & (output_df['local_time'] < 1538623740000))\
                                  | (
                        output_df['local_time'] > 1538624040000 & (output_df['local_time'] < 1538710440000))\
                                  | (
                        output_df['local_time'] > 153621040000 & (output_df['local_time'] < 1538621940000))\
                                  | (
                        output_df['local_time'] > 1538622060000 & (output_df['local_time'] < 1538623740000))\
                                  | (
                        output_df['local_time'] > 1538624040000 & (output_df['local_time'] < 1538710440000))\
                                  | (
                        output_df['local_time'] > 1538702220000 & (output_df['local_time'] < 1538704080000))\
                                  | (
                        output_df['local_time'] > 1538704080000 & (output_df['local_time'] < 1538705280000))\
                                  | (
                        output_df['local_time'] > 1538705460000 & (output_df['local_time'] < 1538706600000))\
                                  | (
                        output_df['local_time'] > 1538706660000 & (output_df['local_time'] < 1538707380000))\
                                  | (
                        output_df['local_time'] > 1538707500000 & (output_df['local_time'] < 1538708220000))\
                                  | (
                        output_df['local_time'] > 1538708340000 & (output_df['local_time'] < 1538698620000))

            update_data = output_df.fillna({'Attack': False})

            update_data.to_csv(export_csv)
            print(export_csv)

        except sqlite3.Error:
            print(filename + " is empty")


def combine():
    # Creates combined file CSV and assigns headers for columns
    allOutput = "allOutput.csv"
    with open(allOutput, 'w') as csvfile:
        fileWriter = csv.writer(csvfile)
        fileWriter.writerow(
            [ 'svid', 'constellation', 'cn0', 'agc', 'local_time','Attack'])

    csv_path = '' #output path of Individual CSV
    original = pd.read_csv(csv_path + 'allOutput.csv')
    for f in os.listdir(csv_path):

        if f.endswith(".csv"):
            print(f)
            try:
                pd.set_option('display.max_columns', None)

                original2 = pd.read_csv(f)
                # print('Original', original)
                # print('Original2', original2)

                original = original.append(original2, ignore_index=True)

            except IOError:
                print(IOError)

    # combined_csv = pd.concat([original, original2], sort=True)
    original.to_csv("combined.csv", index=False)
    # print('Combined', original)


def confirm():
    test_file = 'combined.csv' #location of outputed csv from combine()
    df = pd.read_csv(test_file)
    print(df.head(n=5))
    ### Fills in Columns with Static data  to Columns added that were provided via the SQL statement
    is_attack = (df['Attack'] == True)
    print(is_attack.value_counts()) #Shows Count of T & F , allows individual to know maximum size of sample possible

def sample():
    # making data frame from csv file
    data1 = pd.read_csv('combined.csv')#location of outputed csv from combine()
    data = data1.fillna({'Attack': False, 'CONUS': 0 })  #Fill in empty False 
    print(data.head(5))
    
    attack_data = data[(data['Attack'] == True)]

    print(data.head(5))
    nonattack_data = data[(data['Attack'] == False)]
    print(nonattack_data.head(5))

    attack_sample = attack_data.sample(50000) # sample sizing
    nonattack_sample = nonattack_data.sample(50000)
    combine_sample = pd.concat([attack_sample, nonattack_sample])

    ld = (len(data))
    lad = (len(attack_sample))
    lnad = (len(nonattack_sample))
    print(ld)
    print(lad)
    print(lnad)
    print(lad + lnad)



    combine_sample.to_csv("sample_100k_50tf_v1.csv", index=False) #Naming Format, 100k = 100 Samples, 50tf = 50% tf, v1 = version
    test = pd.read_csv("sample_100k_50tf_v1.csv")
    if len(test) == 100000: #Test sample size
        print("Success")
    else:
        print("Fail")

def main():
    individual_output()
    combine()
    confirm()
    sample()

main()
