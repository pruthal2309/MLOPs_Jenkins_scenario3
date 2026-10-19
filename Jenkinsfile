
pipeline {
    agent {
        label 'local'
    }

    stages {
        stage('Confirm Git Checkout') {
            steps {
                bat 'git log -1 --oneline'
                bat 'dir'
            }
        }

        stage('Validate Configuration') {
            steps {
                bat 'docker compose -p scenario-1 -f compose.yaml config --quiet'
            }
        }

        stage('Build Images') {
            steps {
                bat 'docker compose -p scenario-1 -f compose.yaml build'
            }
        }

        stage('Check Python Syntax') {
            steps {
                bat 'docker compose -p scenario-1 -f compose.yaml run --rm --no-deps webapp python -m compileall -q .'
                bat 'docker compose -p scenario-1 -f compose.yaml run --rm --no-deps dbapp python -m compileall -q .'
            }
        }

        stage('Deploy Containers') {
            steps {
                bat 'docker compose -p scenario-1 -f compose.yaml up -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'docker compose -p scenario-2 -f compose.yaml ps'
                bat 'powershell -NoProfile -Command "Invoke-WebRequest -UseBasicParsing http://localhost:5000/ -TimeoutSec 10 | Out-Null"'
            }
        }
    }
}
