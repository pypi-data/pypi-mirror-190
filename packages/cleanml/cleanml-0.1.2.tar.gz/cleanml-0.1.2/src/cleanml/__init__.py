# read version from installed package
from importlib.metadata import version
__version__ = version("cleanml")

# populate package namespace
from cleanml.cleanml import make_column_names
from cleanml.cleanml import remove_spl_chars_in_columns