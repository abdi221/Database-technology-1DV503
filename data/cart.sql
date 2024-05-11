USE book_store;

CREATE TABLE cart (
    userid INT NOT NULL,
    isbn CHAR(10) NOT NULL,
    qty INT NOT NULL,
    PRIMARY KEY (userid, isbn),
    FOREIGN KEY (userid) REFERENCES members(userid),
    FOREIGN KEY (isbn) REFERENCES books(isbn)
);
