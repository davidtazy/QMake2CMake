
class ConfigVisitor:
    def __init__(self,dictionnary):
        if isinstance(dictionnary, dict) is False:
            raise ValueError("not a dict")
        self.dictionnary = dictionnary

    def visit(self,cmake_writer, qmake_variable, value):
        if qmake_variable in self.dictionnary:
            qmake_variable_dico  = self.dictionnary[qmake_variable]
            self.convert_variable_to_cmake(cmake_writer, qmake_variable_dico,value)

    def convert_variable_to_cmake(self, cmake_writer, qmake_variable_dico, value):
        if value in qmake_variable_dico:

            if 'function' not in qmake_variable_dico[value]:
                raise ValueError("please define 'function' associated to %s qmake_variable" % (value))

            function_callback = getattr(cmake_writer, qmake_variable_dico[value]['function'])
            if function_callback is not None:
                if 'arg' in qmake_variable_dico[value]:
                    function_callback(qmake_variable_dico[value]['arg'])
                else:
                    function_callback()