import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('What city would you like to explore?... chicago, new york city or washington \n')
    
    cities = ['chicago', 'new york city', 'washington']
    
    while True:
        try:
            city = input('City name: ').lower()
            
            if city not in cities:
                print('Please input a valid city name: chicago, new york city or washington')
            else:
                break
               
        finally:
            print('City name has been provided as {} \n'.format(city.title()))
            
    # get user input for month (all, january, february, ... , june)
    print('Which month would you like to explore?... january, february,...,june or all \n')
    
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    
    while True:
        try:
            month = input('Month name: ').lower()
            
            if month not in months:
                print('Please input a valid month name: january, february,...,june or all for no filter')
            
            else:
                break
             
        finally:
            print('Month name has been provided as {} \n'.format(month.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Which day would you like to explore?... monday, tuesday, ..., sunday or all \n')
    
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    
    while True:
        try:
            day = input('Day name: ').lower()
            
            if day not in days:
                print('Please input a valid day name: monday, tueday,..., sunday or all for no filter')
            
            else:
                break
                
        finally:
            print('Day name has been provided as: ', day, '\n')

    print('-'*40)
    return city, month, day

city, month, day = get_filters()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    

    
    df = pd.read_csv(CITY_DATA[city])
    
    # Reconstructing the date culumn for easy manipulation
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Adding a separate month culumn for filtering by month
    df['month'] = df['Start Time'].dt.month
    
    # Adding a separate day of th week (dow) culmn for filtering by day
    df['dow'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        month_index = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}
        new_month = month_index[month]
        df = df[df['month'] == new_month]
    if day != 'all':
        new_day = day.title()
        df = df[df['dow'] == new_day]

    return df
df = load_data(city, month, day)


def raw_data(df):
    i = 0
    
    user_response = input('Would you like to see the first 5 rows (raw data) for {} before you continue?...yes or no: '.format(city.title())).lower()
    
    while user_response == 'yes' and i+5 < df.shape[0]:
        
        print(df.iloc[i: i + 5])
        i += 5
        user_question = input('Would you like to see the next 5 rows of the {} data? Please enter yes or no: '.format(city.title())).lower()
        if user_question != 'yes':
            break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    month_index = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    
    # display the most common month
    # display the most common day of week
    
    if month != 'all' and day != 'all':
        print('You filtered by {} and {}, by default they are the most common month and day of the week'. format(month.title(), day.title()))
        print('\n')
    
    elif month != 'all' and day == 'all':
        
        comm_day = df['dow'].mode()[0]
        
        print('The most common day of the week for the month of {} is {}'. format(month.title(), comm_day))
    
    elif month == 'all' and day != 'all':
        
        comm_month = df['month'].mode()[0]
        new_month = month_index[comm_month]
        
        print("The most popular month for the day ({}) you filtered by is: ".format(day.title()), new_month)
          
    else:
        comm_month = df['month'].mode()[0]
        new_month = month_index[comm_month]
        comm_day = df['dow'].mode()[0]
        
        print('The most common month is ', new_month, '\n')
        print('The most common day of the week is ', comm_day, '\n')
    
    # display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour
    comm_hour = df['hour'].mode()[0]
    
    print('The most common start hour is ', comm_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most common start station is: ', start_station, '\n')

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most common end station is: ', end_station, '\n')

    # display most frequent combination of start station and end station trip
    freq_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent start and end stations are: \n')
    print(freq_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print('Total travel time in seconds: ', travel_time, '\n')

    # display mean travel time
    travel_time_mean = df['Trip Duration'].mean()
    print('The mean travel time is: ', travel_time_mean, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types: \n', user_types, '\n')

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('Gender count: \n', gender_count)
    except KeyError:
      print("\nGender count:\nNo data available.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        comm_year = df['Birth Year'].mode()[0]

        print('Earliest year: {}\n Recent year: {}\n Most common year: {}\n'.format(earliest_year, recent_year, comm_year))
    
    except KeyError:
      print("\nGender count:\nNo birth year data available for {}.".format(city.title()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            
# Trying something new from here down....

            print('Will you like compare two different cities? \n')
            response = input('yes or no: \n').lower()
            if response == 'yes':
                print('Here we go again.....\n')

                
                def filters():
                    """
                    Asks user to specify a city and month to analyze.

                    Returns:
                        (str) city_1 & city_2 - names of the cities to analyze
                        (str) month - name of the month to filter by, or "all" to apply no month filter
                    """
    
                    print('\nHello! Let\'s explore some US bikeshare data!\n')


                    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
                    print('\nWhic 2 cities would you like to explore?... chicago, new york city or washington \n')

                    cities = ['chicago', 'new york city', 'washington']
    
                    while True:
                        try:
                            city_1 = input('First City name: ').lower()
                            city_2 = input('Second City name: ').lower()

                            if city_1 not in cities or city_2 not in cities:
                                print('\nPlease input a valid city name: chicago, new york city or washington\n')
                            elif city_1 == city_2:
                                print('\nPlease enter two different cities...\n')
                            else:
                                break

                        finally:
                            print('Cities to compare are {} and {}\n'.format(city_1.title(), city_2.title()))
            
                        # get user input for month (all, january, february, ... , june)
                        print('\nWhich month would you like to explore?... january, february,...,june or all \n')

                    months_ = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

                    while True:
                        try:
                            month_ = input('Month name: ').lower()

                            if month_ not in months_:
                                print('Please input a valid month name: january, february,...,june or all for no filter')

                            else:
                                break

                        finally:
                            print('Month name has been provided as: ', month_, '\n')
                
                    print('-'*40)
                    return city_1, city_2, month_

                city_1, city_2, month_ = filters()

                
                def loading_data(city_1, city_2, month_):
                    """
                    Loads data for the specified cities and filters by month if applicable.

                    Args:
                        (str) city_1 & _2 - names of the cities to analyze
                        (str) month - name of the month to filter by, or "all" to apply no month filter

                    Returns:
                        df - Pandas DataFrame containing cities data filtered by month
                    """



                    df_1 = pd.read_csv(CITY_DATA[city_1])
                    df_2 = pd.read_csv(CITY_DATA[city_2])

                    # Reconstructing the date culumn for easy manipulation
                    df_1['Start Time'] = pd.to_datetime(df_1['Start Time'])
                    df_2['Start Time'] = pd.to_datetime(df_2['Start Time'])

                    # Adding a separate month culumn for filtering by month
                    df_1['month'] = df_1['Start Time'].dt.month
                    df_2['month'] = df_2['Start Time'].dt.month

                    if month_ != 'all':
                        month_index = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}
                        new_month = month_index[month_]
                        df_1 = df_1[df_1['month'] == new_month]
                        df_2 = df_2[df_2['month'] == new_month]

                    return df_1, df_2
                df_1, df_2 = loading_data(city_1, city_2, month_)              

                def time_travel_stats(df_1, df_2):
                    """Displays statistics on the most frequent times of travel."""

                    print('\nCalculating The Most Frequent Times of Travel...\n')
                    start_time = time.time()

                    month_index = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}

                    # display the most common month
                    # display the most common day of week

                    if month_ != 'all':
                        print('\nYou filtered by {}, by default it is the most common month\n'.format(month.title()))
                    
                    else:

                        comm_month_1 = df_1['month'].mode()[0]
                        comm_month_2 = df_2['month'].mode()[0]
                              
                        new_month_1 = month_index[comm_month_1]
                        new_month_2 = month_index[comm_month_2]

                        print('\nThe most common month for {} is {}\n'.format(city_1.title(), new_month_1))
                        print('\nThe most common month for {} is {}\n'.format(city_2.title(), new_month_2))
                                        

                    # display the most common start hour

                    df_1['hour'] = df_1['Start Time'].dt.hour
                    df_2['hour'] = df_2['Start Time'].dt.hour
                    comm_hour_1 = df_1['hour'].mode()[0]
                    comm_hour_2 = df_2['hour'].mode()[0]

                    print('\nThe most common start hour for {} is {}\n'.format(city_1.title(),comm_hour_1))
                    print('\nThe most common start hour for {} is {}\n'.format(city_2.title(),comm_hour_2))

                    print("\nThis took %s seconds." % (time.time() - start_time))
                    print('-'*40)              

                
                def station_stats_2(df_1, df_2):
                    """Displays statistics on the most popular stations and trip."""

                    print('\nCalculating The Most Popular Stations and Trip...\n')
                    start_time = time.time()

                    # display most commonly used start station
                    start_station_1 = df_1['Start Station'].mode()[0]
                    start_station_2 = df_2['Start Station'].mode()[0]
                    print('\nThe most common start station for {} is: {}\n'.format(city_1.title(), start_station_1))
                    print('\nThe most common start station for {} is: {}\n'.format(city_2.title(), start_station_2))

                    # display most commonly used end station
                    end_station_1 = df_1['End Station'].mode()[0]
                    end_station_2 = df_2['End Station'].mode()[0]
                    print('\nThe most common end station for {} is: {}\n'.format(city_1.title(), end_station_1))
                    print('\nThe most common end station for {} is: {}\n'.format(city_2.title(), end_station_2))


                    # display most frequent combination of start station and end station trip
                    freq_stations_1 = df_1.groupby(['Start Station', 'End Station']).size().nlargest(1)
                    freq_stations_2 = df_2.groupby(['Start Station', 'End Station']).size().nlargest(1)

                    print('\nThe most frequent start and end stations for {} are: \n'.format(city_1))
                    print(freq_stations_1)
                    print('\nThe most frequent start and end stations for {} are: \n'.format(city_2))
                    print(freq_stations_2)

                    print("\nThis took %s seconds." % (time.time() - start_time))
                    print('-'*40)


                def trip_duration_stats_2(df_1, df_2):
                    """Displays statistics on the total and average trip duration."""

                    print('\nCalculating Trip Duration...\n')
                    start_time = time.time()

                    # display total travel time
                    travel_time_1 = df_1['Trip Duration'].sum()
                    travel_time_2 = df_2['Trip Duration'].sum()
                              
                    print('\nTotal travel time for {} in seconds: {}\n'.format(city_1.title(), travel_time_1))
                    print('\nTotal travel time for {} in seconds: {}\n'.format(city_2.title(), travel_time_2))
                    if travel_time_1 > travel_time_2:
                        print('{} has more travel time than {}\n'.format(city_1.title(), city_2.title()))
                    elif travel_time_2 > travel_time_1:
                        print('{} has more travel time than {}\n'.format(city_2.title(), city_1.title()))
                    else:
                        print('{} and {} have equal travel time\n'.format(city_1.title(), city_2.title()))
                              
                    # display mean travel time
                    travel_time_mean_1 = df_1['Trip Duration'].mean()
                    travel_time_mean_2 = df_2['Trip Duration'].mean()
                              
                    print('\nThe mean travel time for {} is: {}\n'.format(city_1.title(), travel_time_mean_1))
                    print('\nThe mean travel time for {} is: {}\n'.format(city_2.title(), travel_time_mean_2))

                    print("\nThis took %s seconds." % (time.time() - start_time))
                    print('-'*40)

                
                def user_stats_2(df_1, df_2):
                    """Displays statistics on bikeshare users."""

                    print('\nCalculating User Stats...\n')
                    start_time = time.time()

                    # Display counts of user types
                    user_types_1 = df_1['User Type'].value_counts()
                    user_types_2 = df_2['User Type'].value_counts()
                          
                    print('User Types for {}: \n{}\n'.format(city_1.title(), user_types_1))
                    print('\nUser Types for {}: \n{}\n'.format(city_2.title(), user_types_2))
                    
                          
                    
                    # breaking down the dataframes to be able to get count of a single column  
            # Here I declear all these variables but i know them. Assuming i don't know the value, how do i handle this kind of situation?
                    sdf_1 = df_1[df_1['User Type'] == 'Subscriber']
                    sdf_2 = df_2[df_2['User Type'] == 'Subscriber']
                    cdf_1 = df_1[df_1['User Type'] == 'Customer']
                    cdf_2 = df_2[df_2['User Type'] == 'Customer']
                    ddf_1 = df_1[df_1['User Type'] == 'Dependent']
                    ddf_2 = df_2[df_2['User Type'] == 'Dependent']
                    
                    # getting the count figure for each user type and assigning it to a variable
                    sub_1 = sdf_1['User Type'].count()
                    sub_2 = sdf_2['User Type'].count()
                    cus_1 = cdf_1['User Type'].count()
                    cus_2 = cdf_2['User Type'].count()
                    dep_1 = ddf_1['User Type'].count()
                    dep_2 = ddf_2['User Type'].count()
                    
                    # comaparing individual user type    
                    if sub_1 > sub_2:
                        print('\n{} have more subscribers than {}\n'. format(city_1.title(), city_2.title()))
                    elif sub_2 > sub_1:
                        print('\n{} have more subscribers than {}\n'. format(city_2.title(), city_1.title()))
                    else:
                        print('\n{} and {} have equal number of subscribers\n'. format(city_1.title(), city_2.title()))
                    
                    if cus_1 > cus_2:
                        print('\n{} have more customers than {}\n'. format(city_1.title(), city_2.title()))
                    elif cus_2 > cus_1:
                        print('\n{} have more customers than {}\n'. format(city_2.title(), city_1.title()))
                    else:
                        print('\n{} and {} have equal number of customers\n'. format(city_1.title(), city_2.title()))
                          
                    if dep_1 > dep_2:
                        print('\n{} have more dependents than {}\n'. format(city_1.title(), city_2.title()))
                    elif dep_2 > dep_1:
                        print('\n{} have more dependents than {}\n'. format(city_2.title(), city_1.title()))
                    else:
                        print('\n{} and {} have equal number of dependents\n'. format(city_1.title(), city_2.title()))
                          
                          
                    # Display counts of gender
                    try:
                        gender_1 = df_1['Gender'].value_counts() 
                        print('\nGender count for {}: \n{}\n'.format(city_1.title(), gender_1))
                        gdf_m1 = df_1[df_1['Gender'] == 'Male']
                        gdf_f1 = df_1[df_1['Gender'] == 'Female']
                        
                        gender_male_1 = gdf_m1['Gender'].count()
                        gender_female_1 = gdf_f1['Gender'].count()
                        
                    except KeyError:
                        print("\nGender count:\nNo gender data available for {}.".format(city_1.title()))
                        
                        # Assigning 'nan' to know that there is no data available 
                        gender_male_1 = 'nan'
                        gender_female_1 = 'nan'
                    
                    try:
                        gender_2 = df_2['Gender'].value_counts()
                        print('\nGender count for {}: \n{}\n'.format(city_2.title(), gender_2))
                        gdf_m2 = df_2[df_2['Gender'] == 'Male']
                        gdf_f2 = df_2[df_2['Gender'] == 'Female']
                        
                        gender_male_2 = gdf_m2['Gender'].count()
                        gender_female_2 = gdf_f2['Gender'].count()
                        
                    except KeyError:
                        print("\nGender count:\nNo gender data available for {}.".format(city_2.title()))
                        
                        # Assigning 'nan' to know that there is no data available
                        gender_male_2 = 'nan'
                        gender_female_2 = 'nan'
                        
                    if gender_male_1 != 'nan' and gender_male_2 != 'nan' and gender_female_1 != 'nan' and gender_female_2 != 'nan':
                    
                        if gender_male_1 > gender_male_2:
                            print('\n{} have more male bikers than {}\n'.format(city_1.title(), city_2.title()))
                        elif gender_male_2 > gender_male_1:
                            print('\n{} have more male bikers than {}\n'.format(city_2.title(), city_1.title()))
                        else:
                            print('\n{} and {} have equal number male bikers\n'.format(city_1.title(), city_2.title()))

                        if gender_female_1 > gender_female_2:
                            print('\n{} have more female bikers than {}\n'.format(city_1.title(), city_2.title()))
                        elif gender_female_2 > gender_female_1:
                            print('\n{} have more female bikers than {}\n'.format(city_2.title(), city_1.title()))
                        else:
                            print('\n{} and {} have equal number female bikers\n'.format(city_1.title(), city_2.title()))
                    else:
                        print('\nIt appears that some data are not available, sorry... can\'t perform any comparison. Try another set of cities')
                    
                    # Display earliest, most recent, and most common year of birth
                    try:
                        earliest_year_1 = df_1['Birth Year'].min()
                        recent_year_1 = df_1['Birth Year'].max()
                        comm_year_1 = df_1['Birth Year'].mode()[0]

                        print('\nThe earliest year of birth for {} is {}\n'.format(city_1.title(), earliest_year_1))
        
                        print('\nThe most recent year of birth for {} is {}\n'.format(city_1.title(), recent_year_1))
                       
                        print('\nThe most common year of birth for {} is {}\n'.format(city_1.title(), comm_year_1))
                    

                    except KeyError:
                        print("\nNo birth year data available for {}.".format(city_1.title()))
                 
                    try:
                        earliest_year_2 = df_2['Birth Year'].min()
                        recent_year_2 = df_2['Birth Year'].max()
                        comm_year_2 = df_2['Birth Year'].mode()[0]
                        
                        print('\nThe earliest year of birth for {} is {}\n'.format(city_2.title(), earliest_year_2))
                        print('\nThe most recent year of birth for {} is {}\n'.format(city_2.title(), recent_year_2))                   
                        print('\nThe most common year of birth for {} is {}\n'.format(city_2.title(), comm_year_1))    

                    except KeyError:
                        print("\nNo birth year data available for {}.".format(city_2.title()))
                    
                    
                    print("\nThis took %s seconds." % (time.time() - start_time))
                    print('-'*40)
                             
                while True:
    
                        #city_1, city_2, month_ = filters()
                        #df_1, df_2 = load_data(city_1, city_2, month_)

                    time_travel_stats(df_1, df_2)
                    station_stats_2(df_1, df_2)
                    trip_duration_stats_2(df_1, df_2)
                    user_stats_2(df_1, df_2)

                    exiting = input('\nEnter any letter or number to exit.\n')
                    if exiting != '':
                        print('Exiting.........................')
                        break
 
            else:
                print('Ok... goodbye, see you next time')
            
# All the extra work I did... Is there a much simpler and better way of doing it? And any corrections too please...
# Thank you!!!
# Something new ends here

        break

if __name__ == "__main__":
	main()

