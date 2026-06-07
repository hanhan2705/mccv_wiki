CREATE TABLE Page_Content (
    PageID    INT NOT NULL,
    VersionID BIGSERIAL,
    Content   TEXT NOT NULL,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (VersionID)
);

-- Index để query theo PageID nhanh hơn
CREATE INDEX idx_page_content_pageid ON Page_Content(PageID);