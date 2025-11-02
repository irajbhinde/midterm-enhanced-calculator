import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class AppConfig:
    log_dir: str = 'logs'
    history_dir: str = 'history'
    max_history_size: int = 1000
    auto_save: bool = True
    precision: int = 6
    max_input_value: float = 1e12
    encoding: str = 'utf-8'
    log_file: str = 'calculator.log'
    history_file: str = 'history.csv'

    @property
    def history_path(self) -> str:
        return os.path.join(self.history_dir, self.history_file)

    def ensure_dirs(self):
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

    @staticmethod
    def _parse_bool(val: str, default=True) -> bool:
        if val is None:
            return default
        return str(val).strip().lower() in {'1','true','yes','y','on'}

    @classmethod
    def load(cls) -> 'AppConfig':
        load_dotenv(override=False)
        cfg = cls(
            log_dir=os.getenv('CALCULATOR_LOG_DIR','logs'),
            history_dir=os.getenv('CALCULATOR_HISTORY_DIR','history'),
            max_history_size=int(float(os.getenv('CALCULATOR_MAX_HISTORY_SIZE','1000'))),
            auto_save=cls._parse_bool(os.getenv('CALCULATOR_AUTO_SAVE','true')),
            precision=int(float(os.getenv('CALCULATOR_PRECISION','6'))),
            max_input_value=float(os.getenv('CALCULATOR_MAX_INPUT_VALUE','1e12')),
            encoding=os.getenv('CALCULATOR_DEFAULT_ENCODING','utf-8'),
            log_file=os.getenv('CALCULATOR_LOG_FILE','calculator.log'),
            history_file=os.getenv('CALCULATOR_HISTORY_FILE','history.csv'),
        )
        cfg.ensure_dirs()
        return cfg