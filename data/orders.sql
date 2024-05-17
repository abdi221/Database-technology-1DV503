USE book_store;

CREATE TABLE  orders (
    ono INT AUTO_INCREMENT PRIMARY KEY,
    userid INT NOT NULL,
    created DATE NULL,
    shipAddress VARCHAR(50) NULL,
    shipCity VARCHAR(30) NULL,
    shipZip INT NULL,
    FOREIGN KEY (userid) REFERENCES members(userid)
);