CREATE TABLE order_line (
	id SERIAL NOT NULL,
	order_id VARCHAR,
	sku VARCHAR,
	quantity INTEGER,
	PRIMARY KEY (id)
);
CREATE TABLE batch (
	id SERIAL NOT NULL,
	ref VARCHAR,
	sku VARCHAR,
	qty INTEGER,
	eta DATE,
	PRIMARY KEY (id)
);
CREATE TABLE allocation (
	order_line_id INTEGER,
	batch_id INTEGER,
	FOREIGN KEY(order_line_id) REFERENCES order_line (id),
	FOREIGN KEY(batch_id) REFERENCES batch (id)
);