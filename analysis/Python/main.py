import sqlite3
import csv
import os
import pandas as pd


def individual_output():
    con = sqlite3.connect(":memory:")
    import_path = '/home/fletcher/dev/0_Torgi/data/'  ###Import Directory Path
    descrip = 'EMI-'  ### FileId Category Identifier
    print(import_path)
    x = 0   ####FileId starting number

    for filename in os.listdir(import_path):
        try:

            # Save the full name if ext matches

            if filename.endswith(".gpkg"):
                x = x + 1
                sqlite_file = import_path + filename
                conn = sqlite3.connect(sqlite_file)
                cur = conn.cursor()
                data = cur.execute(
                    "SELECT id, svid, constellation, cn0, agc, azimuth_deg,elevation_deg,FROM sat_Data;"  )  ### SQL selection statement
                ##local_time = cur.execute("SELECT local_time FROM sat_Data")
                export_csv = descrip +str(x) + '.csv'
                with open(export_csv, 'w') as csvf:
                    writer = csv.writer(csvf)
                    writer.writerow(['id', 'svid', 'constellation', 'cn0', 'agc', 'azimuth_deg', 'elevation_deg', 'fileName', 'CONUS', 'fileId'])  ### Creats header row for CSV file
                    writer.writerows(data)
                    conn.close()

            output_df = pd.read_csv(export_csv)
            ### Fills in Columns with Static data  to Columns added that were provided via the SQL statement
            output_df['CONUS'] = '0'  ### Working to add automatic detection for future use
            output_df['fileId'] = export_csv
            output_df['fileName'] = filename

            output_df.to_csv(export_csv)
            print(export_csv)

        except sqlite3.Error:
            print(filename + " is empty")


def combine():
    # Creates combined file CSV and assigns headers for columns
    allOutput = "allOutput.csv"
    with open(allOutput, 'w') as csvfile:
        fileWriter = csv.writer(csvfile)
        fileWriter.writerow(
            ['id', 'svid', 'constellation', 'cn0', 'agc', 'azimuth_deg', 'elevation_deg', "fileName", "CONUS",
             "fileId"])

    csv_path = '/home/fletcher/dev/0_Torgi/2_Python/'
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
    original.to_csv("combined_csv.csv", index=False)
    # print('Combined', original)


def main():
    individual_output()
    # all_output()
    combine()


main()
