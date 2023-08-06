/**
 * Copyright (C) 2022 Majormode.  All rights reserved.
 *
 * This software is the confidential and proprietary information of
 * Majormode or one of its subsidiaries.  You shall not disclose this
 * confidential information and shall use it only in accordance with the
 * terms of the license agreement or other applicable agreement you
 * entered into with Majormode.
 *
 * MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
 * OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
 * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
 * LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
 * OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
*/

ALTER TABLE account_picture
  ADD COLUMN rejection_exception text NULL,
  ADD COLUMN capture_time timestamptz(3) NULL;

UPDATE account_picture
  SET capture_time = creation_time;

DELETE FROM account_picture
  WHERE
    picture_id IN (
      SELECT
          picture_id
        FROM
          account_picture
        GROUP BY
           picture_id
        HAVING COUNT(*) > 1
    );

ALTER TABLE account_picture
  ADD CONSTRAINT pk_account_picture_id
    PRIMARY KEY (picture_id);

DELETE FROM account_picture
  WHERE NOT EXISTS (
    SELECT
        true
      FROM
        account
      WHERE
        account.account_id = account_picture.account_id
  );

UPDATE account_picture
  SET submitter_account_id = account_id
  WHERE NOT EXISTS (
    SELECT
        true
      FROM
        account
      WHERE
        account.account_id = account_picture.submitter_account_id
  );

ALTER TABLE account_picture
  ADD CONSTRAINT fk_account_picture_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE SET NULL
      ON UPDATE CASCADE;
