pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url') // добавь это как Secret Text в Jenkins credentials
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
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🚀 Запуск автотестов'
                sh '''
                    . .venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -v
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Очистка окружения'
            sh 'rm -rf .venv'
        }
        failure {
            echo '❌ Ошибка: Проверить тесты и окружение'
        }
        success {
            echo '✅ Все тесты прошли успешно!'
        }
    }
}
