from pyspark.sql import SparkSession
from utils.logging_utils import get_logger
from threading import Lock
from queue import Queue
import weakref
import uuid

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
        
    def __del__(self):
        logger.info(f"SparkSessionPool instance is being destroyed. Object ID: {id(self)}")
        self.stop_all_sessions()

    def initialize(self):
        self._pool = Queue()
        self._active_sessions = set()
        self._max_sessions = 7  # 최대 세션 수 설정

    def get_spark_session(self):
        with self._lock:
            if not self._pool.empty():
                session = self._pool.get()
                logger.info(f"Reusing existing Spark session from pool:")
            elif len(self._active_sessions) < self._max_sessions:
                session = self._create_new_session()
            else:
                logger.warning("Maximum number of Spark sessions reached. Waiting for an available session.")
                session = self._pool.get()  # 사용 가능한 세션이 반환될 때까지 대기

            self._active_sessions.add(session)
            self._log_session_info(session, "Retrieved")
            return session

    def release_spark_session(self, session):
        with self._lock:
            if session in self._active_sessions:
                self._active_sessions.remove(session)
                self._pool.put(session)
                self._log_session_info(session, "Released")
            else:
                logger.warning(f"Attempted to release a session that was not active: {id(session)}")

    def _create_new_session(self):
        spark = SparkSession.builder \
            .appName("F1RaceData") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .getOrCreate()
        logger.info("Created new Spark session:")

        # new_session = spark.newSession()
        # # 고유한 식별자 생성 및 설정
        # unique_id = str(uuid.uuid4())
        # new_session.conf.set("custom.session.id", unique_id)

        return spark

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

def get_spark():
    """
    SparkSession을 얻고 반환하는 의존성 주입 함수
    """
    spark = spark_pool.get_spark_session()
    try:
        yield spark
    finally:
        spark_pool.release_spark_session(spark)