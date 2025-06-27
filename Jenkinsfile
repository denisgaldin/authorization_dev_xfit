pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url') // Подставь свою переменную Jenkins Credentials
    }

    tools {
        python 'Python_3.13' // Убедись, что такой Python есть в Manage Jenkins → Global Tool Config
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
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest --alluredir=allure-results --maxfail=1 --disable-warnings -v
                '''
            }
        }

        stage('Allure Report') {
            steps {
                echo '📊 Генерация Allure отчета'
                allure([
                    includeProperties: false,
                    jdk: '',
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
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
    }
}
