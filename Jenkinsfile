pipeline {
    agent any
    environment {
        PATH = 'jonnyfb421/horoscope-scraper'
        IMAGE_NAME = 'jonnyfb421/horoscope-scraper'
        VERSION = sh(script:"cat ./version.txt", returnStdout: true)
        IMAGE_TAG = '$IMAGE_NAME:$VERSION'
    }
    stages {
            stage('Checkout SCM') {
                steps {
                    checkout scm
                }
            }
            stage('Running tests') {
                agent { dockerfile true }
                steps {
                    sh "pip install --user .[dev]"
                    sh "py.test --cov=horoscope_scraper --cov-report xml --junitxml=junit-results.xml tests/"
                }
            }
            stage('Bump version') {
                when { branch 'master' }
                agent { dockerfile true }
                steps {
                    script {
                        sh "pip install --upgrade --user bumpversion"
                        sh "git stash; git checkout master; git pull"
                        sh "bumpversion patch"
                        sh "git push origin master"
                    }
                }
            }
            stage('Push production image') {
                when { branch 'master' }
                steps {
                    script {
                        withDockerRegistry([ credentialsId: "dockerhub-creds", url: "" ]) {
                            docker.build("${IMAGE_TAG}").push()
                        }
                    }
                }
            }
            stage('Deploying the new version') {
                when { branch 'master' }
                steps {
                    script {
                        withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'ssh-ec2-horoscope-scraper', \
                                                                     keyFileVariable: 'SSH_KEY')]) {
                            def running_container = sh (script: "ssh -oStrictHostKeyChecking=no -i ~/.ssh/jonny.pem ec2-user@52.14.201.238 sudo docker ps -qf \"label=$IMAGE_NAME\"", returnStdout: true)
                            if (running_container) {
                                sh "ssh -oStrictHostKeyChecking=no -i ~/.ssh/jonny.pem ec2-user@52.14.201.238 sudo docker kill ${running_container}"
                            }
                            sh "ssh -oStrictHostKeyChecking=no -i ~/.ssh/jonny.pem ec2-user@52.14.201.238 sudo docker run -d -p 80:5000 -l $IMAGE_NAME $IMAGE_TAG"
                        }
                    }
                }
            }
        }
    post {
        always {
            deleteDir()
        }
    }
}
