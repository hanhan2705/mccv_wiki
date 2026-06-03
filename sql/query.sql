SELECT * FROM public.page_content
ORDER BY versionid ASC 

TRUNCATE TABLE Page_Content RESTART IDENTITY;

INSERT INTO Page_Content(PageID, Content)
VALUES
(
    1,
    'Original Wiki Content'
);