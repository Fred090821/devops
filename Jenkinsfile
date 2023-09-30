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
//         stage(' Docker run backend testing First Thing===>') {
//             steps {
//             echo '=== Docker run backend testing First Thing ==='
//                 script {
//                     try{
//                         if (checkOs() == 'Windows') {
//                             echo '/usr/bin/python3 backend_testing.py '
//                             bat '/usr/bin/python3 backend_testing.py'
//                         } else {
//                             echo '/usr/bin/python3 backend_testing.py '
//                             sh '/usr/bin/python3 backend_testing.py'
//                         }
//                     }catch(Exception e){
//                         echo 'Exception Running Back End Test'
//                         error('Aborting The Build')
//                     }
//                 }
//             }
//         }
        stage(' Verify Tooling ') {
            steps {
            echo '=== Verify Tooling ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '''
                               docker version
                               docker info
                               docker compose version
                               python3 --version
                            '''
                        } else {
                            sh '''
                              docker version
                              docker info
                              docker compose version
                              python3 --version
                            '''
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Server'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Prune Docker Data ') {
            steps {
            echo '=== Prune Docker Data ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '''
                               docker-compose -f docker-compose.yml down --remove-orphans -v
                               docker rmi adedo2009/devops:latest
                               docker system prune -a --volumes -f
                               docker logout
                             '''
                        } else {
                            sh '''
                               docker-compose -f docker-compose.yml down --remove-orphans -v
                               docker system prune -a --volumes -f
                               docker logout
                             '''
                        }
                    }catch(Exception e){
                        echo 'Exception pruning the data'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Docker run backend testing First Thing===>') {
            steps {
            echo '=== Docker run backend testing First Thing ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            echo '/usr/bin/python3 backend_testing.py '
                            bat '/usr/bin/python3 backend_testing.py'
                        } else {
                            echo '/usr/bin/python3 backend_testing.py '
                            sh '/usr/bin/python3 backend_testing.py'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Test'
                        error('Aborting The Build')
                    }
                }
            }
        }
         stage(' Checkout Devops Code ') {
            steps {
            echo '=== Checkout Devops Code ==='
                script {
                    properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
                }
                git 'https://github.com/Fred090821/devops.git'
            }
        }
        stage(' Docker run backend testing First Thing===>') {
            steps {
            echo '=== Docker run backend testing First Thing ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            echo '/usr/bin/python3 backend_testing.py '
                            bat '/usr/bin/python3 backend_testing.py'
                        } else {
                            echo '/usr/bin/python3 backend_testing.py '
                            sh '/usr/bin/python3 backend_testing.py'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Test'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Start Back End Server...') {
            steps {
            echo '=== Start Back End Server ==='
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
            echo '=== Start Front End Server ==='
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
            echo '=== Run Back End Tests ==='
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
            echo '=== Run Front End Tests ==='
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
            echo '=== Run Combine Tests ==='
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
            echo '=== Clean Environment After Tests ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '''
                               /usr/bin/python3 clean_environment.py
                             '''
                        } else {
                             sh '''
                               /usr/bin/python3 clean_environment.py
                             '''
                        }
                    }catch(Exception e){
                        echo 'Exception Cleaning The Environment'
                        error('Aborting The Build')
                    }
                }
            }
        }
        stage(' Docker run backend testing ===>') {
            steps {
            echo '=== Docker run backend testing After Cleaning The Environment ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            echo '/usr/bin/python3 backend_testing.py '
                            bat '/usr/bin/python3 backend_testing.py'
                        } else {
                            echo '/usr/bin/python3 backend_testing.py '
                            sh '/usr/bin/python3 backend_testing.py'
                        }
                    }catch(Exception e){
                        echo 'Exception Running Back End Test'
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
            echo '=== Log In To Docker hub ==='
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
            echo '=== Tag & Push Rest Image ==='
                script {
                    try{
                        if (checkOs() == 'Windows') {
                            bat '''
                              docker tag devops adedo2009/devops:latest
                              docker tag devops adedo2009/devops:${BUILD_NUMBER}
                              docker push -a adedo2009/devops
                            '''
                        } else {
                            sh '''
                              docker tag devops adedo2009/devops:latest
                              docker tag devops adedo2009/devops:${BUILD_NUMBER}
                              docker push -a adedo2009/devops
                            '''
                        }
                    }catch(Exception e){
                        echo 'Exception Pushing Docker Build'
                        error('Aborting the build')
                    }
                }
            }
        }
//         stage(' Start Rest Containers ') {
//             steps {
//                echo 'Start containers using docker compose ===> '
//                script {
//                     try{
//                         if (checkOs() == 'Windows') {
//                             bat 'docker-compose -f docker-compose.yml up -d --wait'
//                             bat 'docker-compose ps'
//                         } else {
//                             echo 'docker-compose -f docker-compose.yml up -d --wait ===> '
//                             sh 'docker-compose -f docker-compose.yml up -d --wait'
//                             echo 'docker-compose -f docker-compose.yml ps ===> '
//                             sh 'docker-compose -f docker-compose.yml ps'
//                         }
//                     }catch(Exception e){
//                         echo 'Exception docker compose starting container'
//                         error('Aborting the build')
//                     }
//                 }
//             }
//         }

    }
    post {
//         always {
//         echo '=== post Clean Environment ==='
//             script {
//                 try{
//                     if (checkOs() == 'Windows') {
//                          bat '/usr/bin/python3 clean_environment.py'
//                          bat 'docker-compose -f docker-compose.yml down'
//                          bat 'docker rmi adedo2009/devops:latest'
//                          bat 'docker system prune -a --volumes -f'
//                          bat 'docker logout'
//                     } else {
//                          sh '''
//                             /usr/bin/python3 clean_environment.py
//                              sh 'docker-compose -f docker-compose.yml down --remove-orphans -v
//                              sh 'docker rmi adedo2009/devops:latest
//                              sh 'docker system prune -a --volumes -f
//                              sh 'docker logout
//                          '''
//                     }
//                 }catch(Exception e){
//                         echo 'Exception docker compose starting container'
//                         error('Aborting the build')
//                 }
//             }
//         }
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

