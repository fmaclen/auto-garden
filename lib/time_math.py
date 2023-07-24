class TimeMath:
    def datetime_str_to_tuple(self, datetime_str: str):
        year, month, day, hours, minutes, seconds = self.extract_datetime_components(datetime_str)
        return year, month, day, 0, hours, minutes, seconds, 0, 0

    def datetime_str_to_timestamp(self, datetime_str: str):
        year, month, day, hours, minutes, seconds = self.extract_datetime_components(datetime_str)

        days_in_month = [
            31, 28 if not self.is_leap_year(year) else 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
        ]

        timestamp = (
            sum([86400 * self.days_in_year(y) for y in range(1970, year)]) +
            sum([86400 * days_in_month[m - 1] for m in range(1, month)]) +
            (day - 1) * 86400 +
            hours * 3600 +
            minutes * 60 +
            seconds
        )

        return timestamp

    def extract_datetime_components(self, datetime_str: str):
        # Remove 'Z' and split date and time
        date_str, time_str = datetime_str.rstrip('Z').split(' ')

        # Split date string into year, month, day
        year, month, day = (int(x) for x in date_str.split('-'))

        # Split time string into hours, minutes, seconds
        time_str = time_str.split('.')[0]  # Ignore the milliseconds
        hours, minutes, seconds = (int(x) for x in time_str.split(':'))

        return year, month, day, hours, minutes, seconds

    def is_leap_year(self, year):
        # Leap year is divisible by 4, except when it's divisible by 100 and not divisible by 400
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def days_in_year(self, year):
        return 366 if self.is_leap_year(year) else 365
