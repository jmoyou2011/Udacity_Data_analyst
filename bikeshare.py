import time
import pandas as pd
import numpy as np
import datetime

city_data = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_city():
    city = ""
    while city.title() not in ["Chicago", "New York","Washington"]:

        city = input()
        if city.title() == "Chicago":
            return city_data['Chicago']
        elif city.title() == "New York" or city.title() == "New York City":
            return city_data['New York City']
        elif city.title() == 'Washington':
            return city_data['Washington']
        else:
            print("Sorry, I do not understand your input. Please enter either "
                    "Chicago, New York, Washington.\n")


def get_month():

    month_in = ""
    month_dict = {"January": 1, "February": 2, "March": 3,
                 "April": 4, "May": 5, "June": 6}

    month_in = input("\nWhich month do you want to chose? "
                     "You can chose from January to June or none "
                     "for no filter: ")

    if month_in.lower() == "none":
        return 'all'
    elif month_in.title() in month_dict.keys():
        month_in = month_dict[month_in.title()]
    else:
        print('Sorry, I do not understand your input. The program will set '
              'to no filter.')
        return 'all'

    return ("2017-{}".format(month_in), "2017-{}".format(month_in + 1))


def get_day():
    """Ask the user for a day to search by.
    Args:
        None.
    Returns:
        (tuple) Lower lmit, upper limit of date for the bikeshare data.
    """

    this_month_str = get_month()# the value of the tuple is at [1] and [5]
    if this_month_str == 'all':
        return 'all'
    this_month = this_month_str[0]
    inner_month = this_month[5]


    correct_date = None
    try:
        input_date = input("\nWhich date would you like to select? "
                            "Respond with an integer:")
        input_date = int(input_date)
        check_month = int(inner_month)
        choice_date = datetime.datetime(2017, check_month, input_date)
        correct_date = True
    except ValueError:
        correctDate  = False
        print("Invalid date. Returning with no filter for the date.")
        return 'all'

    end_date = choice_date + datetime.timedelta(days=1)
    return (str(choice_date), str(end_date))


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("Cities available are: Chicago, New York City, Washington")
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()
    print("If you want no filter of data, please enter none twice when prompted.\n"
          "If you want to filter by a specific month and not a date; enter none for "
          "the second prompt for the month.")
    print("If you want to filter out both month and date, enter your month of interest twice "
          "and then your date.")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_month()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()

    print('-'*40)
    return city, month, day


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
    bike_dataframe = pd.read_csv(city, parse_dates=['Start Time', 'End Time'], infer_datetime_format=True)
    pd.set_option('max_colwidth', 100)

    # Create a column for the journey for the most common trip.
    bike_dataframe['Journey'] = bike_dataframe['Start Station'].str.cat(bike_dataframe['End Station'], sep=' to ')

    # Filtering data according to user.
    if month == 'all':
        print("No filtering requesting")
        df = bike_dataframe
    elif month != 'all' and day == 'all': # Filtering by a specific month
        lower_filter, upper_filter = month
        print("Applying month only filtering")
        df = bike_dataframe[(bike_dataframe['Start Time'] >= lower_filter) &
                        (bike_dataframe['Start Time'] < upper_filter)]
    elif month != 'all' and day != 'all':
        lower_filter, upper_filter = day
        print("Apply filtering using month and day")
        df = bike_dataframe[(bike_dataframe['Start Time'] >= lower_filter) &
                            (bike_dataframe['Start Time'] < upper_filter)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months_list = ('January', 'February', 'March', 'April', 'May', 'June')
    idx_mode_month = int(df['Start Time'].dt.month.mode())
    common_month = months_list[idx_mode_month - 1]
    print("The most popular month is: ", common_month)

    # TO DO: display the most common day of week
    days_of_week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
                   'Friday', 'Saturday', 'Sunday')
    idx_mode_day = int(df['Start Time'].dt.dayofweek.mode())
    common_day = days_of_week[idx_mode_day]
    print("The most popular day of week for start time is:", common_day)

    # TO DO: display the most common start hour
    common_start_hour = int(df['Start Time'].dt.hour.mode())
    print("The most popular hour of the day for start time is {}:00 hours".format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode().to_string(index=False)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode().to_string(index=False)

    # TO DO: display most frequent combination of start station and end station trip
    common_journey = df['Journey'].mode().to_string(index=False)

    print("The most common used start station:{}".format(common_start_station))
    print("The most common used end station:{}".format(common_end_station))
    print("The most common journey:{}".format(common_journey))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

     # TO DO: display total travel time
    travel_time = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    travel_time_mean = df['Trip Duration'].mean()

    print("Total travel time duration:{} seconds".format(travel_time))
    print("Mean travel time duration:{0:.4f} seconds".format(travel_time_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        count_users = df['User Type'].value_counts().to_dict()
        for user_type, count in count_users.items():
            print("There are {} {}.".format(count, user_type))
    except KeyError as e:
        print("There exists no feature {} for this dataset.".format(str(e)))

    try:
        count_gender = df['Gender'].value_counts().to_dict()
        for user_gender, i in count_gender.items():
            print("There are {} {}".format(i, user_gender))
    except KeyError as ee:
        print("There exists no feature {} for this dataset.".format(str(ee)))

    try:
        earliest_age = int(df['Birth Year'].min())
        latest_age = int(df['Birth Year'].max())
        mode_age = int(df['Birth Year'].mode())

        print("The oldest users were born in {}.\nThe youngest users were born in {}.\n"
             "The most popular birth year is {}.".format(earliest_age, latest_age, mode_age))
    except KeyError as eee:
        print("There exists no feature {} for this dataset.".format(str(eee)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):

    """ Display five lines of the dataset if the user specifies that they would like to view.
        After showing the five data points, request from the user if they like to view five more.
        Continue until the user specifies a stop condition

    Args:
        df - Dataframe

    Returns:
        None

    """

    start = 0
    end =  5
    flag_input = False
    while flag_input == False:
        # Request user if they want to see the dataset.
        display_data = input("\nDo you want to view individual trip data? "
                             "Enter either 'yes' or 'no': ")

        if display_data.title() in ['Yes', 'No']:
            flag_input = True
            break
        else:
            flag_input = False
            print("Input invalid. Please enter either 'yes' or 'no' as your response: ")

    if display_data.title() == 'Yes':
        # Print the row except the journey column.
        print(df[df.columns[0:-1]].iloc[start:end-1])
        show_more = " "
        while show_more.title() != 'No':
            flag_input_2 = False
            while flag_input_2 == False:
                show_more = input("\nDo you want to view more of the dataset? "
                                  "Enter either 'yes' or 'no': ")

                if show_more.title() in ['Yes', 'No']:
                    flag_input_2 = True
                    break
                else:
                    flag_input_2 = False
                    print("Input invalid. Please enter 'yes' or 'no' as your response: ")

            if show_more.title() == 'Yes':
                start += 5
                end += 5
                print(df[df.columns[0:-1]].iloc[start:end-1])
            elif show_more.title() == 'No':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)
        #print(df.shape)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
