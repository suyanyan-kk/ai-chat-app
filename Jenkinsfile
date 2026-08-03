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
                        error(
                            "当前分支 ${currentBranch} 不是上线分支 ${DEPLOY_BRANCH}，禁止部署。"
                        )
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


        stage('Validate Deploy Config') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=accept-new \
                          ${DEPLOY_USER}@${DEPLOY_HOST} "
                            cd ${DEPLOY_DIR} && \
                            test -f .env.production && \
                            test -f ai-service/.env.production && \
                            sudo -n docker compose \
                              --env-file .env.production \
                              -f docker-compose.yml \
                              config > /dev/null
                        "
                    '''
                }
            }
        }


        stage('Deploy With Docker Compose') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=accept-new \
                          ${DEPLOY_USER}@${DEPLOY_HOST} "
                            cd ${DEPLOY_DIR} && \
                            sudo -n docker compose \
                              --env-file .env.production \
                              -f docker-compose.yml \
                              build --progress=plain backend && \
                            sudo -n docker compose \
                              --env-file .env.production \
                              -f docker-compose.yml \
                              build --progress=plain frontend && \
                            sudo -n docker compose \
                              --env-file .env.production \
                              -f docker-compose.yml \
                              up -d && \
                            sudo -n docker compose \
                              --env-file .env.production \
                              -f docker-compose.yml \
                              ps
                        "
                    '''
                }
            }
        }


        stage('Validate Caddy') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=accept-new \
                          ${DEPLOY_USER}@${DEPLOY_HOST} "
                            cd ${DEPLOY_DIR} && \
                            sudo -n docker exec ai_caddy \
                              caddy validate \
                              --config /etc/caddy/Caddyfile
                        "
                    '''
                }
            }
        }


        stage('Health Check') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=accept-new \
                          ${DEPLOY_USER}@${DEPLOY_HOST} '
                            echo "===== Waiting For HTTPS ====="

                            for i in $(seq 1 12); do

                                if curl \
                                  --fail \
                                  --silent \
                                  --show-error \
                                  --resolve yanaihub.cn:443:127.0.0.1 \
                                  https://yanaihub.cn/ \
                                  -o /dev/null; then

                                    echo "Frontend HTTPS health check passed."
                                    break
                                fi

                                if [ "$i" -eq 12 ]; then
                                    echo "Frontend HTTPS health check failed."
                                    exit 1
                                fi

                                echo "HTTPS not ready yet. Retry $i/12..."
                                sleep 5
                            done


                            echo "===== API Health Check ====="

                            curl \
                              --fail \
                              --silent \
                              --show-error \
                              --resolve yanaihub.cn:443:127.0.0.1 \
                              https://yanaihub.cn/api/docs \
                              -o /dev/null

                            echo "API HTTPS health check passed."
                        '
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