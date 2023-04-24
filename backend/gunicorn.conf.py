workers = 4  # Número de workers para o Gunicorn
module_name = 'pedrofelipevsl_pythonanywhere_com_wsgi.py:application'  # Nome do arquivo do aplicativo Flask (wsgi.py) e instância do aplicativo (application)

bind = '0.0.0.0:8000'  # Endereço IP e porta para a execução do Gunicorn