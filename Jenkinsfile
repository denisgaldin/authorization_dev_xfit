pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url') // переменная через Jenkins Credentials
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Получаем код из репозитория'
                checkout scm
            }
        }

        stage('Install & Run') {
            steps {
                echo '🐍 Установка зависимостей и запуск тестов'
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/python -m pytest --maxfail=1 --disable-warnings -v
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Все тесты прошли успешно!'
        }
        failure {
            echo '❌ Ошибка: Проверить тесты и окружение'
        }
    }
}
