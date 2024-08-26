# from typing import Literal

# import jmespath as jp
# from malevich.square import Context, Docs, condition, scheme

# Operator = Literal["==", "!=", ">", "<", ">=", "<=", "in", "not in"]
# Keyword = Literal["true", "false", "and", "or"]
# Condition = tuple[str, Operator, str]


# @scheme()
# class DocFilters:
#     filter: list

# @condition()
# def docfilter(documents: Docs, context: Context[DocFilters]) -> bool:
#     """Compares documents using JMESPath expressions and operators:

#     Operators:
#     - `==`: equals
#     - `!=`: not equals
#     - `>`: greater than
#     - `<`: less than
#     - `>=`: greater or equal
#     - `<=`: less or equal
#     - `in`: in list
#     - `not in`: not in list

#     One can combine expressions using logical operators: `and`, `or`.

#     ## Input:
#         A list of documents.

#     ## Configuration:
#         - `filter`: list, required.
#             A list of JMESPath expressions and operators to compare documents.
#             Each expression is a dictionary with a single key:
#             - `true`: [str, Operator, str], required.
#                 A JMESPath expression, an operator, and a constant value to compare.
#             - `false`: [str, Operator, str], required.
#                 A JMESPath expression, an operator, and a constant value to compare.
#             - `and`: list, required.
#                 A list of expressions to combine with the logical `and` operator.
#             - `or`: list, required.
#                 A list of expressions to combine with the logical `or` operator.

#             The expressions are evaluated in the order they are given. Expressions
#             are combined using the logical `and` operator.

#             For example:
#             ```json
#             [
#                 {"true": ["$.author", "==", "Alex"]},
#                 {"false": ["$.price", ">", 10]},
#                 {"or": [{"true": ["$.author", "==", "Alex"]}, {"true": ["$.price", ">", 10]}]},
#                 {"and": [{"true": ["$.author", "==", "Alex"]}, {"false": ["$.price", ">", 10]}]}
#             ]
#             ```
#     """
#     data = (
#         documents[0].dict()
#         if len(documents) == 1
#         else [document.dict() for document in documents]
#     )

#     def eval_recursive(filter: dict) -> bool:
#         for key, value in filter.items():
#             if key == "true" or key == "false":
#                 should = key == "true"
#                 query, operator, cvalue = value
#                 matches = jp.search(query, data)
#                 if not isinstance(matches, list):
#                     matches = [matches]

#                 for match in matches:
#                     if isinstance(match, dict):
#                         raise ValueError(
#                             "JMESPath expression should return a value or a list of values "
#                             f"but {query} returned a dictionary {match}. "
#                             f"Cannot evaluate {query} {operator} {cvalue}."
#                         )
#                     elif isinstance(match, list):
#                         if not all([eval(f"{m} {operator} {cvalue}") == should for m in match]):
#                             return False
#                     else:
#                         if eval(f"{match} {operator} {cvalue}") != should:
#                             return False

#             elif key == "and":
#                 return all([eval_recursive(v) for v in value])
#             elif key == "or":
#                 return any([eval_recursive(v) for v in value])
#             else:
#                 raise ValueError(f"Unknown keyword {key}.")
#         return True

#     return all([eval_recursive(filter) for filter in context.app_cfg.filter])
