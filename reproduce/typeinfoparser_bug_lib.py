from robot.running.arguments.typeinfo import TypeInfo


class TypeInfoParserBugLib:

    def parse_type_string(self, type_string):
        TypeInfo.from_string(type_string)
