from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_root():
    """Test the root endpoint"""

    response = client.get("/")

    assert response.status_code == 200


def test_get_books():
    """
    Test the /books endpoint.
    Ensures it returns a list of books with status code 200.
    Checks that the first book has the expected title.
    """
    response = client.get("/books")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["title"] == "Satanás"


def test_get_book_by_id():
    """
    Test the /books/{book_id} endpoint.
    Fetches book with ID 1 and verifies its book_id and author.
    """
    response = client.get("/books/1")

    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == 1
    assert data["author"] == "Mario Mendoza"


def test_get_book_not_found():
    """
    Test the /books/{book_id} endpoint with a non-existent book.
    Checks that the error message is returned.
    """
    response = client.get("/books/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book with ID 999 not found"


def test_create_book():
    """
    Test the POST /books endpoint.
    Creates a new book and verifies the returned data matches the input.
    """
    new_book = {"title": "Delirio", "author": "Laura Restrepo", "year": 2004}

    response = client.post("/books", json=new_book)

    assert response.status_code == 201
    assert response.json()["book_id"] == 5
    assert response.json()["title"] == "Delirio"


def test_update_book():
    """
    Test the PUT /books/{book_id} endpoint.
    Updates the title of book with ID 1 and verifies the change.
    """

    update_data = {"title": "La melancolía de los feos"}
    response = client.put("/books/1", json=update_data)

    assert response.status_code == 200
    assert response.json()["title"] == "La melancolía de los feos"


def test_delete_book():
    """
    Test the DELETE /books/{book_id} endpoint.
    Deletes a book and ensures it no longer exists in the list.
    """
    response = client.delete("/books/5")  # Book ID created in test_create_book

    assert response.status_code == 204

    # Verify that the book was actually deleted
    get_response = client.get("/books/5")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Book with ID 5 not found"
