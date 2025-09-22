# myapp/middleware.py
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Логирование входящего запроса
        client_ip = self.get_client_ip(request)
        request_time = datetime.now().isoformat()
        
        log_message = f"{request_time} - IP: {client_ip} - {request.method} {request.path}"
        logger.info(log_message)
        
        # Запись в файл если путь указан
        log_file_path = os.environ.get('LOG_FILE_PATH')
        if log_file_path:
            try:
                with open(log_file_path, 'a', encoding='utf-8') as f:
                    f.write(log_message + '\n')
            except Exception as e:
                logger.error(f"Failed to write to log file: {e}")
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip