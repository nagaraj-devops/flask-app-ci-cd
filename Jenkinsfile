pipeline {
    agent any
    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '412275828685.dkr.ecr.ap-south-1.amazonaws.com'
        IMAGE_NAME = 'flask-app-ci-cd'
        TARGET_IP = '15.207.11.6'
    }
    stages {
        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'ecr-cross-account-creds']]) {
                        def awsCli = "/usr/local/bin/aws"
                        
                        // 1. Login
                        sh "${awsCli} ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                        
                        // 2. Build or Tag the image specifically for ECR
                        // Assuming your build stage created an image named 'flask-app-ci-cd'
                        sh "docker tag flask-app-ci-cd:${BUILD_NUMBER} ${ECR_REGISTRY}/flask-app-ci-cd:${BUILD_NUMBER}"
                        
                        // 3. Push the fully qualified image
                        sh "docker push ${ECR_REGISTRY}/flask-app-ci-cd:${BUILD_NUMBER}"
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                // This binds your private key to a temporary file path ($MY_KEY)
                withCredentials([sshUserPrivateKey(credentialsId: 'deploy-ssh-key-nagaraj-aws', keyFileVariable: 'MY_KEY', usernameVariable: 'USER')]) {
                    sh """
                        ssh -i $MY_KEY -o StrictHostKeyChecking=no ubuntu@15.207.11.6 << 'EOF'
                            # Use the explicit path found on target server
                            /snap/bin/aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 412275828685.dkr.ecr.ap-south-1.amazonaws.com
                            
                            docker pull 412275828685.dkr.ecr.ap-south-1.amazonaws.com/flask-app-ci-cd:6
                            docker stop flask-app || true
                            docker rm flask-app || true
                            docker run -d -p 5000:5000 --name flask-app 412275828685.dkr.ecr.ap-south-1.amazonaws.com/flask-app-ci-cd:6
        EOF
                    """
                }
            }
        }
    }
}