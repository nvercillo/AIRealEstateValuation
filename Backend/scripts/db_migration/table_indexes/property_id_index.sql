ALTER TABLE PROPERTY_IMAGES
ADD CONSTRAINT fk_prop_id
FOREIGN KEY (property_id) 
REFERENCES AI_PROPERTY_DATA(`id`);