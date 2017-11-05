import enum


@enum.unique
class ResolutionUnits(enum.Enum):
    PixelsPerInch       = 1
    PixelsPerCentimeter = 2

    def __str__(self):
        return self.name


class Resolution:

    def __init__(self, resolution, units):
        self.resolution = resolution
        self.units      = units

    def make_resolution(resolution_val, unit_str):
        if unit_str not in ResolutionUnits.__members__.keys():
            raise ValueError('\'unit_str\' must be one of: {}'.format(ResolutionUnits.__members__.keys()))
        
        if type(resolution_val) is not int:
            raise TypeError('\'resolution_val\' must be a positive integer')

        if resolution_val <= 0:
            raise ValueError('\'resolution_val\' must be a positive integer')
        
        return Resolution(resolution_val, ResolutionUnits.__members__[unit_str])

    def unit_str(self):
        return str(self.units)

    def __repr__(self):
        return 'Resolution({}, {})'.format(self.resolution, self.units)

    def __str__(self):
        return '{} {}'.format(self.resolution, self.units)

