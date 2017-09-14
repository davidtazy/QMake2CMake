
class ConfigVisitor:
    def __init__(self,dictionnary):
        if isinstance(dictionnary, dict) is False:
            raise ValueError("not a dict")
        self.dictionnary = dictionnary

    def visit(self,cmake_writer, config):
        if config in self.dictionnary:

            if 'function' not in  self.dictionnary[config]:
                raise ValueError("please define 'function' associated to %s config"%(config))

            function = getattr(cmake_writer, self.dictionnary[config]['function'])
            if function is not None:
                if 'arg' in self.dictionnary[config]:
                    function(self.dictionnary[config]['arg'])
                else:
                    function()