import time
import sys
import pandas as pd
import numpy as np



chicago = 'chicago.csv' 
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'


   
def get_city():
  
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = input ("Please enter the name of the city you are interested in ('chicago, new york city, washington')")

    city = city.lower().strip()

# TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True: 
        if city == "new york city" or city == "newyorkcity":
            print('\nNew York City Data!\n')
            return new_york_city
        if  city == "chicago":
            print('\nChicago Data!\n')
            return chicago
        elif city == "washington":
            print('\nWashington Data!\n')
            return washington
        city = input ("Please enter the name of the city you are interested in as shown ('chicago, new york city, washington')")
        city = city.lower().strip()
       

    # TO DO: get user input for month (all, january, february, ... , june)
def get_time_period():
    
    time_period = input('\nWould you like to filter by month (m) and date, day of the week(wd), or not at all? Type "none" for no time filter.\n')

    time_period =  time_period.lower().strip()

    while True: 
        if time_period == 'month' or time_period == 'm':

            while True:
                dayfilter = input("\n Do you wish to filter by the date also? Type 'YES' or 'NO'\n").lower().strip()

                if dayfilter == "no":
                    print('\n We are now filtering data by month...\n')

                    return 'month'

                elif dayfilter == "yes":
                   print ('\n We are now filtering data by month and day of the month...\n')
                   return 'day_of_month'
                
        if time_period == "day" or time_period == 'wd' or time_period == 'day of the week': 
            print('\n We are now filtering data by day of the week...\n')
            return 'day_of_week'
        elif time_period == "none":
            print('\n We are not applying any time filter to the data\n')
            return "none"
        time_period = input("\n Please choose a time filter option between month(m), day of the week(wd), or none (n) \n")
        time_period = time_period.lower().strip()
def get_month(month2):
    if month2 == "month":
        month = input ("Enter a month between January and June ")
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may','june']:
            month = input ("Enter a month between January and June")
            month = month.strip().lower()
        return month
    else:
        return 'none'
      
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
def get_day_of_month(df, dayOfMonth2):
    
    monthAndDay = []
    
    if dayOfMonth2 == "day_of_month":
        
        month = get_month("month")
        monthAndDay.append(month)

        maxDayOfMonth = get_max_day_of_month(df, month)
        
        while (True):

            promptString = """\n Which day of the month? \n
            Please type your response as a number between 1 and   """
                            
            
            promptString  = promptString + str(maxDayOfMonth) + "\n" 

            dayOfMonth = input(promptString)

            try: 

                dayOfMonth = int(dayOfMonth)

                if 1 <= dayOfMonth <= maxDayOfMonth:
                    monthAndDay.append(dayOfMonth)
                    return monthAndDay

            except ValueError:

                print("Please enter input as a number in numeral form")
        
    else:
        return 'none'    
def get_day(day2):

    if day2 == 'day_of_week':
        day = input('\nEnter a day of the week. Please type a day as m, tu, w, th, f, sa,su. \n')
        while day.strip().lower() not in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']:
            day = input('\nEnter selection as shown here m, tu, w, th, f, sa, su,\n')
        return day.lower()
    else:
        return 'none'
    
def load_data(city):
    
    print('\nLoading...\n')
    df = pd.read_csv(city)
    
   
    df['Start Time'] = pd.to_datetime(df['Start Time'])

   
    
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['day_of_month'] = df['Start Time'].dt.day

    return df
def apply_time_filters(df, time_period, month, dayOfWeek, monthAndDay):
    
    
# this applies the time filters
    
    print('Loading... \n')
    if time_period == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

   
    if time_period == 'day_of_week':
        days = ['Monday', 'Tuesday', 
        'Wednesday', 'Thursday', 
        'Friday', 'Saturday', 'Sunday']
        for d in days:
            if dayOfWeek.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    if time_period == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = monthAndDay[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = monthAndDay[1]
        df = df[df['day_of_month'] == day]

    return df


def popular_month(df):
    """Displays statistics on the most frequent times of travel."""
    # TO DO: display the most common month
    print('\n * What is the most popular month for bike traveling?')
    mnth = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_popular_month = months[mnth - 1].capitalize()
    return most_popular_month

def popular_day(df):
    # TO DO: display the most common day of week
    print('\n * What is the most popular day of the week for bike traveling?')
    
    return df ['day_of_week'].value_counts().idxmax()
    
def popular_hour(df):
    # TO DO: display the most common start hour
    print('\n * What is the most popular hour of the day for bike traveling?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]


def trip_duration(df):
    """Displays statistics on the total and average trip duration."""

   

    # display total travel time
    print("\n* Travel time statistics")
    total_travel_time = df['Trip Duration'].sum()/86400
    print("Total travel time in days :", total_travel_time)

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()/60
    print("Average travel time in hours :", average_travel_time)
    return total_travel_time, average_travel_time
 


def popular_stations(df):
    
    

    # display most commonly used start station
   start_station = df['Start Station'].value_counts().idxmax(skipna = True)
   print("\n*The most commonly used start station :",start_station)

    # display most commonly used end station
   end_station = df['End Station'].value_counts().idxmax(skipna = True)
   print("\n*The most commonly used end station :", end_station)
   return start_station, end_station


def popular_trip(df):
    df['pop_trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    result = df['pop_trip'].mode().to_string(index = False)
   
    print('\n* The most popular trip is {}.'.format(result))

def users(df):
    
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    
    return df['User Type'].value_counts()

def gender(df):
    """Displays the gender of bikeshare users."""

    try:
        print('\n* What is the breakdown of gender among users?\n')

        return df.groupby('Gender')['Gender'].count()                            
    except:
        print('There is no gender data in the source.')
    
def birth_years(df):
   
    try:
        print('\n* What is the earliest, latest, and most common year of birth')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest) + "\n")
        most_common= df['Birth Year'].mode()[0]
        print ("The most common year of birth is " + str(most_frequent) + "\n")
        return earliest, latest, most_frequent
    except:
        print('No available birth date data for this period.')
def compute_stat(f, df):
   
    
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))

def get_max_day_of_month(df, month):
    
    months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
    df = df[df["month"] == months[month]]
    
    maxDay = max(df["day_of_month"])
    return maxDay

   
    city = get_city()

    df = load_data(city)

    time_period = get_time_period()

    month = get_month(time_period)
    day = get_day(time_period)
    monthAndDay = get_day_of_month(df, time_period)

    df = apply_time_filters(df, time_period, month, day, monthAndDay)

def city_info():
   
    city = get_city()

    df = load_data(city)

    time_period = get_time_period()

    month = get_month(time_period)
    day = get_day(time_period)
    monthAndDay = get_day_of_month(df, time_period)

    df = apply_time_filters(df, time_period, month, day, monthAndDay)

    
    
    stat_function_list = [popular_month,
     popular_day, popular_hour, 
     trip_duration, popular_trip, 
     popular_stations, users, birth_years,gender]

    for function in stat_function_list:
        compute_stat(function, df)

    # Restart?
    restart = input("\n * Would you like to restart and perform another analysis? Type \'yes\' or \'no\'.\n")
    if restart.lower() == 'yes' or restart.lower() == "y":
        city_info()
    
if __name__ == '__main__':
    city_info() 
