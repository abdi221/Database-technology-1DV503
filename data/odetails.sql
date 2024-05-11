USE book_store;

CREATE TABLE odetails (
    ono INT NOT NULL,
    isbn CHAR(10) NOT NULL,
    qty INT NOT NULL,
    amount FLOAT NOT NULL,
    FOREIGN KEY (isbn) REFERENCES books(isbn),
    FOREIGN KEY(ono) REFERENCES orders(ono)
);