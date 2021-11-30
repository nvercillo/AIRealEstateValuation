CREATE TABLE `PROPERTY_IMAGES` (
	`id` VARCHAR(36),
    `property_id`VARCHAR(36),
    `num_blobs`  SMALLINT NOT NULL,
    
	PRIMARY KEY( `id`),
    CONSTRAINT fk_property_id_reference
    FOREIGN KEY (`property_id`) 
    	REFERENCES AI_PROPERTY_DATA(`id`)
);