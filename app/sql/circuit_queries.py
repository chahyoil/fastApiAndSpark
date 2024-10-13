from jinja2 import Template

# 모든 서킷 목록 조회 쿼리
GET_ALL_CIRCUITS = Template("""
    SELECT * FROM (
        SELECT 
            circuitId as circuit_id, 
            name, 
            location, 
            country, 
            lat, 
            lng,
            ROW_NUMBER() OVER (ORDER BY circuitId) as row_num 
        FROM circuits
    ) ranked
    WHERE row_num > {{ offset }} AND row_num <= {{ offset + page_size }}
""")

# 서킷 수 조회 쿼리
GET_CIRCUITS_COUNT = Template("""
SELECT COUNT(*) as count FROM circuits
""")

GET_CIRCUIT_INFO = Template("""
SELECT 
    c.circuitId as circuit_id, 
    c.circuitRef,
    c.name, 
    c.location, 
    c.country, 
    c.lat, 
    c.lng,
    c.alt,
    c.url,
    COUNT(DISTINCT r.raceId) as total_races,
    AVG(r.round) as avg_round
FROM circuits c
LEFT JOIN races r ON c.circuitId = r.circuitId
WHERE c.circuitId = {{ circuit_id }}
GROUP BY 
    c.circuitId, 
    c.circuitRef,
    c.name, 
    c.location, 
    c.country, 
    c.lat, 
    c.lng,
    c.alt,
    c.url
""")

GET_CIRCUIT_RACES = Template("""
SELECT 
    r.raceId AS race_id,
    r.year,
    r.round,
    r.name,
    r.date,
    d.surname as winner_surname,
    c.name as constructor_name,
    res.time as winning_time
FROM races r
JOIN results res ON r.raceId = res.raceId
JOIN drivers d ON res.driverId = d.driverId
JOIN constructors c ON res.constructorId = c.constructorId
WHERE r.circuitId = {{ circuit_id }} AND res.position = 1
ORDER BY r.year DESC, r.round DESC
""")