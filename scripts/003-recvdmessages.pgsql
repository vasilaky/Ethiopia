--
-- Table of messages received
--

CREATE TABLE recvdmessages
(
  cell_phone   TEXT,
  user_id      SERIAL,
  message      TEXT PRIMARY KEY,
  convo_id     SERIAL UNIQUE references sentmessages(convo_id),

  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
