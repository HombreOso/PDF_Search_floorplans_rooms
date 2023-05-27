import math

class Point:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y



def get_perpendicular_base(XYZ_point, XYZ_line_start, XYZ_line_end):
    """
    Given a line and a point, find coordinates of the base of the perpendicular which is drawn from this point onto that line.
    Needed because LeaderEnd property of IndependentTag class has been deprecated for Revit API 2023
    """

    X_point, Y_point = XYZ_point.X, XYZ_point.Y
    X_line_start, Y_line_start = XYZ_line_start.X, XYZ_line_start.Y
    X_line_end, Y_line_end = XYZ_line_end.X, XYZ_line_end.Y

    if X_line_end == X_line_start:

        Y_base = Y_point
        X_base = X_line_start
        return X_base, Y_base


    slope_line = (Y_line_end - Y_line_start) / (X_line_end - X_line_start)

    if slope_line == 0:
        Y_base = Y_line_start
        X_base = X_point
        return X_base, Y_base

    slope_perpendicular = - 1/ slope_line

    Y_base = (slope_line * slope_perpendicular * (X_point - X_line_start) - slope_line * Y_point + slope_perpendicular * Y_line_start) / (slope_perpendicular - slope_line)

    X_base = X_point - (Y_point - Y_base) / slope_perpendicular

    return X_base, Y_base


XYZ_point = Point(4 ,4)

XYZ_line_start = Point(0, 0)

XYZ_line_end = Point(0, 13)

print(get_perpendicular_base(XYZ_point, XYZ_line_start, XYZ_line_end))