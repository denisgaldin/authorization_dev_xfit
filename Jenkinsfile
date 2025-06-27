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
                    python3 -m venv .v
