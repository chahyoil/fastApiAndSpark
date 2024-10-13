from jinja2 import Template

# 모든 드라이버 조회 (페이지네이션 적용)
GET_ALL_DRIVERS = Template("""
    SELECT * FROM (
        SELECT *, ROW_NUMBER() OVER (ORDER BY driverId) as row_num 
        FROM drivers
    ) ranked
    WHERE row_num > {{ offset }} AND row_num <= {{ offset + page_size }}
""")

# 전체 드라이버 수 조회
GET_DRIVERS_COUNT = Template("""
    SELECT COUNT(*) as count FROM drivers
""")

# 특정 ID의 드라이버 조회
GET_DRIVER_BY_ID = Template("""
    SELECT * FROM drivers WHERE driverId = {{ driver_id }}
""")

# 특정 연도의 레이스 결과 조회
GET_RACE_RESULTS = Template("""
    SELECT 
        r.name as race_name, d.surname, rs.position
    FROM results rs
    JOIN races r ON rs.raceId = r.raceId
    JOIN drivers d ON rs.driverId = d.driverId
    WHERE r.year = {{ year }}
    ORDER BY r.date, rs.position
""")

# Spark 예제 쿼리: 팀별 결과 수 조회
SPARK_EXAMPLE_QUERY = Template("""
    SELECT 
        c.name as team, COUNT(*) as count 
    FROM results r
    JOIN constructors c ON r.constructorId = c.constructorId
    GROUP BY c.name
    ORDER BY count DESC
    LIMIT {{ limit }}
""")
