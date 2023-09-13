pipeline {
    agent { label 'CODE' }
    options { gitlabBuilds(builds:["Setup", "Build", "Test", "Lint", "Scan", "Artifacts", "Publish"])}
    environment {
        CI = true
        ARTIFACTORY_URL = 'https://artifactory.code.dodiis.mil/artifactory/'
        ARTIFACTORY_ACCESS_TOKEN = credentials('art-svc-cio4-zerotrustprototype-dev')
        SONAR_URL = 'https://sonarqube.code.dodiis.mil/'
        SONAR_PROJECT_KEY = 'ztp-graphql-keycloak'
        SONAR_API_KEY = credentials('sonar-ztp-global-key')
        DOCKER_USER = 'd041900'
        DOCKER_KEY = credentials('artifactory_jenkins_ci_token_fjimenez')
        DOCKER_URL ='docker.artifactory.code.dodiis.mil'
        DEV_IMAGE = '${DOCKER_URL}/cio4/zerotrustprototype/dev/ztp-backend:latest'
        PROD_IMAGE = '${DOCKER_URL}/cio4/zerotrustprototype/prod/ztp-backend:latest'
        DEV_CONT_NAME = 'ztp_backend'
        SONAR_IMAGE = "${DOCKER_URL}/cio4/zerotrustprototype/common/ztp-sonar-scanner:4.5.0"
        SONAR_CONTAINER = 'ztp_sonarscanner'
    }
    stages {
        stage('Setup') {
            steps {
                gitlabCommitStatus("Setup"){
                    catchError(stageResult: 'FAILURE') {
                        setup()
                    }
                }
            }
        }
        stage('Build Dev Image') {
            steps {
                gitlabCommitStatus("Build"){
                    catchError(stageResult: 'FAILURE') {
                        imageBuildDevImage()
                    }
                }
            }
        }
        stage('Test Dev Image') {
            steps {
                gitlabCommitStatus("Test"){
                    catchError(stageResult: 'FAILURE') {
                        runTestContainer()
                    }
                }
            }
        }
        stage('Linter') {
            steps {
                gitlabCommitStatus("Lint"){
                    catchError(stageResult: 'FAILURE') {
                        blackLinter()
                    }
                }
            }
        }
        stage('Sonarqube Scan') {
            steps {
                gitlabCommitStatus("Scan"){
                    script {
                        //use the built image to run unit test
                        def sonar_image = docker.image("${SONAR_IMAGE}")
                        sonar_image.inside {
                            sonarScan()
                        }   
                    }
                }
            }
        }
        stage('Artifacts') {
            parallel {
                stage('Skip'){
                    when {
                        not{
                            branch 'main'
                        }
                    }
                    steps{
                        updateGitlabCommitStatus name: 'Artifacts', state: 'success'
                        updateGitlabCommitStatus name: 'Publish', state: 'success'
                    }
                }
                stage('Create Artifacts') {
                    when{
                        branch 'main'
                    }
                    steps {
                        gitlabCommitStatus("Artifacts"){
                            catchError(stageResult: 'FAILURE') {
                                createArtifacts()
                            }
                        }
                    }
                }
                stage('Publish') {
                    when{
                        branch 'main'
                    }
                    steps {
                        gitlabCommitStatus("Publish"){
                            catchError(stageResult: 'FAILURE') {
                                prodBuildPublish()
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            sh """
            docker stop ${DEV_CONT_NAME} || true && docker rm ${DEV_CONT_NAME} || true && docker rmi ${DEV_IMAGE} || true
            docker stop ${SONAR_CONTAINER} || true && docker rm ${SONAR_CONTAINER} || true && docker rmi ${SONAR_IMAGE} || true
            docker rmi ${PROD_IMAGE} || true
            docker rmi ${SONAR_IMAGE} || true
            docker logout ${DOCKER_URL}
            """
        }
    }
}

// verify docker and remove (if any) existing containers and images
def setup() {
    sh  """
    docker --version
    echo ${DOCKER_KEY} | docker login ${DOCKER_URL} -u ${DOCKER_USER} --password-stdin
    echo 'Removing existing container and images if any...'
    docker stop ${DEV_CONT_NAME} || true
    docker rm ${DEV_CONT_NAME} || true
    docker rmi ${DEV_IMAGE} || true
    docker rmi ${PROD_IMAGE} || true
    """
}

// build test image
def imageBuildDevImage() {
    sh """
    echo 'Building docker image...'
    docker build -t ${DEV_IMAGE} -f Dockerfile.rootless.dev .
    sleep 5
    docker inspect ${DEV_IMAGE} | grep -i created
    """
}

// test image
def runTestContainer() {
    sh """
    echo 'Running test container...'
    docker run -d -p 8000:8000 --name ${DEV_CONT_NAME} ${DEV_IMAGE}
    docker exec ${DEV_CONT_NAME} /bin/bash -c "python --version"
    """
}

// gen docs using sphinx
def createArtifacts() {
    sh """
    echo 'Running container and generating artifacts...'
    docker exec ${DEV_CONT_NAME} /bin/bash -c "cd docs ; poetry run sphinx-quickstart --no-sep --project='ztp-graphql-keycloak' --author='ZTP Development Team' --release='1.0.0' --language='en' . ; cp template/conf.py . ; poetry run sphinx-apidoc -o . .. --ext-autodoc ; poetry run make html"
    docker exec ${DEV_CONT_NAME} /bin/bash -c "ls -l docs/_build/html"
    docker cp ${DEV_CONT_NAME}:/app/docs/_build/ ./docs
    tar czf ztp-backend_doc.tgz docs/_build/html
    curl -u ${ARTIFACTORY_ACCESS_TOKEN} -XPUT ${ARTIFACTORY_URL}ext-proj-local/cio4/zerotrustprototype/dev/ztp-backend_doc.tgz -T ztp-backend_doc.tgz
    """
    archiveArtifacts artifacts: 'docs/_build/html/*', onlyIfSuccessful: true
}

// linter check with black
def blackLinter() {
    sh """
    echo 'Linting...'
    docker exec ${DEV_CONT_NAME} /bin/bash -c 'poetry run black --check .'
    """
}

// build and push prod image
def prodBuildPublish() {
    sh """
    echo 'Building prod image...'
    docker build -t ${PROD_IMAGE} -f Dockerfile.rootless .
    docker inspect ${PROD_IMAGE} | grep -i created
    docker push ${PROD_IMAGE}
    """
}

// sonarqube scan
def sonarScan() {
    sh ''' 
    sonar-scanner \
    -Dsonar.host.url=${SONAR_URL} \
    -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
    -Dsonar.login=${SONAR_API_KEY} \
    -Dsonar.projectName=${SONAR_PROJECT_KEY} \
    -Dsonar.language=py \
    -Dsonar.python.version=3.11 \
    -Dsonar.exclusions="**/docs/_build/**/*","**.yaml" \
    -Dsonar.sourceEncoding=UTF-8 \
    -Dsonar.python.xunit.reportPath=nosetests.xml \
    -Dsonar.python.coverage.reportPaths=coverage.xml \
    | tee sonarqube-${CURRENT_TIMESTAMP}.log
    '''
    archiveArtifacts artifacts: 'sonarqube*.log', onlyIfSuccessful: false
}