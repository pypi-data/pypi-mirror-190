import string

def make_column_names(df, column_dict=None):
    """clean dataframe column names by lowering the case and replacing spaces with underscores.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to clean

    column_dict : dict
        A dictionary of old column names and their new names.

    Returns
    -------
    pandas.DataFrame
        The cleaned dataframe

    Examples
    --------
    >>> make_column_names(df, column_dict={'old_column_name': 'new_column_name'})  
    >>> make_column_names(df) # default column_dict is None   
    """
    column_names = df.columns
    if column_dict is not None:
        df.rename(columns=column_dict, inplace=True)
    for column in column_names:        
        df.rename(columns={column: column.lower().replace(" ", "_").replace("-", "_")}, inplace=True)          
    return df


def remove_spl_chars_in_columns(df, spl_chars_excepted=['_']):
    """remove spl_chars_excepted from column names.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe which consists of columns with special characters
    
    spl_chars_excepted : list
        A list of characters which should be kept in the column name.

    Returns
    -------
    pandas.DataFrame
        The cleaned dataframe
    
    Examples
    --------

    >>> remove_spl_chars_in_columns(df, spl_chars_excepted=['_'])        
    """
    
    invalid_characters = set(string.punctuation)
    df_columns = df.columns.to_list()

    new_columns = []
    
    for spl_char in spl_chars_excepted:
        invalid_characters.remove(spl_char)
    
    for column in df_columns:
        for char in invalid_characters:
            column = column.replace(char, '')
        if column.endswith('_'):
            column = column[:-1]
        new_columns.append(column)
    df.columns = new_columns
    return df  
    