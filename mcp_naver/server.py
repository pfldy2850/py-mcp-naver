# demo.py
import json
import os

import httpx
import xmltodict
from fastmcp import FastMCP

mcp = FastMCP("Naver OpenAPI", dependencies=["httpx", "xmltodict"])


NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")
api_headers = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
}

API_ENDPOINT = "https://openapi.naver.com/v1"


@mcp.tool(
    name="search_blog",
    description="Search blog posts on Naver",
)
async def search_blog(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
):
    """
    Search blog posts on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_ENDPOINT}/search/blog.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_news",
    description="Search news articles on Naver",
)
def search_news(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
):
    """
    Search news articles on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/news.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_book",
    description="Search books on Naver",
)
def search_book(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
):
    """
    Search books on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/book.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="get_book_adv",
    description="Get book information from Naver",
)
def get_book_adv(
    query: str = None,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
    d_titl: str = None,
    d_isbn: str = None,
):
    """
    Get book information from Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
        d_titl (str, optional): Title of the book.
        d_isbn (str, optional): ISBN of the book.
    """

    assert d_titl or d_isbn, "Either d_titl or d_isbn must be provided"

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/book_adv.xml",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
                "d_titl": d_titl,
                "d_isbn": d_isbn,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return json.dumps(xmltodict.parse(response.text), ensure_ascii=False)


@mcp.tool(
    name="adult_check",
    description="Check if the search term is adult content",
)
def adult_check(
    query: str,
):
    """
    Check if the search term is adult content

    Args:
        query (str): The query to check.
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/adult.json",
            params={
                "query": query,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_encyc",
    description="Search encyclopedia on Naver",
)
def search_encyc(
    query: str,
    display: int = 10,
    start: int = 1,
):
    """
    Search encyclopedia on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/encyc.json",
            params={
                "query": query,
                "display": display,
                "start": start,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_cafe_article",
    description="Search cafe articles on Naver",
)
def search_cafe_article(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
):
    """
    Search cafe articles on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/cafearticle.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_kin",
    description="Search Q&A on Naver",
)
def search_kin(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
):
    """
    Search Q&A on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/kin.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_local",
    description="Search local information on Naver",
)
def search_local(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "random",
):
    """
    Search local information on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "random".
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/local.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="fix_spelling",
    description="Correct spelling errors in a given text",
)
def fix_spelling(
    query: str,
):
    """
    Correct spelling errors in a given text

    Args:
        query (str): The text to correct.
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/errata.json",
            params={
                "query": query,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_webkr",
    description="Search web pages on Naver",
)
def search_webkr(
    query: str,
    display: int = 10,
    start: int = 1,
):
    """
    Search web pages on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/webkr.json",
            params={
                "query": query,
                "display": display,
                "start": start,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_image",
    description="Search images on Naver",
)
def search_image(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
    filter: str = "all",
):
    """
    Search images on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
        filter (str, optional): The filter for the search. Defaults to "all".
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/image",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
                "filter": filter,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_shop",
    description="Search shopping items on Naver",
)
def search_shop(
    query: str,
    display: int = 10,
    start: int = 1,
    sort: str = "sim",
    filter: str = None,
    exclude: str = None,
):
    """
    Search shopping items on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
        sort (str, optional): The sorting method. Defaults to "sim".
        filter (str, optional): The filter for the search. Defaults to None.
        exclude (str, optional): The exclude filter for the search. Defaults to None.
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/shop.json",
            params={
                "query": query,
                "display": display,
                "start": start,
                "sort": sort,
                "filter": filter,
                "exclude": exclude,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


@mcp.tool(
    name="search_doc",
    description="Search documents on Naver",
)
def search_doc(
    query: str,
    display: int = 10,
    start: int = 1,
):
    """
    Search documents on Naver

    Args:
        query (str): The query to search for.
        display (int, optional): The number of items to display. Defaults to 10.
        start (int, optional): The start index for the search. Defaults to 1.
    """

    with httpx.Client() as client:
        response = client.get(
            f"{API_ENDPOINT}/search/doc.json",
            params={
                "query": query,
                "display": display,
                "start": start,
            },
            headers=api_headers,
        )

        response.raise_for_status()  # Raise an error for bad responses

        return response.text


if __name__ == "__main__":
    mcp.run()
