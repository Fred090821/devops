pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '2', daysToKeepStr: '1'))
    }

    environment {
        registry = 'adedo2009'
        // Define environment variables here, if needed
    }

    stages {
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
         stage(' Checkout Devops Code ') {
            steps {
            echo '=== Checkout Devops Code ==='
                script {
                    properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
                }
                git 'https://github.com/Fred090821/devops.git'
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
    }
    post {
        always {
        echo '=== Clean Environment After Tests ==='
            script {
                try{
                    if (checkOs() == 'Windows') {
                        bat '''
                           /usr/bin/python3 clean_environment.py
                         '''
                    } else {
                         sh '/usr/bin/python3 clean_environment.py'
                    }
                }catch(Exception e){
                    echo 'Exception Cleaning The Environment'
                    error('Aborting The Build')
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

