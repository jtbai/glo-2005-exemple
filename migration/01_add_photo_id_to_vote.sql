use what_is_it;
ALTER TABLE vote
    add image_id VARCHAR(32);
UPDATE vote set image_id = md5(image_url);
