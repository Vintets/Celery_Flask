from kombu.serialization import registry


broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_ignore_result = False
task_serializer = 'pickle'
result_serializer = 'json'
accept_content = ['json', 'application/text', 'pickle']
worker_safe_modules = ['tasks']
timezone = 'Europe/Moscow'
enable_utc = True
registry.enable('json')
registry.enable('application/text')
# registry.enable('pickle')
# registry.enable('application/x-python-serialize')
