#importing utility modules
import os, sys
import pandas as pd
#LIVIN' ON THE EDGE
import warnings
warnings.filterwarnings("ignore")

def trim_tri_df(tri_df):
    # list of the categories we want from each tri data set
    #primarily interested in INDUSTRY_SECTOR and TOTAL_RELEASES
    # will use STATE in part 3 to compare to US
    desired_categories = ['YEAR', 'INDUSTRY_SECTOR', 'TOTAL_RELEASES', 'RECYCLED_TOTAL']
    #filter for plastics and rubber production
    category = 'Plastics and Rubber'
    tri_df = tri_df[tri_df.INDUSTRY_SECTOR == category]
    tri_df['RECYCLED_TOTAL'] = tri_df.OFF_SITE_RECYCLED_TOTAL + tri_df.ON_SITE_RECYCLED_TOTAL
    tri_df = tri_df[desired_categories]
    #return trimmed tri
    return tri_df

directory = './A4_TRI_Data'
def write_cleaned_tri_to_csv(tri_df, tri_year, directory):
    #create target directory if it doesn't already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    tri_df.to_csv('%s/%s'%(directory,'A4_TRI_%s_US.csv'%(tri_year)))

if len(sys.argv) == 2:
    print """
        This script is particularly for TRI US data sets, CSC495 Assignment 4.

        Cleaning CSV File...
        """

    tri_year = str(sys.argv[1].split('/')[-1].split('_')[-3])

    print 'US TRI data file imported...\n'

    #read in csv file
    initial_df = pd.read_csv(sys.argv[1])

    print 'Trimming data\n'
    #trim and rename columns
    trimmed_df = trim_tri_df(initial_df)

    print 'Writing cleaned DataFrame to %s/A4_TRI_%s_US.csv\n'%(directory,tri_year)
    #write cleaned TRI DataFrame to csv and store in local folder - create if it doesn't exist yet
    write_cleaned_tri_to_csv(trimmed_df, tri_year, directory)

    #it probably works!
    print 'TRI CSV File cleaned and placed in ./A4_TRI_Data/A4_TRI_%s_US_CLEAN.csv\n'%(tri_year)

else:
    print """
        Provide a single TRI data file for cleaning.
    """
