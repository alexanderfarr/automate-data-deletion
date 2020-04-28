CREATE TABLE privacydb (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    timestamp TIME,
    adcolony JSON NOT NULL,
    asl JSON NOT NULL,
    bestbuy JSON NOT NULL,
    chipotle JSON NOT NULL,
    petco JSON NOT NULL,
    pipl JSON NOT NULL,
    email_acxiom JSON NOT NULL,
    email_infutor JSON NOT NULL,
    email_advantagesolutions JSON NOT NULL,
    email_alc JSON NOT NULL,
    email_epsilon JSON NOT NULL,
    databreach JSON NOT NULL
);
