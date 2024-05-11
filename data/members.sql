USE book_store;

CREATE TABLE members (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL,
    city VARCHAR(30) NOT NULL,
    zip INT NOT NULL,
    phone VARCHAR(15) NULL,
    email VARCHAR(40) NOT NULL,
    userid INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(200) NOT NULL
);