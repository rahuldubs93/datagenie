#!/usr/bin/env groovy

// Deployment environment variables.
envParamsMap = [
    prod : [
        go: [
            agentLabel : 'app-prod',
            env : 'go',
            jenkins_aws_profile: 'app-data-science-prod',
            ECR_IMAGE: '491600578599.dkr.ecr.us-east-1.amazonaws.com/zdt/datagenie/api'
        ],
        main: [
            agentLabel : 'app-prod',
            env : 'prod',
            jenkins_aws_profile: 'app-data-science-prod',
            ECR_IMAGE: '491600578599.dkr.ecr.us-east-1.amazonaws.com/zdt/datagenie/api'
        ]
    ]
]
// Determine which Jenkins instance we are running on. Results can be nonprod and prod.
jenkinsInstanceName = getJenkinsEnv()

// Set a default deployment environment based on the Jenkins instance.
defaultEnvMap = [prod: 'prod']
defaultEnvName = defaultEnvMap[jenkinsInstanceName]

// Determine the actual deployment environment based on the branch name.
envParams = envParamsMap[jenkinsInstanceName].get(env.BRANCH_NAME, envParamsMap[jenkinsInstanceName][defaultEnvName])

// Kubernetes configuration
kubernetes_configuration = [
    spec: [
        containers: [
            [
                name: 'terraform',
                image: 'hashicorp/terraform:1.4.6',
                command: ['sleep'],
                args: ['1d'],
                env: [
                    [name: 'HOME', value: '/home/jenkins/agent'],
                    [name: 'GIT_SSH_COMMAND', value: 'ssh -i /home/jenkins/agent/.ssh/id_rsa -o UserKnownHostsFile=/home/jenkins/agent/.ssh/known_hosts']
                ]
            ]
        ]
    ]
]

pipeline {
    agent {
        kubernetes {
            cloud envParams['agentLabel']
            inheritFrom envParams['agentLabel']
        }
    }
    environment{
        JENKINS_AWS_PROFILE = "${envParams['jenkins_aws_profile']}"
        ECR_IMAGE = "${envParams['ECR_IMAGE']}"
        ENV = "${envParams['env']}"
    }
    parameters {
        string(name: 'TF_VAR_image_tag', defaultValue: '0.0.1-pre.18', description: 'Enter the image tag.')
    }


    stages {
        stage ('Pull and Push Docker') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'artifacts.corp.zoom.us-readonly', url: 'https://artifacts.corp.zoom.us/') {
                      sh 'docker pull artifacts.corp.zoom.us/datasci-docker-dev/zdt/platform/zdt_datagenie:${TF_VAR_image_tag}'
                      sh '''
                        aws ecr get-login-password --profile ${JENKINS_AWS_PROFILE} | docker login --username=AWS --password-stdin ${ECR_IMAGE}
                        docker tag "artifacts.corp.zoom.us/datasci-docker-dev/zdt/platform/zdt_datagenie:${TF_VAR_image_tag}" "${ECR_IMAGE}:${TF_VAR_image_tag}"
                        docker push "${ECR_IMAGE}:${TF_VAR_image_tag}"

                    '''
  
                    }
                }
            }
        }
        stage('terraform-apply') {           
            when {
                equals expected: env.BRANCH_NAME, actual: envParams['env']
            }
            agent {
                kubernetes {
                    cloud envParams['agentLabel']
                    inheritFrom envParams['agentLabel']
                    yaml writeYaml(returnText: true, data: kubernetes_configuration)
                }
            } 
            steps {
                container('terraform') {
                    dir("infra") {
                        script {
                            sh "terraform init -backend-config tfenv/${envParams['env']}/backend.hcl -no-color"
                            sh "terraform apply -var-file tfenv/${envParams['env']}/vars.tfvars --auto-approve -no-color"
                            echo "running post apply check of configuration integrity."
                            sh "terraform plan -var-file tfenv/${envParams['env']}/vars.tfvars -detailed-exitcode -no-color || ( echo 'A permanent difference exists after apply. This indicates collisions within the terraform configuration.' ; exit 1)"
                        }
                    }
                }
            }
        }
    }
}
