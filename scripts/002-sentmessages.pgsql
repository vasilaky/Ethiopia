--
-- Table of messages sent
--

CREATE TABLE sentmessages
(
  -- Status of message that was sent
  status       TEXT,

  cell_phone   TEXT,
  user_id      SERIAL references users(id),
  message      TEXT PRIMARY KEY,
  convo_id     SERIAL UNIQUE,

	timestamp	TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
