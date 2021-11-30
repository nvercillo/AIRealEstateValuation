from enum import Enum
from inspect import Attribute
from posixpath import join
import sys

sys.path.insert(0, "..")  # import parent folder
from utils.abstract import AbstractBaseClass, abstractmethod


class Attributes:
    def __init__(self, attributes: None) -> None:
        self.attributes = attributes

    def __str__(self) -> str:

        if type(self.attributes) == list:
            res = self._convert_attributes_to_list()
        elif self.attributes is None or self.attributes == "*":
            res = "*"
        else:
            res = f"`{self.attributes}`"
        return res

    def _to_list(self):
        if type(self.attributes) == list:
            res = self.attributes
        elif self.attributes is None or self.attributes == "*":
            res = "*"
        else:
            res = [self.attributes]

        return res

    def _convert_attributes_to_list(self):
        res = ""
        c = self.attributes
        for i, e in enumerate(c):
            if isinstance(e, list) and not isinstance(e, str):
                for j in range(len(e)):
                    res += "`"
                    ele = e[j]
                    res += str(ele)
                    res += "`"
                    if j != len(e) - 1:
                        res += ", "
            else:
                res += f" {e} "
                if i != len(c) - 1:
                    res += ", "

        return res


class AttributeValue:
    def __init__(self, value):
        self.val = value
        self._type = type(value)

        assert self._type not in [list, dict, type(None)], "INVALID ATTRIBUTE VALUE"

    def isnumeric(self):
        return self._type not in [str]

    def __str__(self) -> str:
        if self.isnumeric():
            return f"{self.val}"
        else:
            return f'"{self.val}"'


class Operator:
    LOGICAL_OPERATORS = set(
        {
            "ALL",
            "AND",
            "ANY",
            "BETWEEN",
            "EXISTS",
            "IN",
            "LIKE",
            "NOT",
            "OR",
            "SOME",
        }
    )

    ARITHIMETIC_OPERATORS = set({"+", "-", "*", "/", "%"})

    BITWISE_OPERATORS = set({"&", "|", "^"})

    COMPARISON_OPERATORS = set({"=", ">", "<", ">=", "<=", "<>"})

    def __init__(self, operator: str) -> None:
        self.operator = operator.upper()

        assert operator in set().union(
            self.LOGICAL_OPERATORS,
            self.ARITHIMETIC_OPERATORS,
            self.BITWISE_OPERATORS,
            self.COMPARISON_OPERATORS,
        ), f'INVALID OPERATOR: "{operator}" given'

    def __str__(self) -> str:
        return str(self.operator)


class Filter:
    def __init__(
        self, attribute_name: Attributes, operator: Operator, attribute_val
    ) -> None:

        self.attribute_name = attribute_name
        self.operator = operator
        self.attribute_val = AttributeValue(attribute_val)

    def __str__(self) -> str:
        res = f"`{self.attribute_name}` {self.operator} "

        if type(self.attribute_name) == list:
            res += self._convert_attr_list()
        else:
            res += f"`{self.attribute_val}`"

        res += " "
        return res

    def _convert_attr_list(self):
        res = ""
        c = self.attribute_val
        for e in c:
            if isinstance(e, list) and not isinstance(e, str):
                res += "("
                for j in range(len(e)):
                    ele = e[j]
                    res += str(ele)
                    if j != len(e) - 1:
                        res += ", "
                res += ")"

            else:
                res += f" {e} "

        return res

    def _get_class(self):
        return "FITLER"

    def __str__(self) -> str:
        return f"{self.attribute_name} {self.operator} {self.attribute_val}"

    def __rer__(self) -> str:
        return self.__str__()


class JoinCondition:
    class JoinType(Enum):
        LEFT = "LEFT"
        RIGHT = "RIGHT"
        INNER = "INNER"
        OUTTER = "OUTTER"
        PLAIN = ""

    def __init__(
        self,
        obj1,
        obj2,
        join_on_1: Attribute,
        join_on_2: Attribute,
        join_operator: Operator,
        join_type: JoinType = JoinType.PLAIN,
    ) -> None:

        self.obj1 = obj1
        self.obj2 = obj2
        self.join_on_1 = join_on_1
        self.join_on_2 = join_on_2
        self.join_operator = join_operator
        self.join_type = join_type

    def __str__(self) -> str:
        print(
            f"SDSDFSDFSDF   {self.obj1.__tablename__}\n\n ",
        )
        return (
            f"{self.join_type.value} JOIN {self.obj2.__tablename__} ON "
            + f"{self.obj1.__tablename__}.{str(self.join_on_1)} "
            + f"{self.join_operator} {self.obj2.__tablename__}.{str(self.join_on_2)}"
        )


class SQLObject(AbstractBaseClass, Filter, Attributes):
    pass
