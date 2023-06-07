from qa_engine import Analyzer
from qa_report import ReportSection, ReportItem, ReportGroupType
from pyrevit import HOST_APP, EXEC_PARAMS
from pyrevit import revit, DB, UI
from pyrevit import script
import math

import Autodesk.Revit.DB as db



"""
Environment variables
"""
doc = revit.doc
uidoc = HOST_APP.uidoc
logger = script.get_logger()


"""
Constants

"""
# Human readable name of the collector
NAME = 'Check if the elements are tagged'
# Short description of the collector
DESCRIPTION = 'Check if the elements are tagged'
# Author
AUTHOR = 'Arthur Emig'
# The arguments that could be passed to the analyzer
ARG_TYPES = {
    "Count Report Type": [t.value for t in ReportGroupType],
    "Print Details": bool,
    "Max Printed Items": int,
}
# Default values of arguments
DEFAULT_ARGS = {
    "Count Report Type": ReportGroupType.TEST.value,
    "Print Details": True,
    "Max Printed Items": 1000,
}


# Minimal distance between sloped pipe tags
MINIMAL_DISTANCE_INCHES = 6

"""
Environment variables

"""
doc = revit.doc
uidoc = HOST_APP.uidoc
logger = script.get_logger()


"""
Analyzer class

"""
class IsTaggedAnalyzer(Analyzer):
    name = NAME
    _author = AUTHOR

    def analyze(self, data, **kwargs):
        desc = DESCRIPTION
        desc += " through {count} elements".format(count=len(data))
        section = ReportSection(name=NAME,
                                description=desc,
                                type=ReportGroupType.TEST,
                                auto_count=False,
                                print_details=True)
        report_type = kwargs.get("Count Report Type", DEFAULT_ARGS["Count Report Type"])
        print_details = kwargs.get("Print Details", DEFAULT_ARGS["Print Details"])
        max_printed_items = kwargs.get("Max Printed Items", DEFAULT_ARGS["Max Printed Items"])
        section = ReportSection(name=NAME,
                              description=desc,
                              type=ReportGroupType(report_type),
                              auto_count=True,
                              print_details=print_details)
        section.max_printed_items = max_printed_items
        for element in data:
            if element is None:
                continue

            name = "Unknown"
            if hasattr(element, "Name"):
                name = element.Name

            category = "Unknown"
            if element.Category:
                category = element.Category.Name

            item = ReportItem(
                name=name,
                description="{category} - {id}".format(
                    category=category,
                    id=element.Id.IntegerValue
                ),
                element_ids=[element.Id.IntegerValue],
                passed=is_double_tagged(elem=element),
            )
            section.add_item(item)

        # element_count = len(data)
        # if element_count > 0:
        #     section.passed_ratio = 1.0 - float(len(section.items)) / len(data)
        # else:
        #     section.passed_ratio = 1.0
        return section
    
def get_perpendicular_base(XYZ_point, XYZ_line_start, XYZ_line_end):
    """
    Given a line and a point, find coordinates of the base of the perpendicular which is drawn from this point onto that line.
    Needed because LeaderEnd property of IndependentTag class has been deprecated for Revit API 2023
    """

    X_point, Y_point = XYZ_point.X, XYZ_point.Y
    X_line_start, Y_line_start = XYZ_line_start.X, XYZ_line_start.Y
    X_line_end, Y_line_end = XYZ_line_end.X, XYZ_line_end.Y

    if X_line_end == X_line_start: 
        # if the pipe is parallel to Y axis

        Y_base = Y_point
        X_base = X_line_start
        return X_base, Y_base


    slope_line = (Y_line_end - Y_line_start) / (X_line_end - X_line_start)

    if slope_line == 0:
        # if the pipe is parallel to X axis
        Y_base = Y_line_start
        X_base = X_point
        return X_base, Y_base

    slope_perpendicular = - 1/ slope_line

    Y_base = (slope_line * slope_perpendicular * (X_point - X_line_start) - slope_line * Y_point + slope_perpendicular * Y_line_start) / (slope_perpendicular - slope_line)

    X_base = X_point - (Y_point - Y_base) / slope_perpendicular

    return X_base, Y_base


def get_points(pipe):
    """Get the start and end point of a pipe."""
    curve = pipe.Location.Curve
    point0 = curve.GetEndPoint(0)
    point1 = curve.GetEndPoint(1)
    return point0, point1


def distance_between_points(point1, point2):

    """
    Find distance between two planar points
    """

    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


def is_double_tagged(elem):
    """
    Check if the elememt (elem) has hosted independent tags.
    """
    filter_ = db.ElementClassFilter(db.IndependentTag)

    dependent_tags = elem.GetDependentElements(filter_)

    if len(dependent_tags) != 2:
        return False
    
    tag_head_position_first_tag = doc.GetElement(dependent_tags[0]).TagHeadPosition
    # print(dependent_tags)
    tag_head_position_second_tag = doc.GetElement(dependent_tags[1]).TagHeadPosition

    print("Tag Position: ", tag_head_position_first_tag)

    distance_between_tags = math.sqrt((tag_head_position_first_tag[0] - tag_head_position_second_tag[0])**2 + (tag_head_position_first_tag[1] - tag_head_position_second_tag[1])**2)
    print("Distance:", distance_between_tags)

    tagged_pipe = doc.GetElement(dependent_tags[0]).GetTaggedLocalElements()[0]

    XYZ_pipe_start, XYZ_pipe_end = get_points(tagged_pipe)

    perp_base_tag_1 = get_perpendicular_base(XYZ_point=tag_head_position_first_tag,
                                             XYZ_line_start=XYZ_pipe_start,
                                             XYZ_line_end=XYZ_pipe_end)
    
    perp_base_tag_2 = get_perpendicular_base(XYZ_point=tag_head_position_second_tag,
                                             XYZ_line_start=XYZ_pipe_start,
                                             XYZ_line_end=XYZ_pipe_end)
    
    distance_between_leader_ends = distance_between_points(perp_base_tag_1, perp_base_tag_2)

    print("Distance between leader ends:", distance_between_leader_ends)




    return distance_between_leader_ends >= MINIMAL_DISTANCE_INCHES

"""
Export the Analyzer class
"""
export = IsTaggedAnalyzer()
