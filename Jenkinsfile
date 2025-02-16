pipeline {
    agent any

    environment {
        EC2_USER = 'ubuntu'
        EC2_HOST = '13.201.63.31'
        EC2_KEY = '/var/lib/jenkins/jenkkins.pem'
        REMOTE_DIR = '/home/ubuntu/chatbot'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', credentialsId: 'your-github-cred-id', url: 'git@github.com:your-repo/chatbot.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    sshagent(['your-ssh-cred-id']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << EOF
                        cd ${REMOTE_DIR}
                        git pull origin main
                        source venv/bin/activate
                        pip install -r requirements.txt
                        sudo systemctl restart chatbot
                        EOF
                        """
                    }
                }
            }
        }
    }
}

