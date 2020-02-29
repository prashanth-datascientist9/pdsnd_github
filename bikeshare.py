import time
import pandas as pd
import numpy as np
import calendar

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_question = 'Please enter the name of city that you want to explore data - chicago, new york city or washington.\n'
    city = input(city_question)
    if city not in('Chicago', 'New York City', 'Washington'):
        print('Please consider entering city names as titles. ex: Chicago, New York City....\n')
    while city.lower() not in ('chicago', 'new york city', 'washington'):
        city = input(city_question)
        if city not in('Chicago', 'New York City', 'Washington'):
            print('Please consider entering city names as titles next time. ex: Chicago, New York City....\n')



    # TO DO: get user input for month (all, january, february, ... , june)
    month_question = 'Please enter a month from this list - all, january, february, march, april, may, june.\n'
    month = input(month_question)
    if month not in('All', 'January', 'February', 'March', 'April', 'May', 'June'):
        print('Please consider entering month names as titles. ex: All, January, February....\n')
    while month.lower() not in('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input(month_question)
        if month not in('All', 'January', 'February', 'March', 'April', 'May', 'June'):
            print('Please consider entering month names as titles next time. ex: All, January, February....\n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_question = 'Please enter the day of week - all, monday, tuesday, wednesday, thursday, friday, saturday, sunday.\n'
    day = input(day_question)
    if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        print('Please consider entering day of week names as titles. ex: All, Monday, Tuesday....\n')
    while day.lower() not in('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input(day_question)
        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print('Please consider entering day of week names as titles next time. ex: All, Monday, Tuesday....\n')

    print('-'*40)
    return city.lower(), month.lower(), day.lower()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    print('The most common month of travel is {}'.format(calendar.month_name[most_common_month]))

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    most_common_dayofweek = df['day_of_week'].mode()[0]
    print('The most common day of week for travel is {}'.format(most_common_dayofweek))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common start hour of day for travel is {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    df['start_station'] = df['Start Station']
    most_common_start_station = df['start_station'].mode()[0]
    print('The most common start station for travel is {}'.format(most_common_start_station))

    # TO DO: display most commonly used end station
    df['end_station'] = df['End Station']
    most_common_end_station = df['end_station'].mode()[0]
    print('The most common end station for travel is {}'.format(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    most_freq_start_end_comb = df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'count'})
    most_freq_start_end_comb_sorted = most_freq_start_end_comb.sort_values(by='count', ascending=False)
    most_freq_start_end_stations = most_freq_start_end_comb_sorted.head(1)
    print("The most freq start and end station for travel is '{}' and '{}' with a total count of {} combinations".format(most_freq_start_end_stations.iat[0, 0], most_freq_start_end_stations.iat[0, 1], most_freq_start_end_stations.iat[0, 2]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is {} seconds'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types : \n{}'.format(user_types))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nGender : \n{}'.format(gender))
    else:
        print('No Gender data available in this dataset. Please choose another city.')


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('\nEarliest, most recent, and most common year of birth are : {}, {}, {}'.format(int(earliest_year), int(recent_year), int(most_common_year)))
    else:
        print('No Birth Year data available in this dataset. Please choose another city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """
    Asks user if they want to see the raw data.

    Returns:
        (DataFrame) rows - 5 rows at a time
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    raw_data_question = '\nWould you like to see the raw data (5 rows at a time)? Enter yes or no.\n'
    see_raw_data = input(raw_data_question)
    counter = 0
    while see_raw_data.lower() == 'yes':
        print('-'*40)
        print(df.iloc[counter:(counter + 5), :])
        counter = counter + 5
        print('-'*40)
        see_raw_data = input(raw_data_question)

def main():
    while True:
        city, month, day = get_filters()
        print('The entered values for city, month and day are {}, {}, {}'.format(city, month, day))

        df = load_data(city, month, day)
        #print(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
