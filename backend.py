import pandas as pd
import numpy as np
import os
import xlsxwriter 

def run_all(test1,test2,master_path,val_CLIENT_NAME,val_FREQUENCY,val_WEEKLY):
    output_info_string = ""
    # inputs
    # test1 = r"C:\Users\khsh2008\Desktop\MY FOLDER\otherteamProjects\sourab\mergeAndWriteInSeparateSheet\TEST FILES\Test 1"
    # test2 = r"C:\Users\khsh2008\Desktop\MY FOLDER\otherteamProjects\sourab\mergeAndWriteInSeparateSheet\TEST FILES\Test 2"
    # # master_path to write excel file
    # master_path = r"C:\Users\khsh2008\Desktop\MY FOLDER\otherteamProjects\sourab\mergeAndWriteInSeparateSheet"
    # val_CLIENT_NAME	= "test_client_name"	
    # val_FREQUENCY = "test_frequency"				
    # val_WEEKLY = "test_weekly"
    # ===========================================
    #---------PRE DECLARATION-------------
    dict_sheet_nam_avg = {}
    # creating a second dataframe 
    lst_entities = []
    lst_average = []
    lst_comments_main = []
    lst_sheet_links = []
    #============================================
    #--------------------------------------------
    # --------------- FUNCTIONS -----------------
    def remove_substrings(string, substrings):
        for substring in substrings:
            string = string.replace(substring, "")
        return string
    
    def adding_list_as_last_row(df, list_obs):
        # list_obs = [1, 2, 3, 4]  # Replace with the actual values for the new row
        new_row = pd.DataFrame([list_obs], columns=df.columns)
        df = df.append(new_row, ignore_index=True)
        return df
    
    def take_sum_and_avg_for_desired_col(df):
        lst = []
        for i in df.columns:
            if i == "DIFF":
                lst.append(np.sum(df[i]))
                print(lst)
            elif i == "PERCENTAGE":
                lst.append(np.mean(df[i]))
                print(lst)
            else:
                lst.append(np.nan)
        return lst
    #============================================
    #--------------------------------------------
    
    list_of_file_1 = os.listdir(test1)
    list_of_file_2 = os.listdir(test2)
    lst_all_data_sheet = []
    
    #--------------------------------------------
    # Create an Excel writer using openpyxl
    os.chdir(master_path)
    writer = pd.ExcelWriter('Output_merging.xlsx', engine='xlsxwriter')
    #--------------------------------------------
    
    
    #--------------------------------------------
    # To make summary sheet to be at first
    df_empty = pd.DataFrame()
    df_empty.to_excel(writer, sheet_name="RMC", index=False)
    #--------------------------------------------
    
    
    
    
    if list_of_file_1 == list_of_file_2:
        print("Files names are same")
        output_info_string = output_info_string + "Files names are same"
    else:
        print("Files names are not same")
        output_info_string = output_info_string + "Files names are not same"
        
    global lst_mac_sheet_name
    lst_mac_sheet_name = []
    for file1 in list_of_file_1:
        try:
            df1 = pd.read_csv(r""+test1+"\\"+file1)
            df2 = pd.read_csv(r""+test2+"\\"+file1)
            sheet_nam = remove_substrings(file1, ["-", ".XLSX"])[:31]
            sheet_nam = remove_substrings(file1, ["-", ".xlsx"])[:31]
            print(file1,"csv")
        except:
            df1 = pd.read_excel(r""+test1+"\\"+file1)
            df2 = pd.read_excel(r""+test2+"\\"+file1)
            sheet_nam = remove_substrings(file1, ["-", ".CSV"])[:31]
            sheet_nam = remove_substrings(file1, ["-", ".csv"])[:31]
            print(file1,"excel")
        try:
            if "VALUE_ID" in list(df1.columns):
                df_merge = pd.merge(df1,df2,on = "VALUE_ID",how = "outer")
                print(file1," merging done!---------for VALUE_ID")
            elif "MODULE_CODE" in list(df1.columns):
                df_merge = pd.merge(df1,df2,on = "MODULE_CODE",how = "outer")
                print(file1," merging done!---------for MODULE_CODE")
    
            elif "CHAR ID" in list(df1.columns):
                df_merge = pd.merge(df1,df2,on = "CHAR ID",how = "outer")
                print(file1," merging done!---------for CHAR_ID")
            elif "HIERARCHY" in list(df1.columns):
                df_merge = pd.merge(df1,df2,on = "CHAR_ID",how = "outer")
                print(file1," merging done!---------for CHAR_ID for Hierarchy")
    
        except:
            print("-----------",file1,"sorry merging is not happening!!!--------")
        
        # Write each dataframe to a separate sheet
        # Assuming you have a DataFrame called 'df'
        # df_merge.dropna(axis=1, inplace=True)
        # Check which columns have all empty values
        empty_columns = df_merge.columns[df_merge.isnull().all()]
        
        # Drop the empty columns
        df_merge.drop(empty_columns, axis=1, inplace=True)
        try:
            df_merge.drop(["RUN_ID_y","MAC_CODE_y","STATUS_y"], axis=1, inplace=True)
        except:
            print("'RUN_ID_y', 'MAC_CODE_y', 'STATUS_y' not found in axis")
        #----calculation part
        if "ITEMS_x" in list(df_merge.columns):
            df_merge["DIFF"] = df_merge["ITEMS_x"] - df_merge["ITEMS_y"]
            df_merge["PERCENTAGE"] = round((df_merge["DIFF"]/df_merge["ITEMS_x"])*100,2)
        elif "ITEM_COUNT_x" in list(df_merge.columns):
            df_merge["DIFF"] = df_merge["ITEM_COUNT_x"] - df_merge["ITEM_COUNT_y"]
            df_merge["PERCENTAGE"] = round((df_merge["DIFF"]/df_merge["ITEM_COUNT_x"])*100,2)
        else:
            pass
        #------calculating the comments--------
        lst_comments = []
        for i in range(len(df_merge)):
            if "ITL_SHORT_DESCRIPTION_x" in list(df_merge.columns):
                if df_merge["ITL_SHORT_DESCRIPTION_x"][i] == df_merge["ITL_SHORT_DESCRIPTION_y"][i]:
                    lst_comments.append("OK")
                else:
                    lst_comments.append("Mismatch Found")
            
            elif "MODULE_y" in list(df_merge.columns):
                if df_merge["MODULE_x"][i] == df_merge["MODULE_y"][i]:
                    lst_comments.append("OK")
                else:
                    lst_comments.append("Mismatch Found")
                    
            elif "CHAR DESCRIPTION_x" in list(df_merge.columns):
                if df_merge["CHAR DESCRIPTION_x"][i] == df_merge["CHAR DESCRIPTION_y"][i]:
                    lst_comments.append("OK")
                else:
                    lst_comments.append("Mismatch Found")
            
            elif "CHARACTERISTIC_x" in list(df_merge.columns):
                if df_merge["CHARACTERISTIC_x"][i] == df_merge["CHARACTERISTIC_y"][i]:
                    lst_comments.append("OK")
                else:
                    lst_comments.append("Mismatch Found")
                            
        try:
            df_merge["Comments"] = lst_comments
        except:
            print("-----Comments not required for Hierarchy and Soft Chars-----\n")
        
        ##--------------------------------------------
        # deleting unnecessary columns in the sheets
        # for Hierarchy - unique col name is CHAR_ID - del POS_CODE_y	PHI_CODE_y
        if "CHAR_ID" in list(df1.columns):
            df_merge.drop(["POS_CODE_y","PHI_CODE_y"], axis=1, inplace=True)
            print("\n del POS_CODE_y	PHI_CODE_y \n for hierarchy sheet")
        # for soft chars - unique col name is CHAR ID - FDS DESCRIPTION_y	CHAR TYPE (M/P)_y
        if "CHAR ID" in list(df1.columns):
            df_merge.drop(["FDS DESCRIPTION_y","CHAR TYPE (M/P)_y"], axis =1, inplace = True)
            print("\n del POS_CODE_y	PHI_CODE_y \n for softchar sheet")
        #--------------------------------------------
        #----- take the mac code sheet alone -----
        for val_col_name in df_merge.columns:
            if "VALUE_ID" in str(val_col_name):
                print("^^^^^^^^^")
                print(val_col_name)
                lst_mac_sheet_name.append(sheet_nam)
                print(lst_mac_sheet_name)
                print(sheet_nam)
                print("^^^^^^^^^")
        #--------------------------------------------
        # ----- sum for diff and avg for percentage ----
        lst_sum_avg = take_sum_and_avg_for_desired_col(df_merge)
        print(lst_sum_avg,"------------\n\n")
        df_merge = adding_list_as_last_row(df_merge,lst_sum_avg)
        df_merge.to_excel(writer, sheet_name=sheet_nam, index=False)
        #---------------------------------
        # adding key value pair for summary tab
        lst_entities.append(sheet_nam)
        try:
            lst_average.append(np.mean(df_merge["PERCENTAGE"]))
            if (np.mean(df_merge["PERCENTAGE"]) > 9.999) or (np.mean(df_merge["PERCENTAGE"]) < -9.999):
                lst_comments_main.append("ERROR")
            else:
                lst_comments_main.append("OK")
        except:
            lst_average.append(np.nan)
            lst_comments_main.append("")
        lst_sheet_links.append('internal:'+str(sheet_nam)+'!A1')
        #---------------------------------
        lst_all_data_sheet.append(df_merge)
        # taking the mapping char sheets
    #===========================================
    #-------------------------------------------
    # ------- SUMMARY TAB --------
    
    # add title to the excel sheet
    workbook  = writer.book
    worksheet = writer.sheets["RMC"]
    worksheet.write(0, 0, 'RETAILERS MAINTENANCE CHART', workbook.add_format({'bold': True, 'color': '#E26B0A', 'size': 20}))
    #-------------------------------------------
    # add main information
    # CLIENT NAME			
    # FREQUENCY						
    # WEEKLY			
    worksheet.write(3, 0, 'CLIENT NAME', workbook.add_format({'bold': True, 'color': '#004d1a', 'size': 14}))
    worksheet.write(4, 0, 'FREQUENCY', workbook.add_format({'bold': True, 'color': '#004d1a', 'size': 14}))
    worksheet.write(5, 0, 'WEEKLY', workbook.add_format({'bold': True, 'color': '#004d1a', 'size': 14}))
    
    #-------------------------------------------
    # merging cells
    merge_format = workbook.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "fg_color": "#33ff77",
        }
    )
    worksheet.merge_range('B4:D4',val_CLIENT_NAME, merge_format)	
    worksheet.merge_range('B5:D5',val_FREQUENCY, merge_format)	
    worksheet.merge_range('B6:D6',val_WEEKLY, merge_format)	
    #-------------------------------------------
    
    # creating a second dataframe 
    
    df_second_df = pd.DataFrame({"ENTITIES": lst_entities,
                                 "AVERAGE %":lst_average,   
                                 "COMMENTS":lst_comments_main,
                                 "LINKS":lst_sheet_links})
    df_second_df.to_excel(writer, sheet_name="RMC", startrow = 9, index=False)
    #-------------------------------------------
    # set col width
    worksheet.set_column(0, 3, 20)
    #-------------------------------------------
    # add borders
    border_format=workbook.add_format({
                                'border':1
                               })
    worksheet.conditional_format( 'A4:D6' , { 'type' : 'no_blanks' , 'format' : border_format} )
    #==========================================
    #-------------------------------------------
    print(lst_mac_sheet_name)
    x = lst_mac_sheet_name
    # Save the Excel file
    writer.save()
    print("successfully saved")

    #--------------
    
    
    
    
