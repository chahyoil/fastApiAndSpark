from jinja2 import Template

# 레이스 결과 조회 쿼리
GET_RACE_RESULTS = Template("""
SELECT 
    r.*, 
    d.forename, 
    d.surname, 
    c.name as constructor_name, 
    s.status
FROM results r
JOIN drivers d ON r.driverId = d.driverId
JOIN constructors c ON r.constructorId = c.constructorId
JOIN status s ON r.statusId = s.statusId
WHERE r.raceId = {{ race_id }}
ORDER BY r.position
""")

# 가장 빠른 랩 타임 조회 쿼리
GET_FASTEST_LAPS = Template("""
SELECT 
    r.position, 
    d.forename, 
    d.surname, 
    r.fastestLapTime, 
    r.fastestLapSpeed
FROM results r
JOIN drivers d ON r.driverId = d.driverId
WHERE r.raceId = {{ race_id }} 
  AND r.fastestLapTime IS NOT NULL
ORDER BY r.fastestLapTime
LIMIT 10
""")

# 모든 레이스 목록 카운트 조회 쿼리
GET_ALL_RACES_COUNT = Template("""
    SELECT COUNT(*) AS count FROM races
""")

# 모든 레이스 목록 조회 쿼리 (페이지네이션 적용)
GET_ALL_RACES = Template("""
    SELECT * FROM (
        SELECT 
            raceId, year, round, name, date,
            ROW_NUMBER() OVER (ORDER BY year DESC, round) as row_num 
        FROM races
    ) ranked
    WHERE row_num > {{ offset }} AND row_num <= {{ offset + page_size }}
""")

# 특정 레이스 세부 정보 조회 쿼리
GET_RACE_DETAILS = Template("""
SELECT r.*, c.name as circuit_name, c.location, c.country
FROM races r
JOIN circuits c ON r.circuitId = c.circuitId
WHERE r.raceId = {{ race_id }}
""")