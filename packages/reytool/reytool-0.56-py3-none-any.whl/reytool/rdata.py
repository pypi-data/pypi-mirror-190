# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's directory type
"""


from typing import Any, List, Tuple, Dict, Iterable, Iterator, Literal, Optional, Union, Type
from sqlalchemy.engine.cursor import LegacyCursorResult
from pandas import DataFrame, ExcelWriter

from .rbasic import is_iterable, check_least_one
from .rtime import time_to_str


class RDict(object):
    """
    Rey's directory type.

    Methods
    -------
    attribute : parms, default
    syntax : [index | slice], for, in/ not in
    enter parameter : len
    symbol : +(l/ r), -(l/ r), &(l/ r), +=, -=, &=
    function : items, keys, values, get, pop
    """
    
    def __init__(self, *dicts: Dict, default: Union[Any, Literal["error"]] = "error") -> None:
        """
        Set directory attribute.

        Parameters
        ----------
        dicts : directory
        default : Default method when index fails.
            - Any : Return this value.
            - Literal['error'] : Throw error.
        """

        data = {}
        for _dict in dicts:
            data.update(_dict)
        self.data = data
        self.default = default
    
    def __call__(self, *keys: Any) -> Any:
        """
        Indexes key value pair.
        """

        if keys == ():
            ret = self.data
        else:
            ret = {key: self.data[key] for key in keys}
        return ret

    def __getattr__(self, key: Any) -> Any:
        """
        Index value.
        """

        value = self.data[key]
        return value

    def __getitem__(self, indexes: Union[Any, Tuple]) -> Any:
        """
        Batch indexing directory values.
        """

        if type(indexes) == tuple:
            if self.default == "error":
                vals = [self.data[key] for key in indexes]
            else:
                vals = [self.data.get(key, self.default) for key in indexes]
        else:
            if self.default == "error":
                vals = self.data[indexes]
            else:
                vals = self.data.get(indexes, self.default)
        return vals

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Create or modify key value pair.
        """

        self.data[key] = value
    
    def __iter__(self) -> Iterator:
        """
        Return iterable directory keys.
        """

        return self.keys

    def __contains__(self, key: Any) -> bool:
        """
        Judge contain.
        """

        judge = key in self.data
        return judge

    def __len__(self) -> int:
        """
        Return directory length.
        """
        return self.len

    def __add__(self, parms: Dict) -> Dict:
        """
        Union directory.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**self.data, **parms}
        return parms
    
    def __radd__(self, parms: Dict) -> Dict:
        """
        Union directory right.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**parms, **self.data}
        return parms

    def __iadd__(self, parms: Dict) -> Any:
        """
        Union directory and definition.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        parms = {**self.data, **parms}
        self.data = parms
        return self

    def __sub__(self, parms: Iterable) -> Dict:
        """
        Difference directory.
        """
        
        main_set = set(self.data)
        sub_set = set(parms)
        diff_set = main_set - sub_set
        parms = {key: self.data[key] for key in diff_set}
        return parms

    def __rsub__(self, parms: Dict) -> Dict:
        """
        Difference directory right.
        """

        main_set = set(parms)
        sub_set = set(self.data)
        diff_set = main_set - sub_set
        parms = {key: parms[key] for key in diff_set}
        return parms

    def __isub__(self, parms: Dict) -> Any:
        """
        Difference directory and definition.
        """

        main_set = set(self.data)
        sub_set = set(parms)
        diff_set = main_set - sub_set
        parms = {key: self.data[key] for key in diff_set}
        self.data = parms
        return self

    def __and__(self, parms: Dict) -> Dict:
        """
        Intersection directory.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(self.data)
        sub_set = set(parms)
        inte_set = main_set & sub_set
        parms = {key: self.data[key] for key in inte_set}
        return parms

    def __rand__(self, parms: Dict) -> Dict:
        """
        Intersection directory right.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(parms)
        sub_set = set(self.data)
        inte_set = main_set & sub_set
        parms = {key: parms[key] for key in inte_set}
        return parms

    def __iand__(self, parms: Dict) -> Dict:
        """
        Intersection directory and definition.
        """

        if is_iterable(parms, [str, bytes, dict]):
            parms = {key: val for parm in parms for key, val in parm.items()}
        main_set = set(self.data)
        sub_set = set(parms)
        inte_set = main_set & sub_set
        parms = {key: self.data[key] for key in inte_set}
        self.data = parms
        return self

    def items(self) -> Iterator:
        """
        Get directory all keys and values.
        """

        items = self.data.items()
        return items

    def keys(self) -> Iterator:
        """
        Get directory all keys.
        """

        keys = self.data.keys()
        return keys

    def values(self) -> Iterator:
        """
        Get directory all values.
        """

        values = self.data.values()
        return values

    def get(self, keys: Union[Any, Iterable], default: Optional[Any] = None) -> Dict:
        """
        Batch get directory values.
        """

        if default == None and self.default != "error":
            default = self.default
        if is_iterable(keys):
            vals = [self.data.get(key, default) for key in keys]
        else:
            vals = self.data.get(keys, default)
        return vals

    def pop(self, keys: Union[Any, Iterable], default: Optional[Any] = None) -> Dict:
        """
        Batch pop directory values.
        """

        if default == None and self.default != "error":
            default = self.default
        if is_iterable(keys):
            vals = [self.data.pop(key, default) for key in keys]
        else:
            vals = self.data.pop(keys, default)
        return vals

def to_table(data: Union[LegacyCursorResult, Iterable[Dict], DataFrame], fields: Optional[Iterable] = None) -> List[Dict]:
    """
    Fetch data to table in List[Dict] format.

    Parameters
    ----------
    data : SQL result or Iterable[Dict] or DataFrame object.
    fields : Table fields.
        - None : Use data fields.
        - Iterable : Use values in Iterable.
    
    Returns
    -------
    Table in List[Dict] format.
    """

    data_type = type(data)
    if data_type == LegacyCursorResult:
        if fields == None:
            fields = data.keys()
        table = [dict(zip(fields, [time_to_str(val) for val in row])) for row in data]
    elif data_type == DataFrame:
        table = data.to_dict("records")
    else:
        data_fields_len = max([len(row) for row in data])
        if fields == None:
            data = [list(row) + [None] * (data_fields_len - len(row)) for row in data]
            field_range = range(data_fields_len)
            table = [dict(zip(field_range, [time_to_str(val) for val in row])) for row in data]
        else:
            field_len = len(fields)
            if data_fields_len > field_len:
                fields += list(range(data_fields_len - field_len))
            data = [list(row) + [None] * (field_len - len(row)) for row in data]
            table = [dict(zip(fields, [time_to_str(val) for val in row])) for row in data]
    return table

def to_df(data: Union[LegacyCursorResult, Iterable[Dict]], fields: Optional[Iterable] = None) -> DataFrame:
    """
    Fetch data to table of DataFrame object.

    Parameters
    ----------
    data : SQL result or Iterable[Dict].
    fields : Table fields.
        - None : Use data fields.
        - Iterable : Use values in Iterable.
    
    Returns
    -------
    Table of DataFrame object.
    """

    data_type = type(data)
    if data_type == LegacyCursorResult:
        if fields == None:
            fields = data.keys()
        else:
            fields_len = len(data.keys())
            fields = fields[:fields_len]
        df = DataFrame(data, columns=fields)
    else:
        if fields == None:
            df = DataFrame(data)
        else:
            data_fields_len = max([len(row) for row in data])
            field_len = len(fields)
            if data_fields_len > field_len:
                fields += list(range(data_fields_len - field_len))
            data = [list(row) + [None] * (field_len - len(row)) for row in data]
            df = DataFrame(data, columns=fields)
    return df

def to_sql(data: Union[LegacyCursorResult, Iterable[Dict], DataFrame], fields: Optional[Iterable] = None) -> str:
    """
    Fetch data to SQL syntax.
    
    Parameters
    ----------
    data : SQL result or Iterable[Dict] or DataFrame object.
    fields : Table fields.
        - None : Use data fields.
        - Iterable : Use values in Iterable.
    
    Returns
    -------
    SQL syntax.
    """

    data_type = type(data)
    if data_type == LegacyCursorResult:
        if fields == None:
            fields = data.keys()
        sqls = [[repr(time_to_str(val)) if val else "NULL" for val in row] for row in data]
    else:
        if data_type == DataFrame:
            data = data.to_dict("records")
        if fields == None:
            data_fields_len = max([len(row) for row in data])
            fields = ["field_%d" % i for i in range(data_fields_len)]
        sqls = [[repr(time_to_str(val)) if val else "NULL" for val in row] + ["NULL"] * (data_fields_len - len(row)) for row in data]
    sqls[0] = "SELECT " + ",".join(["%s AS `%s`" % (val, fie) for val, fie in list(zip(sqls[0], fields))])
    sqls[1:] = ["SELECT " + ",".join(sql) for sql in sqls[1:]]
    sql = " UNION ALL ".join(sqls)
    return sql

def to_csv(data: Union[LegacyCursorResult, Iterable[Dict], DataFrame], path: str = "table.csv", fields: Optional[Iterable] = None) -> None:
    """
    Fetch data to save csv format file.
    
    Parameters
    ----------
    data : SQL result or Iterable[Dict] or DataFrame object.
    path : File save path.
    fields : Table fields.
        - None : Use data fields.
        - Iterable : Use values in Iterable.
    """

    data_df = to_df(data, fields)
    data_df.to_csv(path, mode="a")

def to_excel(
    data: Union[LegacyCursorResult, Iterable[Dict], DataFrame],
    path: str = "table.xlsx",
    group_field: Optional[str] = None,
    sheets_set: Dict[Union[str, int], Dict[Literal["name", "index", "filter"], Union[str, int, List[str]]]] = {}
) -> Tuple[Tuple[str, DataFrame], ...]:
    """
    Fetch data to save excel format file and return sheet name and sheet data.

    Parameters
    ----------
    data : SQL result or Iterable[Dict] or DataFrame object.
    path : File save path.
    group_field : Group filed.
    sheets_set : Set sheet new name and sort sheet and filter sheet fields,
        key is old name or index, value is set parameters.
        - Parameter 'name' : Set sheet new name.
        - Parameter 'index' : Sort sheet.
        - Parameter 'filter' : Filter sheet fields.

    Returns
    -------
    Sheet name and sheet data.
    """

    data_type = type(data)
    if data_type != DataFrame:
        data_df = to_df(data)
    else:
        data_df = data
    if group_field == None:
        data_group = (("Sheet1", data_df),)
    else:
        data_group = data_df.groupby(group_field)
    sheets_table_before = []
    sheets_table_after = []
    for index, sheet_table in enumerate(data_group):
        sheet_name, sheet_df = sheet_table
        if group_field != None:
                del sheet_df[group_field]
        if sheet_name in sheets_set:
            sheet_set = sheets_set[sheet_name]
        elif index in sheets_set:
            sheet_set = sheets_set[index]
        else:
            sheets_table_after.append((sheet_name, sheet_df))
            continue
        if "name" in sheet_set:
            sheet_name = sheet_set["name"]
        if "filter" in sheet_set:
            sheet_df = sheet_df[sheet_set["filter"]]
        if "index" in sheet_set:
            sheets_table_before.append((sheet_set["index"], (sheet_name, sheet_df)))
        else:
            sheets_table_after.append((sheet_name, sheet_df))
    sort_func = lambda item: item[0]
    sheets_table_before.sort(key=sort_func)
    sheets_table = [sheet_table for sheet_index, sheet_table in sheets_table_before] + sheets_table_after
    excel = ExcelWriter(path)
    for sheet_name, sheet_df in sheets_table:
        sheet_df.to_excel(excel, sheet_name, index=False)
    excel.close()
    return sheets_table

def count(
    data: Any,
    count_value: Dict = {"size": 0, "total": 0, "types": {}},
    surface: bool = True
) -> Dict[Literal["size", "total", "types"], Union[int, Dict[Type, int]]]:
    """
    Count data element.

    Parameters
    ----------
    data : Data.
    count_value : Cumulative Count.
    surface : Whether is surface recursion.
    
    Returns
    -------
    Count data.
    """

    data_type = type(data)
    count_value["total"] += 1
    count_value["types"][data_type] = count_value["types"].get(data_type, 0) + 1
    if data_type == dict:
        for element in data.values():
            count(element, count_value, False)
    elif is_iterable(data):
        for element in data:
            count(element, count_value, False)
    else:
        count_value["size"] = count_value["size"] + 1
    if surface:
        sorted_func = lambda key: count_value["types"][key]
        sorted_key = sorted(count_value["types"], key=sorted_func, reverse=True)
        count_value["types"] = {key: count_value["types"][key] for key in sorted_key}
        return count_value

def flatten(data: Any, flattern_data: List = []) -> List:
    """
    Flatten data.
    """

    data_type = type(data)
    if data_type == dict:
        for element in data.values():
            _ = flatten(element, flattern_data)
    elif is_iterable(data):
        for element in data:
            _ = flatten(element, flattern_data)
    else:
        flattern_data.append(data)
    return flattern_data

def split(data: Iterable, bin_size: Optional[int] = None, share: int = 2) -> List[List]:
    """
    Split data into multiple data.
    """

    check_least_one(bin_size, share)

    data = list(data)
    data_len = len(data)
    datas = []
    datas_len = 0
    if bin_size == None:
        average = data_len / share
        for n in range(share):
            bin_size = int(average * (n + 1)) - int(average * n)
            _data = data[datas_len:datas_len + bin_size]
            datas.append(_data)
            datas_len += bin_size
    else:
        while True:
            _data = data[datas_len:datas_len + bin_size]
            datas.append(_data)
            datas_len += bin_size
            if datas_len > data_len:
                break
    return datas