pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'sudo docker build -t financial-risk-scanner .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'sudo docker stop risk-app || true'
                sh 'sudo docker rm risk-app || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                sudo docker run -d \
                -p 8501:8501 \
                --name risk-app \
                financial-risk-scanner
                '''
            }
        }
    }
}