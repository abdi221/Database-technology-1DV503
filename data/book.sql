USE book_store;

CREATE TABLE books (
    isbn CHAR(10) PRIMARY KEY,
    author VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    price FLOAT NOT NULL,
    subject VARCHAR(100) NOT NULL
);