from pk.apis.seventyfivef.Read import Read as Read

class ReadByFilter(Read):
    def __init__(self):
        super().__init__()

    def get_body(self, read_argument):
        # NOTE:  The "id" filter does not use quotes around the argument, the "filter" filter does
        return f"ver:\"3.0\"\nfilter\n\"{read_argument}\""