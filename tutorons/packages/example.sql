-- SQL query for getting results_with_code field for a package.
-- Needs to be translated into Django's ORM; untested.
SELECT SUM(pages_with_code) / (SUM(pages_with_code) + SUM(pages_without_code))::decimal AS ratio
  FROM (
    SELECT web_page_url, COUNT(page_has_code) AS pages_with_code, COUNT(page_missing_code) AS pages_without_code
    FROM (
      SELECT webpagecontent.url as web_page_url,
        webpagecontent.id AS web_page_content_id,
        BOOL_OR(CASE WHEN (compute_index IS NULL) THEN true ELSE NULL END) AS page_missing_code,
        BOOL_OR(CASE WHEN (compute_index = 3) THEN true ELSE NULL END) AS page_has_code
      FROM webpagecontent
      LEFT OUTER JOIN code ON web_page_id = webpagecontent.id
      JOIN searchresultcontent ON content_id = webpagecontent.id
      JOIN searchresult ON searchresult.id = search_result_id
      JOIN search ON search_id = search.id
      WHERE search.fetch_index = 13 AND package = 'nodemailer'
      GROUP BY webpagecontent.id
    ) AS pages_have_code
    JOIN searchresultcontent ON content_id = web_page_content_id
    JOIN searchresult ON searchresult.id = search_result_id
    JOIN search ON search_id = search.id
    WHERE search.fetch_index = 13
    GROUP BY web_page_url
  ) AS page_occurrences_with_code;

-- Extracted segment from above SQL query for some testing purposes.
SELECT webpagecontent.url as web_page_url, code.id AS code_id
FROM webpagecontent
LEFT OUTER JOIN code ON web_page_id = webpagecontent.id
JOIN searchresultcontent ON content_id = webpagecontent.id
JOIN searchresult ON searchresult.id = search_result_id
JOIN search ON search_id = search.id
WHERE search.fetch_index = 13 AND package = 'nodemailer'
ORDER BY web_page_url;

-- SQL query for getting the documented_since field for a package.
SELECT MIN(webpageversion.timestamp)
  FROM webpageversion
  JOIN searchresult ON searchresult.url = webpageversion.url
  JOIN search ON search.id = searchresult.search_id
  WHERE search.fetch_index = 13 AND package = 'nodemailer';
