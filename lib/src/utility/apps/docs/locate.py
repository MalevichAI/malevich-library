import jmespath as jp
from malevich.square import Context, Doc, Docs, processor, scheme


@scheme()
class JMESPathExpression:
    expression: str

@processor()
def search(document: Doc, context: Context[JMESPathExpression]) -> Docs:
    """Selects parts from documents using JMESPath and constructs a new document

    Explore JMESPath: https://jmespath.org/tutorial.html

    ## Input:
        An arbitrary JSON document.

    ## Output:
        A document containing results of queries. See Configuration.

    ## Configuration:
        - `expression`: str, required.
            A JMESPath expression to extract data from the document.
            See https://jmespath.org/tutorial.html

    -----
    """
    return jp.search(context.app_cfg.expression, document.dict())


@processor()
def insert(source: Doc, target: Docs, context: Context) -> Docs:
    """Modifies target document inserting results of JMESPath queries from source

    Explore JMESPath: https://jmespath.org/tutorial.html

    For example, a target document can be:

    ```json
    {
        "author": "Alex"
        "first_book": "::$.book[0]"
    }
    ```
    and a source document is given as

    ```json
    {
        "book": [
            {
                "title": "The Book",
                "price": 10
            },
            {
                "title": "The Second Book",
                "price": 15
            }
        ]
    }```

    The processor will detect a special marker "::" in the beginning
    of a string value and execute JMESPath query that succeeds the marker.
    The result of the query will be inserted instead of the value.

    So the output will be:
    ```json
    {
        "author": "Alex"
        "first_book": {
            "title": "The Book",
            "price": 10
        }
    }
    ``

    ## Input:
        An arbitrary source document and a number of arbitrary target documents.
        Each of target documents might have fields, which values are 
        JMESPath expressions.

    ## Output:
        The same as target documents, but each value, that contained JMESPath query, is
        substited with a result of the query.

    ## Configuration:
        - `query_marker`: str, default "::".
            A marker that denotes a query.

    -----
    """
    query_marker = context.app_cfg.get('query_marker', '::')
    def recursive_replace(value: list | dict | str | int | float | bool):
        if isinstance(value, str) and value.startswith(query_marker):
            return jp.search(value[len(query_marker):], source)
        if isinstance(value, dict):
            return {key: recursive_replace(val) for key, val in value.items()}
        if isinstance(value, list):
            return [recursive_replace(val) for val in value]
        return value

    return [
        recursive_replace(t)
        for t in target
    ]

