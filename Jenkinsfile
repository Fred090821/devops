pipeline {
    agent any
   options{
//        buildDiscarder(logRotator(numToKeepStr:'20', daysToKeepStr:'5'))
            buildDiscarder(logRotator(numToKeepStr:'2', daysToKeepStr:'1'))
   }
    environment{
       REGISTRY = 'adedo2009/devops'
       DOCKERHUB_CREDENTIALS = credentials('docker-hub')
       dockerImage = ''
   }
    stages {
         stage(' Checkout Devops Code') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
                }
                git 'https://github.com/Fred090821/devops.git'
            }
        }
        stage(' Start Back End Server...') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat 'start/min /usr/bin/python3 rest_app.py'
                        } else {
                            sh 'nohup /usr/bin/python3 rest_app.py &'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Server'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Start Front End Server... ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                           bat 'start/min /usr/bin/python3 web_app.py'
                        } else {
                            sh 'nohup nohup /usr/bin/python3 web_app.py &'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Front End Server'
                        error('Aborting The Build')
                    }
                }
            }
        }

        stage(' Run Back End Tests ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '/usr/bin/python3 backend_testing.py'
                        } else {
                            sh '/usr/bin/python3 backend_testing.py'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Test'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Run Front End Tests ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '/usr/bin/python3 frontend_testing.py'
                        } else {
                            sh '/usr/bin/python3 frontend_testing.py '
                        }
                    }catch(Exception e){
                        echo 'Exception Running Front End Test'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Run Combine Tests ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '/usr/bin/python3 combined_testing.py'
                        } else {
                            sh '/usr/bin/python3 combined_testing.py'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Front End Test'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Clean Environment After Tests ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '/usr/bin/python3 clean_environment.py'
                        } else {
                             sh '/usr/bin/python3 clean_environment.py'
                        }
                    }catch(Exception e){
                        echo 'Exception Cleaning The Environment'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Docker Build Back End Image ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                           bat 'docker build -t devops .'
                        } else {
                            sh 'docker build -t devops .'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Docker Build'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage(' Log In To Docker hub ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                        } else {
                            sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                        }
                    }catch(Exception e){
                        echo 'Exception Login into Ducker Hub'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Tag & Push Rest Image ') {
            steps {
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat 'docker tag devops adedo2009/devops:latest'
                            bat 'docker tag devops adedo2009/devops:${BUILD_NUMBER}'
                            bat 'docker push -a $REGISTRY'
                        } else {
                            sh 'docker tag devops adedo2009/devops:latest'
                            sh 'docker tag devops adedo2009/devops:${BUILD_NUMBER}'
                            sh 'docker push -a adedo2009/devops'
                        }
                    }catch(Exception e){
                        echo 'Exception Pushing Docker Build'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage(' Start Rest Containers ') {
            steps {
               echo 'Start containers using docker compose ===> '
               script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat 'docker-compose -f docker-compose.yml up -d --wait'
                            bat 'docker-compose ps'
                        } else {
                            echo 'docker-compose -f docker-compose.yml up -d --wait ===> '
                            sh 'docker-compose -f docker-compose.yml up -d --wait'
                            echo 'docker-compose -f docker-compose.yml ps ===> '
                            sh 'docker-compose -f docker-compose.yml ps'
                        }
                    }catch(Exception e){
                        echo 'Exception docker compose starting container'
                        error('Aborting the build')
                    }
                }
            }
        }
//         stage(' Docker run backend testing ===>') {
//             steps {
//                 script {
//                     try{
//                         if (checkOs() == 'Windows') {
//                             bat '/usr/bin/python3 backend_testing.py'
//                         } else {
//                             sh '/usr/bin/python3 backend_testing.py'
//                         }
//                     }catch(Exception e){
//                         echo 'Exception Running Back End Test'
//                         error('Aborting The Build')
//                     }
//                 }
//             }
//         }
    }
    post {
        always {
            script {
                try{
                    if (checkOs() == 'Windows') {
                         bat '/usr/bin/python3 clean_environment.py'
                         bat 'docker-compose -f docker-compose.yml down'
                         bat 'docker rmi adedo2009/devops:latest'
                         bat 'docker system prune -a --volumes -f'
                         bat 'docker logout'
                    } else {
//                       sh '/usr/bin/python3 clean_environment.py'
//                       sh 'docker-compose -f /Users/jaydenassi/Documents/GitHub/devops/docker-compose.yml down --remove-orphans -v'
                         sh 'docker rmi adedo2009/devops:latest'
                         sh 'docker system prune -a --volumes -f'
                         sh 'docker logout'
                    }
                }catch(Exception e){
                        echo 'Exception docker compose starting container'
                        error('Aborting the build')
                }
            }
        }
        success {
            echo 'All test run successfully'
        }
        failure {
            echo 'One or more test(s) failed'
            emailext body: 'failed jenkins build', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequestRecipientProvider']], subject: 'test'
        }
        unstable {
            echo 'The build is unstable'
        }
        changed {
            echo 'The pipeline  state has changed'
        }
    }
}

def checkOs(){
    if (isUnix()) {
        def uname = sh script: 'uname', returnStdout: true
        if (uname.startsWith("Darwin")) {
            return "Macos"
        }
        else {
            return "Linux"
        }
    }
    else {
        return "Windows"
    }

}

