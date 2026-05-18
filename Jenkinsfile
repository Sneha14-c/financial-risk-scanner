pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh '/usr/bin/docker build -t financial-risk-scanner .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '/usr/bin/docker stop risk-app || true'
                sh '/usr/bin/docker rm risk-app || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                /usr/bin/docker run -d \
                -p 8501:8501 \
                --name risk-app \
                financial-risk-scanner
                '''
            }
        }
    }
}