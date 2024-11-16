pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  securityContext:
                    runAsUser: 1000
                    runAsGroup: 1000
                    fsGroup: 1000
                  containers:
                  - name: python
                    image: python:3.11-slim
                    command:
                    - cat
                    tty: true
                    resources:
                      limits:
                        memory: "512Mi"
                        cpu: "500m"
                  - name: docker
                    image: docker:dind
                    securityContext:
                      privileged: false
                    volumeMounts:
                    - name: docker-socket
                      mountPath: /var/run/docker.sock
                  volumes:
                  - name: docker-socket
                    hostPath:
                      path: /var/run/docker.sock
            '''
        }
    }

    environment {
        VAULT_ADDR = credentials('vault-addr')
        VAULT_ROLE_ID = credentials('vault-role-id')
        VAULT_SECRET_ID = credentials('vault-secret-id')
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Setup') {
            steps {
                container('python') {
                    sh 'pip install poetry'
                    sh 'poetry install'
                }
            }
        }

        stage('Security Scan') {
            parallel {
                stage('Dependencies') {
                    steps {
                        container('python') {
                            sh 'poetry export -f requirements.txt | safety check'
                            sh 'poetry run bandit -r src/'
                        }
                    }
                }

                stage('SAST') {
                    steps {
                        container('python') {
                            sh 'poetry run pylint src/'
                        }
                    }
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        container('python') {
                            sh '''
                                poetry run pytest tests/unit \
                                    --junitxml=test-results/unit-tests.xml \
                                    --cov=src \
                                    --cov-report=xml:coverage.xml
                            '''
                        }
                    }
                }

                stage('Integration Tests') {
                    steps {
                        container('python') {
                            sh 'poetry run pytest tests/integration'
                        }
                    }
                }
            }
        }

        stage('Build & Scan Image') {
            steps {
                container('docker') {
                    script {
                        def image = docker.build("${DOCKER_IMAGE}:${GIT_COMMIT}", "-f Dockerfile.multistage .")

                        // Scan image for vulnerabilities
                        sh "trivy image ${DOCKER_IMAGE}:${GIT_COMMIT}"

                        // Sign image
                        sh "cosign sign ${DOCKER_IMAGE}:${GIT_COMMIT}"
                    }
                }
            }
        }

        stage('Deploy to Dev') {
            when { branch 'develop' }
            steps {
                script {
                    // Get secrets from Vault
                    withVault(
                        vaultSecrets: [[
                            path: 'secret/dev/python-app',
                            secretValues: [[envVar: 'API_KEY', vaultKey: 'api-key']]
                        ]]
                    ) {
                        // Update Helm values
                        sh '''
                            helm upgrade --install python-app ./deployments/helm/python-app \
                                --namespace dev \
                                --set image.tag=${GIT_COMMIT} \
                                --set secrets.apiKey=${API_KEY} \
                                --wait
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            junit 'test-results/**/*.xml'
            recordIssues(tools: [pylint(pattern: 'pylint.log')])
            recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']])

            // Clean workspace
            cleanWs()
        }
        success {
            script {
                if (env.BRANCH_NAME == 'main') {
                    // Trigger ArgoCD sync
                    sh 'argocd app sync python-app'
                }
            }
        }
    }
}
