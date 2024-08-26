

pipeline{
    agent any

// this will disable the automatic checkout
    options {
        skipDefaultCheckout true
    }

    parameters {
        string(name: 'app_version', defaultValue: '', description: 'Application Version to build')
    }

// Setting up fixed values as environmental variables 
    environment {
        NEXUS_URL = "192.168.0.104:8082"
    }

    stages {

    // Git Checkout 

        stage ('Git-Checkout') {
            steps {
                git credentialsId: 'git', poll: false, url: 'https://github.com/aditya-tanwar/Dynamic-Microservice-Pipeline.git', branch: env.BRANCH_NAME
            }
        }

// Trivy Filesystem Scanning 

        stage ('Trivy-File-System-Scanning') {
            steps {
                sh 'trivy fs . --format json --output trivy-results.json'
            }
        }

// Dependency Check 

        stage ('Dependency-Check') {
            steps {
                dependencyCheck additionalArguments: '--scan ./', odcInstallation: 'owasp'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }


// Dynamic Pipelines         
        
        stage ('Dynamic Pipeline') {
            steps {
                script {
                    def microservices = readFile('components').split('\n')
                    def parallelStages = [:]

                    microservices.each { microservice ->
                        parallelStages["${microservice}"] = {
                            stage ("${microservice}") {
                                echo "${microservice}"
                                //script{

                                    // stage ("Docker-Image-Build") {
                                    //     echo "build"
                                    //     sh "ls && pwd"
                                    //     sh "docker build -t ${microservice}-`date +'%F'`:v1 src/${microservice}/"

                                    // }

                                    // stage ("Docker-Image-Scan") {
                                    //     sh '''
                                    //         trivy image --scanners vuln,misconfig,secret ${microservice}-$(date +"%F"):v${app_version} --format json -o TEST-RESULTS/trivy-${microservice}-$(date +"%F")-v${app_version}.json
                                    //         dockle -f json ${microservice}-$(date +"%F"):v${app_version} > TEST-RESULTS/dockle-${microservice}-$(date +"%F")-v${app_version}.json

                                    //     '''
                                    // }

                                    // stage ("Taggin & Pushing Image") {
                                    //     sh '''
                                    //         if [ $( cat TEST-RESULTS/dockle-log-${microservice}-$(date +"%F")-v${app_version}.json | jq -r '.summary.fatal' ) -lt 3 ]; then
                                    //             docker tag ${microservice}-$(date +"%F"):v${app_version} adityatanwar03/${microservice}-$(date +"%F"):v${app_version}
                                    //             docker push adityatanwar03/${microservice}-$(date +"%F"):v${app_version}
                                    //         else
                                    //             echo "Docker image build failed , Please check the trivy and Dockle reports for troubleshooting"
                                    //         fi
                                    //     '''
                                    //     sh "echo 'Pushing image to docker hosted rerpository on Docker'"

                                    //     //withCredentials([usernamePassword(credentialsId: 'nexuslogin', passwordVariable: 'PSW', usernameVariable: 'USER')]){
                                    //     //sh "echo ${PSW} | docker login -u ${USER} --password-stdin ${NEXUS_URL}"
                                    //     //sh 'docker push ${NEXUS_URL}/log-message-processor-$(date +"%F"):v${app_version}'
                                    //     //}   
                                    // }
                                //}
                            }
                        }
                        
                    }
                    parallel parallelStages
                }
            }
        } // End of Dynamic Pipeline stage


    }
}
