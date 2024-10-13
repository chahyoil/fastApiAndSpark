from jinja2 import Template

GET_CONSTRUCTOR_STANDINGS_COUNT = Template("""
SELECT COUNT(*) as count 
FROM constructor_standings cs
JOIN constructors c ON cs.constructorId = c.constructorId
JOIN races r ON cs.raceId = r.raceId
{% if year is not none %}
WHERE r.year = {{ year }}
{% endif %}
""")

GET_CONSTRUCTOR_STANDINGS = Template("""
WITH ranked_standings AS (
    SELECT 
        cs.*, 
        c.name as constructor_name, 
        r.year,
        ROW_NUMBER() OVER (ORDER BY r.year DESC, cs.position) as row_num
    FROM constructor_standings cs
    JOIN constructors c ON cs.constructorId = c.constructorId
    JOIN races r ON cs.raceId = r.raceId
    {% if year is not none %}
    WHERE r.year = {{ year }}
    {% endif %}
)
SELECT *
FROM ranked_standings
WHERE row_num > {{ offset }} AND row_num <= {{ offset + page_size }}
ORDER BY year DESC, position
""")

# 생성자 결과 조회 쿼리
GET_CONSTRUCTOR_RESULTS = Template("""
SELECT 
    r.*, 
    ra.year, 
    ra.name as race_name, 
    d.surname as driver_surname
FROM constructorResults cr
JOIN results r ON cr.raceId = r.raceId AND cr.constructorId = r.constructorId
JOIN races ra ON r.raceId = ra.raceId
JOIN drivers d ON r.driverId = d.driverId
WHERE cr.constructorId = {{ constructor_id }}
{% if year %}
AND ra.year = {{ year }}
{% endif %}
ORDER BY ra.year DESC, ra.round
""")
