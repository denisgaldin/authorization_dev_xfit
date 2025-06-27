pipeline {
    agent any

    environment {
        BASE_URL = 'https://dev-mobile.xfit.ru'  // или из Jenkins credentials
        VENV_DIR = '.venv'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Получаем код из репозитория'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Установка зависимостей'
                sh '''
                    python3 -m venv $VENV_DIR
                    source $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🚀 Запуск pytest'
                sh '''
                    source $VENV_DIR/bin/activate
                    pytest tests/ --disable-warnings -v
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Успешно: Все тесты прошли'
        }
        failure {
            echo '❌ Ошибка: Проверить тесты и окружение'
        }
        always {
            echo '🧹 Очистка окружения'
            sh 'rm -rf $VENV_DIR'
        }
    }
}
