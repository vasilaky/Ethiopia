--
-- Table of calls
--

CREATE TABLE calls
(
  -- Status of message that was sent
  response     BOOLEAN DEFAULT FALSE,

  user_id      SERIAL,
  call_id      VARCHAR(40),
  question     TEXT,
  answer       INTEGER,
  timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,


FOREIGN KEY (user_id)
REFERENCES users (id)
ON DELETE CASCADE);
