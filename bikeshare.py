import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york location': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a location, month, and day to analyze.

    Returns:
        (str) location - name of the location to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for location (chicago, new york location, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        location = input("Would you like to see data for Chicago, New York location, or Washington?\n ")
        location = location.lower()
        if location in ['chicago', 'new york location', 'washington']:
            break
        else:
            print('Error: Please enter one of the location names: Chicago, New York location, or Washington\n')


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('For which month would you like to see the data? January, February, March, April, May, June or all? Type "all" for no month filter.\n ')
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Error: Please enter one of the following months: January, Februrary, March, April, May, June. Or type "all" for no month filter.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would you like to see? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all? Type "all" for no day filter.\n ')
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Error: Please enter one of the following days: Mon, Tue, Wed, Thu, Fri, Sat, Sun. Or type "all" for no day filter.\n')

    print('-'*40)
    return location, month, day


def load_data(location, month, day):
    """
    Loads data for the specified location and filters by month and day if applicable.

    Args:
        (str) location - name of the location to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing location data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[location])

    # convert the Start Time column to datetimew
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new column for month and day. Extracted from Start Time.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

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
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, location, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('Set filter\nCity: {}, Month: {}, Day: {}\n'.format(location, month, day))
    start_time = time.time()

    #Check if values in month are unequal to 'month' from the user input
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    if len(df['month'].unique()) > 1 or df['month'].unique() != month:
        # display the most common month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month_name = months[df['month'].mode()[0]-1].capitalize()
        popular_month = df['month'].mode()[0]
        percentage_popular_month = int(round(((df.groupby(['month'])['month'].count()[popular_month] / df['month'].value_counts().sum()) * 100),0))
        print('The most common month is: {}. This month makes up {} % of all data.'.format(popular_month_name, percentage_popular_month))

    #Check if values in day_of_week are unequal to 'day' from the user input
    if len(df['day_of_week'].unique()) > 1 or df['day_of_week'].unique() != day:
         # display the most common day of week
        popular_day = df['day_of_week'].mode()[0]
        percentage_popular_day = int(round(((df.groupby(['day_of_week'])['day_of_week'].count()[popular_day] / df['day_of_week'].value_counts().sum()) * 100),0))
        print('The most common day is: {}. This day makes up {} % of all data.'.format(popular_day.capitalize(), percentage_popular_day))

    # display the most common start hour (from 0 to 23)
    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    ## calculate most common start hour
    popular_hour = df['hour'].mode()[0]
    percentage_popular_hour = int(round(((df.groupby(['hour'])['hour'].count()[popular_hour] / df['hour'].value_counts().sum()) * 100),0))
    print('The most common start hour is: {}. This start hour makes up {} % of all data.'.format(popular_hour, percentage_popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, location, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('Set filter\nCity: {}, Month: {}, Day: {}\n'.format(location, month, day))
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common start station is:', popular_start_station)
          
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common end station is:', popular_end_station)


    # display most frequent combination of start station and end station trip
    ## Create variable merging start and end station
    trip = df['Start Station'] + " to " + df['End Station']
    popular_trip = trip.mode()[0]
    print('The most common trip is:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def convert_seconds(seconds):
    """Transfers input into dd:hh:mm:ss. Used to transfer travel time (given in seconds)"""

    # Ensure data input is integer
    seconds = int(seconds)
    # Calculate days, hours, minutes, seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return "{:04d}d {:02d}:{:02d}:{:02d}".format(days, hours, minutes, seconds)


def trip_duration_stats(df, location, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print('Set filter\nCity: {}, Month: {}, Day: {}\n'.format(location, month, day))
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    formatted_total_travel_time = convert_seconds(total_travel_time)
    print('The total travel time (days hh:mm:ss) for 2017 is:', formatted_total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    sd_travel_time = np.std(df['Trip Duration'])
    formatted_sd_travel_time = convert_seconds(sd_travel_time)
    formatted_mean_travel_time = convert_seconds(mean_travel_time)
    print('The mean travel time (days hh:mm:ss) is {}, with a standard deviation (days hh:mm:ss) of {}.'.format(formatted_mean_travel_time, formatted_sd_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, location, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print('Set filter\nCity: {}, Month: {}, Day: {}\n'.format(location, month, day))
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('Count per user type...')
    print(count_user_types)

    # Display counts of gender
    if 'Gender' not in df.columns:
        print('\nUnfortunately, gender data cannot be shared due to missing values')
    else:
        count_gender = df['Gender'].value_counts()
        print('\nCount per gender...')
        print(count_gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('\nUnfortunately, birth year data cannot be shared due to missing values')
    else:
        earliest_birthyear = int(df['Birth Year'].min())
        recent_birthyear = int(df['Birth Year'].max())
        common_birthyear = int(df['Birth Year'].mode()[0])
        print('\nInformation on birth year...')
        print('Earliest birth year: {}\nMost recent birth year: {}\nMost common birth year: {}'.format(earliest_birthyear, recent_birthyear, common_birthyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Function to ask user if they want to display first 5 rows. Continues adding five rows until user says 'no" or no more data are available"""
    i = 0
    while True:
        decision_input = input('Would you like to see five rows of the raw data? Answer "yes" or "no".\n')
        decision_input = decision_input.lower()
        if decision_input in ['yes', 'no']:
            if decision_input == 'yes':
                if i < len(df):
                    print(df.iloc[i:i+5])
                    i += 5
                else:
                    print('\nUnforunately, no more data is available\n')
                    break
            elif decision_input == 'no':
                break
        else:
            print('Error: Please enter "yes" or "no".\n')



def main():
    while True:
        location, month, day = get_filters()
        df = load_data(location, month, day)

        time_stats(df, location, month, day)
        station_stats(df, location, month, day)
        trip_duration_stats(df, location, month, day)
        user_stats(df, location, month, day)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
