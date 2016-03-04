---
--- Table of Messages
---


CREATE TABLE message(
  message_id        SERIAL PRIMARY KEY,
  convo_id          SMALLSERIAL references users(id) ON DELETE CASCADE,
  content           TEXT
)
