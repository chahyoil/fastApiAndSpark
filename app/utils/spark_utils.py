from pyspark.sql import SparkSession
from utils.logging_utils import get_logger
from threading import Lock
from queue import Queue
import weakref
import uuid
import time
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
        self._max_sessions = 4
        self._base_session = self._create_base_session()
        self._session_timeout = 30  # 30초 타임아웃

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

def get_spark():
    """
    SparkSession을 얻고 반환하는 의존성 주입 함수
    """
    try:
        spark = spark_pool.get_spark_session(timeout=30)
        yield spark
    except TimeoutError:
        logger.error("Timeout occurred while waiting for a Spark session")
        raise
    finally:
        spark_pool.release_spark_session(spark)