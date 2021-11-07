CREATE TABLE `IMAGE_BLOB` (
	`blob_index` SMALLINT,
    `image_id`VARCHAR(36),
    `raw_image_binary` BLOB NOT NULL,
    
	PRIMARY KEY( `blob_index`, `image_id`),
    CONSTRAINT fk_image_id
    FOREIGN KEY (`image_id`) 
    	REFERENCES PROPERTY_IMAGES(`id`)
);