r"""Module with the :class:`SQLContainer <pandemy.SQLContainer>` class.

The :class:`SQLContainer <pandemy.SQLContainer>` is a storage container for the SQL statements
used by a :class:`DatabaseManager <pandemy.DatabaseManager>` of an application.
It also provides the :meth:`replace_placeholders() <pandemy.SQLContainer.replace_placeholders>`
method for pre-processing of placeholders in a SQL statement before it is executed on the database.
"""

# ===============================================================
# Imports
# ===============================================================

# Standard Library
from collections import namedtuple
import logging
from typing import Sequence, Tuple, Union

# Third Party

# Local
import pandemy

# ===============================================================
# Set Logger
# ===============================================================

# Initiate the module logger
# Handlers and formatters will be inherited from the root logger
logger = logging.getLogger(__name__)


# ===============================================================
# Classes
# ===============================================================


class Placeholder:
    r"""Container of placeholders and their replacement values for parametrized SQL statements.

    The :class:`Placeholder` handles placeholders and their replacement values when building
    parametrized SQL statements. A SQL placeholder is always prefixed by a colon (*:*) e.g.
    ``:myplaceholder`` in the SQL statement. :class:`Placeholder` is used as input to the
    :meth:`SQLContainer.replace_placeholders` method.

    Parameters
    ----------
    placeholder : str
        The placeholder to replace in the SQL statement. E.g. ``':myplaceholder'``.

    replacements : str or int or float or sequence of str or int or float
        The value(s) to replace `placeholder` with.

    return_new_placeholders : bool, default True
        If `replacements` should be mapped to new placeholders in the `params` return value
        of the :meth:`SQLContainer.replace_placeholders` method.

    See Also
    --------
    * :class:`SQLContainer` : A container of SQL statements.

    Examples
    --------
    Creating a :class:`Placeholder` and accessing its attributes.

    >>> p1 = pandemy.Placeholder(
    ...     placeholder=':itemid',
    ...     replacements=[1, 2, 3]
    ... )
    >>> p1
    Placeholder(placeholder=':itemid', replacements=[1, 2, 3], return_new_placeholders=True)
    >>> p2 = pandemy.Placeholder(
    ...     placeholder=':itemname',
    ...     replacements='A%',
    ...     return_new_placeholders=False
    ... )
    >>> p2
    Placeholder(placeholder=':itemname', replacements='A%', return_new_placeholders=False)
    >>> p1.placeholder
    ':itemid'
    >>> p2.replacements
    'A%'
    >>> p2.return_new_placeholders
    False
    """

    __slots__ = ('placeholder', 'replacements', 'return_new_placeholders')

    def __init__(
        self,
        placeholder: str,
        replacements: Union[str, int, float, Sequence[Union[str, int, float]]],
        return_new_placeholders: bool = True
    ) -> None:
        self.placeholder = placeholder
        self.replacements = replacements
        self.return_new_placeholders = return_new_placeholders

    def __str__(self) -> str:
        r"""String representation of the object."""

        return self.__repr__()

    def __repr__(self) -> str:
        r"""Debug representation of the object."""

        return (
            f'Placeholder(placeholder={self.placeholder!r}, replacements={self.replacements!r}, '
            f'return_new_placeholders={self.return_new_placeholders!r})'
        )


class SQLContainer:
    r"""Base class of a container of SQL statements.

    Each SQL-dialect will subclass from :class:`SQLContainer` and :class:`SQLContainer`
    is never used on its own, but merely provides methods to work with SQL statements.

    Each SQL statement is implemented as a class variable.
    """

    @staticmethod
    def validate_class_variables(cls: object, parent_cls: object, type_validation: str) -> None:
        r"""
        Validate that a subclass has implemented the class variables
        specified on its parent class.

        Intended to be used in special method `__init_subclass__`.

        Parameters
        ----------
        cls : object
            The class being validated.

        parent_cls : object
            The parent class that `cls` inherits from.

        type_validation : {'isinstance', 'type'}
            How to validate the type of the class variables.
            'type' should be used if a class is assigned to class variables and 'isinstance'
            in other cases. You cannot combine class variables with classes assigned and
            class variables with other types assigned e.g. str or int.

        Raises
        ------
        AttributeError
            If the parent class is missing annotated class variables.

        NotImplementedError
            If a class variable is not implemented.

        TypeError
            If a class variable is not of the type specified in the parent class.

        pandemy.InvalidInputError
            If a value other than 'isinstance' or 'type' is given to the `type_validation` parameter.
        """

        # Get the annotated class variables of the parent class
        class_vars = parent_cls.__annotations__

        for var, dtype in class_vars.items():
            logger.debug(f'var = {var}, dtype = {dtype}')

            # Check that the class variable exists
            if (value := getattr(cls, var, None)) is None:
                raise NotImplementedError(f'Class {cls.__name__} has not implemented the requried variable: {var}')

            # Check for correct data type
            if type_validation == 'isinstance':
                is_valid = isinstance(value, dtype)
            elif type_validation == 'type':
                is_valid = type(value) == type(dtype)
            else:
                raise pandemy.InvalidInputError(f'type_validation = {type_validation}. '
                                                "Expected 'isinstance', or 'type'")

            if not is_valid:
                raise TypeError(f'Class variable "{var}"" of class {cls.__name__} '
                                f'is of type {type(value)} ({value}). Expected {dtype}.')

    @staticmethod
    def replace_placeholders(stmt: str, placeholders: Union[Placeholder, Sequence[Placeholder]]) -> Tuple[str, dict]:
        r"""Replace placeholders in a SQL statement.

        Replace the placeholders in the SQL statement `stmt` that are specified by the `placeholder` parameter of a
        :class:`Placeholder` instance, supplied to the `placeholders` parameter, with their respective replacements
        in the `replacements` parameter of a :class:`Placeholder`. A placeholder in a SQL statement is always prefixed
        with a colon (*:*) e.g. ``:myplaceholder``.

        The main purpose of the method is to handle parametrized IN statements with a variable number of values.
        A single placeholder can be placed in the IN statement and later be replaced by new placeholders
        that match the length of the `replacements` parameter of a :class:`Placeholder` instance.

        The return values `stmt` and `params` can be used as input to the
        :meth:`execute() <pandemy.DatabaseManager.execute>` and
        :meth:`load_table() <pandemy.DatabaseManager.load_table>` methods
        of a :class:`DatabaseManager <pandemy.DatabaseManager>`.

        Parameters
        ----------
        stmt : str
            The SQL statement in which to replace placeholders.

        placeholders : Placeholder or sequence of Placeholder
            The replacements for each placeholder in `stmt`.

        Returns
        -------
        stmt : str
            The SQL statement after placeholders have been replaced.

        params : dict
            The new placeholders and their replacement values from the `replacements` parameter
            of a :class:`Placeholder`. Entries to `params` are only written if the parameter
            `return_new_placeholders` in a :class:`Placeholder` is set to ``True``.

            Example of a return value: ``{'v0': 'value1', 'v1': 3.14}``. The new placeholders
            are always named *v* followed by a sequential number denoting the order (zero-indexed) in which the new
            placeholder occurs in the returned SQL statement `stmt`.

            The keys of `params` never contain the prefix colon (*:*) that is used in the SQL statement to identify
            a placeholder.

        Raises
        ------
        pandemy.InvalidInputError
            If the replacement values in a :class:`Placeholder` are not valid.

        See Also
        --------
        * :class:`Placeholder` : Container of a placeholder and its replacement values.

        * :meth:`DatabaseManager.execute() <pandemy.DatabaseManager.execute>` : Execute a SQL statement.

        * :meth:`DatabaseManager.load_table() <pandemy.DatabaseManager.load_table>` : Load a SQL table into a :class:`pandas.DataFrame`.

        Examples
        --------
        Replace the placeholders of a SQL statement (``stmt``) with new placeholders and return a mapping of
        the new placeholders to the desired values (``params``).

        .. doctest::

           >>> stmt = 'SELECT * FROM Item WHERE ItemId IN (:itemid);'
           >>> p1 = pandemy.Placeholder(placeholder=':itemid',
           ...                          replacements=[1, 2, 3],
           ...                          return_new_placeholders=True)
           >>> stmt, params = pandemy.SQLContainer.replace_placeholders(stmt=stmt, placeholders=p1)
           >>> stmt
           'SELECT * FROM Item WHERE ItemId IN (:v0, :v1, :v2);'
           >>> params
           {'v0': 1, 'v1': 2, 'v2': 3}

        If the SQL statement contains more than one placeholder a sequence of
        :class:`Placeholder <pandemy.Placeholder>` can be passed.

        .. doctest::

           >>> stmt = ('SELECT * FROM Item '
           ...         'WHERE ItemId IN (:itemid) AND Description LIKE :desc '
           ...         'ORDER BY :orderby;')
           ...
           >>> p1 = pandemy.Placeholder(placeholder=':itemid',
           ...                          replacements=[1, 2, 3],
           ...                          return_new_placeholders=True)
           ...
           >>> p2 = pandemy.Placeholder(placeholder=':desc',
           ...                          replacements='A%',
           ...                          return_new_placeholders=True)
           ...
           >>> p3 = pandemy.Placeholder(placeholder=':orderby',
           ...                          replacements='ItemName DESC',
           ...                          return_new_placeholders=False)
           ...
           >>> stmt, params = pandemy.SQLContainer.replace_placeholders(stmt=stmt,
           ...                                                          placeholders=[p1, p2, p3])
           >>> stmt
           'SELECT * FROM Item WHERE ItemId IN (:v0, :v1, :v2) AND Description LIKE :v3 ORDER BY ItemName DESC;'
           >>> params
           {'v0': 1, 'v1': 2, 'v2': 3, 'v3': 'A%'}


        .. note::

           The replacement for the *':orderby'* placeholder is not part of the returned ``params``
           dictionary because ``return_new_placeholders=False`` for ``p3``.


        .. warning::

           Replacing *':orderby'* by an arbitrary value that is not a placeholder is not safe against
           SQL injection attacks the way placeholders are and is therefore discouraged. The feature is
           there if it is needed, but be aware of its security limitations.
        """

        def is_valid_replacement_value(value: Union[str, int, float, bool, None], raises: bool = False) -> bool:
            r"""Helper function to validate values of the replacements.

            Parameters
            ----------
            value : str, int or float
                The value to validate.

            raises : bool, default False
                If True pandemy.InvalidInputError will be raised if `value` is not valid.
                If False the function will return False instead of raising an exception.

            Returns
            -------
            bool
                True if the value is valid and False otherwise.

            Raises
            ------
            pandemy.InvalidInputError
                If the replacement values in a Placeholder are not valid and `raises` is True.
            """

            if (isinstance(value, str) or
                isinstance(value, int) or
                isinstance(value, float) or
                isinstance(value, bool) or
                value is None):
                return True
            else:
                if raises:
                    raise pandemy.InvalidInputError('values in replacements must be: str, int, float, bool or None.'
                                                    f'Got {value} ({type(value)})', data=value)
                else:
                    return False

        # Stores new placeholders and their mapped values
        params = dict()

        # Counter of number of new placeholders added. Makes sure each new placeholder is unique
        counter = 0

        # Convert to list if a single Placeholder object is passed
        if isinstance(placeholders, Placeholder):
            placeholders = [placeholders]

        for placeholder in placeholders:
            if is_valid_replacement_value(placeholder.replacements, raises=False):

                # Build replacement string of new placeholder
                if placeholder.return_new_placeholders:
                    new_placeholder = f'v{counter}'
                    counter += 1
                    repl_str = f':{new_placeholder}'
                    params[new_placeholder] = placeholder.replacements
                else:
                    repl_str = str(placeholder.replacements)

            elif hasattr(placeholder.replacements, '__iter__'):  # list like

                repl_str = ''
                for value in placeholder.replacements:

                    # Check that we have a valid replacement value
                    is_valid_replacement_value(value, raises=True)

                    # Build replacement string of new placeholders
                    if placeholder.return_new_placeholders:
                        new_placeholder = f'v{counter}'
                        counter += 1
                        repl_str += f':{new_placeholder}, '
                        params[new_placeholder] = value
                    else:
                        repl_str += f'{value}, '

                # Remove last unwanted ', '
                repl_str = repl_str[:-2]

            else:
                raise pandemy.InvalidInputError(f'placeholder replacement values must be of type str, int, float, bool '
                                                'or a sequence of those. '
                                                f'Got {placeholder.replacements} ({type(placeholder.replacements)})')

            # Replace the placeholder with the replacement string
            stmt = stmt.replace(placeholder.placeholder, repl_str)
            logger.debug(f'stmt = {stmt}')
            logger.debug(f'params = {params}')

        return stmt, params
