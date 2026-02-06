pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'valms/concilia-core'
        SCANNER_HOME = tool 'SonarScanner'
        SEMVER = "v1.0.${env.BUILD_NUMBER}"
    }

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
            }
        }

        stage('2. Build & Unit Tests') {
             steps {
                 script {
                     echo "Preparando ambiente para testes da aplicação concilia-core..."

                     def dockerfileTest = '''
                     FROM python:3.13-slim
                     WORKDIR /app
                     RUN pip install poetry && poetry config virtualenvs.create false
                     COPY pyproject.toml poetry.lock* /app/
                     RUN poetry install --no-interaction --no-root
                     COPY . /app
                     '''
                     writeFile file: 'Dockerfile.test', text: dockerfileTest

                     sh "docker build -t test-image:${env.BUILD_ID} -f Dockerfile.test ."

                     try {
                         sh "docker run --name test-container-${env.BUILD_ID} test-image:${env.BUILD_ID} \
                            poetry run pytest --cov=src --cov-report=xml:coverage.xml --cov-report=term"

                         sh "docker cp test-container-${env.BUILD_ID}:/app/coverage.xml ."

                         sh "sed -i 's|/app|${env.WORKSPACE}|g' coverage.xml"
                     } finally {
                         sh "docker rm -f test-container-${env.BUILD_ID} || true"
                         sh "docker rmi -f test-image:${env.BUILD_ID} || true"
                         sh "rm Dockerfile.test"
                     }
                 }
             }
        }

        stage('3. SonarQube Scan') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                    ${SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=concilia-core \
                    -Dsonar.python.coverage.reportPaths=coverage.xml \
                    -Dsonar.sources=src \
                    -Dsonar.tests=tests
                    """
                }
            }
        }

        stage('4. Quality Gate Approval') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('5. Trivy Repo Scan') {
            steps {
                sh "docker run --rm -v ${env.WORKSPACE}:/root aquasec/trivy fs /root --exit-code 1 --severity HIGH,CRITICAL"
            }
        }

        stage('6. Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${SEMVER} ."
                sh "docker tag ${DOCKER_IMAGE}:${SEMVER} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('7. Trivy Image Scan') {
            steps {
                sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL ${DOCKER_IMAGE}:${SEMVER}"
            }
        }

        stage('8. Create Git Tag') {
            when {
                all {
                    branch 'main'
                    expression { env.CHANGE_ID == null }
                }
            }
            steps {
                script {
                    sshagent(['github-ssh-key']) {
                        sh 'git config user.email "jenkins@ci.com" && git config user.name "Jenkins"'
                        sh "git tag -a ${SEMVER} -m 'Release ${SEMVER} - Jenkins Build'"
                        sh "git push origin ${SEMVER}"
                    }
                }
            }
        }
    }
}