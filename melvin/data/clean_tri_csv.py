#importing utility modules
import os, sys
import pandas as pd
#LIVIN' ON THE EDGE
import warnings
warnings.filterwarnings("ignore")

# Function to capture/rename the attributes listed above from TRI dataframe
# Some input validataion could be done here... but we're all going to agree to only use valid inputs!!
def trim_tri_df(tri_df):
    # list of the categories we want from each tri data set
    desired_categories = [
        'YEAR','FACILITY_NAME','FEDERAL_FACILITY','PARENT_COMPANY_NAME',       \
        'INDUSTRY_SECTOR','ZIP','ST', 'CITY', 'COUNTY', 'LATITUDE',            \
        'LONGITUDE', 'CHEMICAL', 'UNIT_OF_MEASURE', 'CARCINOGEN',              \
        'CLEAR_AIR_ACT_CHEMICAL','TOTAL_RELEASES','ON-SITE_RELEASE_TOTAL',     \
        'OFF-SITE_RELEASE_TOTAL', 'OFF-SITE_RECYCLED_TOTAL',                   \
        '8.4_RECYCLING_ON-SITE', '8.8_ONE-TIME_RELEASE']

    tri_df = tri_df[desired_categories]

    #rename categories as described above
    tri_df.rename(columns = {                                                  \
        'ST':'STATE',                                                          \
        'CLEAR_AIR_ACT_CHEMICAL':'CAA_CHEMICAL',                               \
        'ON-SITE_RELEASE_TOTAL':'ON_SITE_RELEASE_TOTAL',                       \
        'OFF-SITE_RELEASE_TOTAL':'OFF_SITE_RELEASE_TOTAL',                     \
        '8.4_RECYCLING_ON-SITE':'ON_SITE_RECYCLED_TOTAL',                      \
        'OFF-SITE_RECYCLED_TOTAL':'OFF_SITE_RECYCLED_TOTAL',                   \
        '8.8_ONE-TIME_RELEASE':'ONE_TIME_RELEASES'}, inplace=True)

    #return trimmed tri
    return tri_df

# Function to handle missing values in our trimmed TRI data fram
# Some input validataion could also be done here... but this will be chained with the previous trim_tri_df() function
# in the source for the actual utility program... so again we'll just agree to not give bad inputs to this function!
# The output and input to this function is very specific to this particular data set and project, of course.
def handle_nan_tri_df(tri_df):
    # Filling NaN categories for attributes that may need to be summed across
    fill_zero_categories = [
        'TOTAL_RELEASES','ON_SITE_RELEASE_TOTAL','OFF_SITE_RELEASE_TOTAL',     \
        'ON_SITE_RECYCLED_TOTAL','OFF_SITE_RECYCLED_TOTAL','ONE_TIME_RELEASES']

    for i in range(len(fill_zero_categories)):
        tri_df[fill_zero_categories[i]].fillna(0,inplace=True)

    #return now-cleaned (after running through trim_tri_df) data frame
    return tri_df

# Function to write the DataFrame to csv. For the purposes of this project, we will call the folder clean_TRI_Data/
# and the files will be in the format 'TRI_<YEAR>_US_CLEAN.csv'
# define out dir to be made -- change this if you want files written to a different directory
directory = './clean_TRI_Data'
def write_cleaned_tri_to_csv(tri_df, tri_type, directory):
    #create target directory if it doesn't already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not tri_type == 'US':
        #check for state sub-folder, create if none
        if not os.path.exists('%s/State_TRI/'%directory):
            os.makedirs('%s/State_TRI/'%directory)
        tri_df.to_csv('%s/State_TRI/%s'%(directory,'TRI_%s_%s_CLEAN.csv'%(tri_df.YEAR[0], tri_type)))
    else:
        #check for US sub-folder, create if none
        if not os.path.exists('%s/US_TRI/'%directory):
            os.makedirs('%s/US_TRI/'%directory)
        tri_df.to_csv('%s/US_TRI/%s'%(directory,'TRI_%s_US_CLEAN.csv'%(tri_df.YEAR[0])))

if len(sys.argv) == 2:
    print """
        This script is particularly for TRI US and State data sets. Read documentation at
        https://github.com/UNCG-CSE/Toxic-Crusaders/blob/master/jacob/Cleaning_TRI_Data.ipynb for example.

        Cleaning CSV File...
    """

    tri_type = str(sys.argv[1].split('/')[-1].split('_')[-1].split('.')[0])

    if not tri_type == 'US':
        print 'State TRI data file imported...\n'
    else:
        print 'US TRI data file imported...\n'

    #read in csv file
    initial_df = pd.read_csv(sys.argv[1])

    print 'Trimming and renaming columns\n'
    #trim and rename columns
    trimmed_df = trim_tri_df(initial_df)

    print 'Converting NaN values in numerical columns to zeroes\n'
    #fill NaN values in appropriate categories
    clean_df = handle_nan_tri_df(trimmed_df)

    print 'Writing cleaned DataFrame to %s/TRI_%s_%s_CLEAN.csv\n'%(directory,clean_df.YEAR[0],tri_type)
    #write cleaned TRI DataFrame to csv and store in local folder - create if it doesn't exist yet
    write_cleaned_tri_to_csv(clean_df, tri_type, directory)

    #it probably works!
    print 'TRI CSV File cleaned and placed in ./clean_TRI_Data/TRI_%s_%s_CLEAN.csv\n'%(clean_df.YEAR[0],tri_type)

else:
    print """
        Provide a single TRI data file for cleaning.

        This script is particularly for TRI US and State data sets. Read documentation at
        https://github.com/UNCG-CSE/Toxic-Crusaders/blob/master/jacob/Cleaning_TRI_Data.ipynb for example.
    """
