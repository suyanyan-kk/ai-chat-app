pipeline {
    agent any

    environment {
        DEPLOY_BRANCH = 'main'

        DEPLOY_HOST = '101.42.13.233'
        DEPLOY_USER = 'ubuntu'
        DEPLOY_DIR = '/opt/AI_PY_Project'

        SSH_CREDENTIALS_ID = 'yanaihub-server-ssh-key'
    }

    stages {
        stage('Check Branch') {
            steps {
                script {
                    def currentBranch = env.BRANCH_NAME

                    if (!currentBranch && env.GIT_BRANCH) {
                        currentBranch = env.GIT_BRANCH.replaceFirst(/^origin\//, '')
                    }

                    echo "Current branch: ${currentBranch}"
                    echo "Deploy branch: ${DEPLOY_BRANCH}"

                    if (currentBranch != DEPLOY_BRANCH) {
                        error("当前分支 ${currentBranch} 不是上线分支 ${DEPLOY_BRANCH}，禁止部署。")
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Show Git Info') {
            steps {
                sh '''
                    echo "===== Git Commit ====="
                    git log -1 --oneline

                    echo "===== Git Status ====="
                    git status --short
                '''
            }
        }

        stage('Upload Code To Server') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh '''
                        rsync -avz --delete \
                          -e "ssh -o StrictHostKeyChecking=accept-new" \
                          --exclude '.git' \
                          --exclude '.venv' \
                          --exclude '__pycache__' \
                          --exclude '.DS_Store' \
                          --exclude '.env' \
                          --exclude '.env.*' \
                          --exclude 'chroma_db' \
                          --exclude 'data' \
                          --exclude 'logs' \
                          --exclude 'uploads' \
                          --exclude 'node_modules' \
                          --exclude 'dist' \
                          --exclude 'mcp_workspace' \
                          ./ ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}/
                    '''
                }
            }
        }

        stage('Deploy With Docker Compose') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=accept-new ${DEPLOY_USER}@${DEPLOY_HOST} "
                            cd ${DEPLOY_DIR} && \
                            docker compose -f docker-compose.prod.yml build --progress=plain backend && \
                            docker compose -f docker-compose.prod.yml build --progress=plain frontend && \
                            docker compose -f docker-compose.prod.yml up -d && \
                            docker compose -f docker-compose.prod.yml ps
                        "
                    '''
                }
            }
        }

        stage('Health Check') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=accept-new ${DEPLOY_USER}@${DEPLOY_HOST} "
                            curl -I http://127.0.0.1 && \
                            curl -I http://127.0.0.1/api/docs
                        "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deploy success.'
        }

        failure {
            echo 'Deploy failed. Check Jenkins console logs and server docker logs.'
        }
    }
}
EOF