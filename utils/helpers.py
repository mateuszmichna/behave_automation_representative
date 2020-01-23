import re

from parse import parse


class Helpers(object):
    def get_numeric_from_string(self, string):
        modified_string = re.sub('[^0-9.]', '', string)
        floated_sting = float(modified_string)
        if floated_sting.is_integer():
            final_string = int(floated_sting)
        else:
            final_string = floated_sting
        return final_string

    def parse_text(self, text, parsing_format, which_fragment):
        return parse(parsing_format, text).fixed[which_fragment - 1]
