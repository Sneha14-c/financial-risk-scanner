pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t financial-risk-scanner .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop risk-app || true'
                sh 'docker rm risk-app || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                docker run -d \
                -p 8501:8501 \
                --name risk-app \
                financial-risk-scanner
                '''
            }
        }
    }
}