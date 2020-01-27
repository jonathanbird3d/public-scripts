import operator


class TempTracker(object):
    """Stores temperature values

    Insert new temperatures (int), get highest or lowest recorded temperature
    or get average (float)

    Attributes:
        temps: Array of integers of temperatures
        scale: String representing scale of temperature, 'fahrenheit' or 'celsius'
        temp_range: List of min and max temperatures, default is [0, 110]
    """

    def __init__(self, temps = [], scale = 'fahrenheit', temp_range = [0, 110]):
        """Initialize the TempTracker object with optional temps, scale, temp_range values"""
        self.temps = temps
        self.scale = scale
        self.temp_range = temp_range

    def insert(self, new_temp):
        """Add new temperature as int"""
        if isinstance(new_temp, (int, long)):
            self.temps.append(new_temp)
        else:
            raise TypeError('Expected int but got {0}'.format(type(new_temp)))

    def get_max(self):
        """Return highest recorded temperature as int"""
        if len(self.temps) > 0:
            return max(self.temps)
        else:
            return None

    def get_min(self):
        """Return lowest recorded temperature as int"""
        if len(self.temps) > 0:
            return min(self.temps)
        else:
            return None

    def get_mean(self):
        """Return average temperature as float"""
        total_temp = 0
        recordings = 0
        if self.temps > 0:
            for temp in self.temps:
                if isinstance(temp, (int, long)):
                    recordings += 1
                    total_temp += temp
                else:
                    raise TypeError('Found entry of type {0} {1}'.format(type(temp), temp))
        else:
            return None
        mean = operator.truediv(total_temp, recordings)
        return mean
