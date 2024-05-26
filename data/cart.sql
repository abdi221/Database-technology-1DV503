USE book_store;

CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userid INT NOT NULL,
    isbn CHAR(10) NOT NULL,
    qty INT NOT NULL,
    UNIQUE (userid, isbn),
    FOREIGN KEY (userid) REFERENCES members(userid),
    FOREIGN KEY (isbn) REFERENCES books(isbn)
);
