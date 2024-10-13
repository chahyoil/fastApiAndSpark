from jinja2 import Template

# 모든 드라이버 조회 (페이지네이션 적용)
GET_ALL_DRIVERS = Template("""
    SELECT * FROM (
        SELECT 
            driverId as driver_id,
            code,
            forename,
            surname,
            dob,
            nationality,
            ROW_NUMBER() OVER (ORDER BY driverId) as row_num 
        FROM drivers
    ) ranked
    WHERE row_num > {{ offset }} AND row_num <= {{ offset + page_size }}
""")

# 전체 드라이버 수 조회
GET_DRIVERS_COUNT = Template("""
    SELECT COUNT(*) as count FROM drivers
""")

# 드라이버 상세 정보를 가져오는 쿼리
GET_DRIVER_DETAILS = Template("""
    SELECT 
        d.*, 
        COUNT(DISTINCT r.raceId) as total_races,
        SUM(ds.points) as total_points,
        COUNT(CASE WHEN ds.position = 1 THEN 1 END) as wins
    FROM 
        drivers d
    LEFT JOIN 
        results r ON d.driverId = r.driverId
    LEFT JOIN 
        driverStandings ds ON d.driverId = ds.driverId
    WHERE 
        d.driverId = {{ driver_id }}
    GROUP BY 
        d.driverId
""")

# 드라이버의 연도별 순위를 가져오는 쿼리
GET_DRIVER_STANDINGS = Template("""
    SELECT 
        ds.*, 
        r.year, 
        r.name as race_name
    FROM 
        driverStandings ds
    JOIN 
        races r ON ds.raceId = r.raceId
    WHERE 
        ds.driverId = {{ driver_id }}
    {% if year %}
    AND r.year = {{ year }}
    {% endif %}
    ORDER BY 
        r.year DESC, 
        r.round DESC
""")
