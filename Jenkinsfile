pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'concilia-core'
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Baixar Código Fonte') {
            steps { checkout scm }
        }

        stage('Compilação e Testes Unitários') {
             steps {
                 script {
                     echo "Criando ambiente de teste isolado..."

                     def dockerfileTest = '''
                     FROM python:3.13-slim
                     WORKDIR /app
                     COPY . /app
                     RUN pip install poetry
                     RUN poetry config virtualenvs.create false
                     RUN poetry install --no-interaction --no-root
                     '''
                     writeFile file: 'Dockerfile.test', text: dockerfileTest

                     sh 'docker build -t imagem-teste -f Dockerfile.test .'

                     try {
                         sh 'docker run --name container-teste imagem-teste poetry run pytest --cov=src --cov-report=xml:coverage.xml --cov-report=term'

                         sh 'docker cp container-teste:/app/coverage.xml .'

                         sh "sed -i 's|/app|${env.WORKSPACE}|g' coverage.xml"
                     } finally {
                         sh 'docker rm -f container-teste || true'
                         sh 'docker rmi -f imagem-teste || true'
                         sh 'rm Dockerfile.test'
                     }
                 }
             }
        }

        stage('Análise de Código (Sonar)') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner"
                }
            }
        }

        stage('Aprovação de Qualidade') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Segurança do Repositório (Trivy FS)') {
            steps {
                sh "docker run --rm -v ${env.WORKSPACE}:/root aquasec/trivy fs /root --exit-code 1 --severity HIGH,CRITICAL"
            }
        }

        stage('Criar Imagem Docker') {
            steps {
                script {
                    def TAG = "v1.0.${env.BUILD_NUMBER}"
                    sh "docker build -t ${DOCKER_IMAGE}:${TAG} ."
                    sh "docker tag ${DOCKER_IMAGE}:${TAG} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Segurança da Imagem (Trivy)') {
            steps {
                script {
                    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 1 --severity CRITICAL ${DOCKER_IMAGE}:${GIT_COMMIT}"
                }
            }
        }

        stage('Gerar Versão (Tag Git)') {
            when {
                    expression {
                        return env.GIT_BRANCH == 'origin/main' || env.GIT_BRANCH == 'main' || env.BRANCH_NAME == 'main'
                    }
                }
            steps {
                script {
                    sh "docker tag ${DOCKER_IMAGE}:${GIT_COMMIT} ${DOCKER_IMAGE}:latest"

                    sshagent(['github-ssh-key']) {
                        sh 'git config user.email "jenkins@ci.com" && git config user.name "Jenkins"'
                        def TAG = "v1.0.${env.BUILD_NUMBER}"

                        sh 'mkdir -p ~/.ssh && touch ~/.ssh/known_hosts'
                        sh 'ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts'
                        sh "git tag -a ${TAG} -m 'Jenkins Build'"
                        sh "git push git@github.com:valms/trabalho-ci-cd.git ${TAG}"
                    }
                }
            }
        }
    }
}