class Mess:
    """Class that contains specific methods for the temperature measurements"""

    def __init__(self,df):
        self.df = df
    
    def process1(self):
        # Initial formating of the file
        import pandas as pd
        import numpy as np

        # Starts dataframe from index 4 (deletes first lines)
        self.df.drop(self.df.index[:4], inplace = True)

        # Dataframe to list
        li = self.df.values.tolist()

        # Refacere df dupa primul el din list (prima linie cap coloane)
        self.df = pd.DataFrame(li,columns=li[0])

        # Eliminates again the first line
        self.df.drop(self.df.index[:1], inplace=True)

        # Replaces empty values with 0 (by numpy)
        self.df = self.df.replace(np.nan,0)


    def process2(self,last_point):
        # Loop that replaces >70 values or "-" with (column+1)+0.9
        # n=2 start value, in the table the values start from the 2th column
        # On the values from the last column, it will replace them with values from first column +0.9
        # We use iloc for nonString(int) and loc for string(ex:"-")

        n = 2
        while True:      
            if n == last_point:

                self.df.loc[self.df.iloc[:,n] == "-",self.df.columns[n]] = self.df.iloc[:,2] + 0.9

                for x in range(1, len(self.df.iloc[:,n]) - 1):

                    if self.df.iloc[:,n][x] > 70:

                        self.df.replace(self.df.iloc[:,n][x],self.df.iloc[:,2][x] + 0.9, inplace=True)
                break

            else:
                self.df.loc[self.df.iloc[:,n] == "-" ,self.df.columns[n]] = self.df.iloc[:,n+1] + 0.9

                for x in range(1, len(self.df.iloc[:,n]) - 1):

                    if self.df.iloc[:,n][x] > 70:

                        self.df.replace(self.df.iloc[:,n][x],self.df.iloc[:,n+1][x] + 0.9,inplace=True)
                n += 1
                continue

    # For status signalinng
    alarm = 0 # Status:0=ok,1=values >70

    # I' ve used a static method in order to create a function inside the class. This function will take data from the
    # big_table, will process data and return another dataframe, which we will use to create the small_table
    #  containing the maximum values

    @staticmethod
    def procesare3(df,nr_mes,nr_points,last_point):
        import pandas as pd
        # Define the non 0 values from the first column (for measurements limmiting)
        intervals = []
        i = 0

        while True:
            if len(intervals) > nr_mes:
                break
            if df.iloc[i,0] != 0:
                intervals.append(i)
            i += 1
            continue
            
        # List that contains the upper limits
        upper_limit = []
        for x in intervals[:len(intervals) - 1]:
            upper_limit.append(x)

        # List that contains the lower limits
        lower_limit = []
        for x in intervals[1:]:
            lower_limit.append(x)

        # Combines upper_limit and lower_limit in real intervals. Idex that we use in order to take the maximum values
        real_limit = []
        for x in range(0,nr_mes):
            real_limit.append([upper_limit[x],lower_limit[x]])

        # Maximums table
        # Inserts in list the maximum value in the real_limit
        # Caution! the maximum values must be rearranged on lines in order to display them. Group to nested
        li = []
        n1 = 2
        while True:
            if n1 > last_point:
                break
            for x in range(0,len(real_limit)):
                li.append(max(df.iloc[real_limit[x][0]:real_limit[x][1],n1]))
            n1 += 1
            continue
        
        # Checks if in the list we still have values > 70, then sets the alarm to 1
        for x in li:
            if x > 70:
                Mess.alarm = 1

        # Example on how the values must be rearranged on lines (for 3 measurements x 3 points and for 4 x 4)
        # 0 3 6     0 4 8  12
        # 1 4 7     1 5 9  13
        # 2 5 8     2 6 10 14
        #           3 7 11 15

        # Define template positions to use for the desired arrangement (above example)
        li1 = []
        for x in range(nr_mes):
            li1.append([x])

        n2 = 0
        while True:
            if n2 > nr_points - 2:
                break
            for x in li1:
                x.append(x[n2] + nr_mes)    
            n2 += 1                         
            continue                      

        # Adding values to list by using the created template (li1)
        li2 = []    
        for x in li1:
            for x1 in x:
                li2.append(li[x1])

        # Nested list grouped by lines (after li2)
        n3 = 0
        li3 = []
        while n3 < len(li2):
            li3.append(li2[n3:n3 + nr_points])
            n3 += nr_points

        # Fromatting the small_table or the maximums table: number of measurement and date for each "line"

        # Number
        for x in range(0,len(li3)):
            li3[x].insert(0, x + 1)

        # Date
        for x in li3:
            x.insert(1,str(df.iloc[0,0])[:10])

        # Dedining the small_table_head
        small_table_head = ["Messung","Datum"]

        # Adding measurement points to the small table / maximums table
        for x in range(0,nr_points): 
            small_table_head.append("M" + str(x))


        # Making another dataframe after li3 and small_table_head
        # This dataframe will be used to create another object (small_table) on which the maximum values will stay
        df1=pd.DataFrame(li3,columns = small_table_head)
        return df1
