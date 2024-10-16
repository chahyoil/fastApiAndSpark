from pyspark.sql import SparkSession
from utils.logging_utils import get_logger
from threading import Lock
from queue import Queue
import weakref
import uuid
import time
from contextlib import asynccontextmanager
from datetime import datetime

logger = get_logger(__name__)

class SparkSessionPool:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                instance = super(SparkSessionPool, cls).__new__(cls)
                instance.initialize()
                cls._instance = weakref.ref(instance)
                logger.info(f"SparkSessionPool instance created. Object ID: {id(instance)}")
            else:
                instance = cls._instance()
                if instance is None:
                    instance = super(SparkSessionPool, cls).__new__(cls)
                    instance.initialize()
                    cls._instance = weakref.ref(instance)
                    logger.info(f"SparkSessionPool instance recreated. Object ID: {id(instance)}")
                else:
                    logger.info(f"Existing SparkSessionPool instance returned. Object ID: {id(instance)}")
            return instance

    def initialize(self):
        self._pool = Queue()
        self._active_sessions = {}  # 세션 ID를 키로 사용하는 딕셔너리로 변경
        self._max_sessions = 15
        self._base_session = self._create_base_session()
        self._session_timeout = 3000  # 30초 타임아웃

    def _create_base_session(self):
        spark = SparkSession.builder \
            .appName("F1RaceData") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .config("javax.jdo.option.ConnectionURL", "jdbc:derby:memory:myDb;create=true") \
            .config("javax.jdo.option.ConnectionDriverName", "org.apache.derby.jdbc.EmbeddedDriver") \
            .config("hive.metastore.schema.verification", "false") \
            .enableHiveSupport() \
            .getOrCreate()
        logger.info("Created base Spark session")
        return spark

    def get_spark_session(self, timeout=30):
        overall_start_time = time.time()
        start_time = time.time()
        while True:
            with self._lock:
                if not self._pool.empty():
                    session = self._pool.get()
                    self._activate_session(session)
                    overall_end_time = time.time()
                    logger.info(f"Total time to get session from pool: {overall_end_time - overall_start_time:.4f} seconds")
                    return session
                elif len(self._active_sessions) < self._max_sessions:
                    session = self._create_new_session()
                    self._activate_session(session)
                    overall_end_time = time.time()
                    logger.info(f"Total time to create and activate new session: {overall_end_time - overall_start_time:.4f} seconds")
                    return session
                else:
                    # 오래된 세션 확인 및 강제 해제
                    current_time = time.time()
                    for session_id, (session, activation_time) in list(self._active_sessions.items()):
                        if current_time - activation_time > self._session_timeout:
                            logger.warning(f"Force releasing session {session_id} due to timeout")
                            self.release_spark_session(session)
                            session = self._create_new_session()
                            self._activate_session(session)
                            overall_end_time = time.time()
                            logger.info(f"Total time to force release and create new session: {overall_end_time - overall_start_time:.4f} seconds")
                            return session

            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for available Spark session")

            time.sleep(1)  # 잠시 대기 후 다시 시도

    def release_spark_session(self, session):
        with self._lock:
            session_id = session.conf.get("custom.session.id")
            if session_id in self._active_sessions:
                del self._active_sessions[session_id]
                self._pool.put(session)
                self._log_session_info(session, "Released")
                logger.info(f"Successfully released and returned session to pool: {session_id}")
            else:
                logger.warning(f"Attempted to release a session that was not active: {session_id}")

    def _activate_session(self, session):
        session_id = session.conf.get("custom.session.id")
        self._active_sessions[session_id] = (session, time.time())
        
        start_time = time.time()
        session.sql("USE f1_database").collect()
        end_time = time.time()
        sql_execution_time = end_time - start_time
        
        logger.info(f"SQL execution time: {sql_execution_time:.4f} seconds")
        self._log_session_info(session, "Retrieved")

    def _create_new_session(self):
        start_time = time.time()
        new_session = self._base_session.newSession()
        end_time = time.time()
        session_creation_time = end_time - start_time
        
        unique_id = str(uuid.uuid4())
        new_session.conf.set("custom.session.id", unique_id)
        logger.info(f"Created new Spark session with ID: {unique_id}")
        logger.info(f"Session creation time: {session_creation_time:.4f} seconds")
        return new_session

    def _log_session_info(self, session, action):
        session_id = id(session)
        spark_app_id = session.sparkContext.applicationId
        
        logger.info(f"{action} Spark session:")
        logger.info(f"  - Session object ID: {session_id}")
        logger.info(f"  - Spark Application ID: {spark_app_id}")
        logger.info(f"  - Session object hash: {hash(session)}")
        logger.info(f"  - Active sessions: {len(self._active_sessions)}")
        logger.info(f"  - Available sessions in pool: {self._pool.qsize()}")

    def stop_all_sessions(self):
        with self._lock:
            while not self._pool.empty():
                session = self._pool.get()
                session.stop()
            for session in list(self._active_sessions):
                session.stop()
                self._active_sessions.remove(session)
            logger.info("All Spark sessions have been stopped.")

# 전역 SparkSessionPool 인스턴스 생성
spark_pool = SparkSessionPool()

from contextlib import contextmanager, asynccontextmanager

@contextmanager
def get_spark():
    """
    SparkSession을 얻고 반환하는 동기 의존성 주입 함수
    """
    start_time = time.time()
    start_time_human = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S.%f')
    logger.info(f"[SessionTime] Starting to acquire Spark session at {start_time_human}")

    try:
        spark = spark_pool.get_spark_session(timeout=30)
        session_id = spark.conf.get("custom.session.id")

        acquire_time = time.time()
        acquire_time_human = datetime.fromtimestamp(acquire_time).strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info(f"[SessionTime] Acquired Spark session at {acquire_time_human} with session_id: {session_id}")
        logger.info(f"[SessionTime] Time to acquire session: {acquire_time - start_time:.4f} seconds with session_id: {session_id}")

        yield spark, session_id
    except TimeoutError:
        logger.error("Timeout occurred while waiting for a Spark session")
        raise
    finally:
        end_time = time.time()
        end_time_human = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info(f"[SessionTime] Releasing Spark session at {end_time_human} with session_id: {session_id}")
        
        if 'spark' in locals():
            spark_pool.release_spark_session(spark)
            release_time = time.time()
            release_time_human = datetime.fromtimestamp(release_time).strftime('%Y-%m-%d %H:%M:%S.%f')
            logger.info(f"[SessionTime] Released Spark session at {release_time_human} with session_id: {session_id}")
            logger.info(f"[SessionTime] Total time for Spark session usage: {release_time - acquire_time:.4f} seconds with session_id: {session_id}")
        else:
            logger.warning("Spark session was not acquired, so it cannot be released")

        logger.info(f"[SessionTime] Total time in get_spark context: {end_time - start_time:.4f} seconds with session_id: {session_id}")

def get_spark_and_session_id():
    with get_spark() as (spark, session_id):
        yield spark, session_id

#####

# from pyspark.sql import SparkSession
# from contextlib import contextmanager
# import uuid
# from utils.logging_utils import get_logger
# import time
# from datetime import datetime

# logger = get_logger(__name__)

# _spark_session = None

# def get_spark_session():
#     global _spark_session
#     if _spark_session is None:
#         _spark_session = SparkSession.builder \
#             .appName("F1RaceData") \
#             .master("local[*]") \
#             .getOrCreate()
#     return _spark_session

# def stop_spark_session():
#     global _spark_session
#     if _spark_session:
#         _spark_session.stop()
#         _spark_session = None

# @contextmanager
# def get_spark():
#     """
#     SparkSession을 얻고 반환하는 동기 의존성 주입 함수
#     """
#     global _spark_session
#     start_time = time.time()
#     start_time_human = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S.%f')
#     logger.info(f"[SessionTime] Starting to acquire Spark session at {start_time_human}")

#     spark = get_spark_session()
#     session_id = spark.sparkContext.applicationId

#     acquire_time = time.time()
#     acquire_time_human = datetime.fromtimestamp(acquire_time).strftime('%Y-%m-%d %H:%M:%S.%f')
#     logger.info(f"[SessionTime] Acquired Spark session at {acquire_time_human}")
#     logger.info(f"[SessionTime] Time to acquire session: {acquire_time - start_time:.2f} seconds")

#     try:
#         yield spark, session_id
#     finally:
#         end_time = time.time()
#         end_time_human = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S.%f')
#         logger.info(f"[SessionTime] Finished using Spark session at {end_time_human}")
#         logger.info(f"[SessionTime] Total time for Spark session usage: {end_time - acquire_time:.2f} seconds")
#         # 주의: 여기서는 세션을 중지하지 않습니다. 글로벌 세션을 유지합니다.

# def get_spark_and_session_id():
#     with get_spark() as (spark, session_id):
#         yield spark, session_id

# class SparkSessionPool:
#     def __init__(self):
#         self._base_session = get_spark_session()

#     def get_spark_session(self, timeout=30):
#         return get_spark_session()

#     def release_spark_session(self, session):
#         # 싱글톤 패턴에서는 실제로 세션을 해제하지 않습니다.
#         pass

#     def stop_all_sessions(self):
#         stop_spark_session()

# # 전역 SparkSessionPool 인스턴스 생성 (실제로는 싱글톤을 사용)
# spark_pool = SparkSessionPool()