pipeline {
    agent any

    environment {
        VENV_DIR      = '.venv'
        ALLURE_RESULTS = 'allure-results'
        HEADLESS      = 'true'   // Forces Playwright to run headless in CI
    }

    stages {

        // ─────────────────────────────────────────────
        // 1. Pull source code
        // ─────────────────────────────────────────────
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ─────────────────────────────────────────────
        // 2. Create venv & install Python dependencies
        // ─────────────────────────────────────────────
        stage('Setup Python Environment') {
            steps {
                bat 'python -m venv %VENV_DIR%'
                bat '%VENV_DIR%\\Scripts\\pip install --upgrade pip'
                bat '%VENV_DIR%\\Scripts\\pip install -r requirements.txt'
            }
        }

        // ─────────────────────────────────────────────
        // 3. Install Playwright browsers
        // ─────────────────────────────────────────────
        stage('Install Playwright Browsers') {
            steps {
                bat '%VENV_DIR%\\Scripts\\playwright install chromium'
            }
        }

        // ─────────────────────────────────────────────
        // 4. Run pytest and generate Allure results
        // ─────────────────────────────────────────────
        stage('Run Tests') {
            steps {
                bat '''
                    %VENV_DIR%\\Scripts\\pytest ^
                        --alluredir=%ALLURE_RESULTS% ^
                        -v ^
                        --tb=short
                '''
            }
        }
    }

    // ─────────────────────────────────────────────
    // Post-build: always publish Allure report
    // ─────────────────────────────────────────────
    post {
        always {
            allure([
                includeProperties: false,
                jdk              : '',
                results          : [[path: "${env.ALLURE_RESULTS}"]]
            ])

            archiveArtifacts(
                artifacts        : 'screenshot/**',
                allowEmptyArchive: true
            )
        }
        success {
            echo 'All tests passed.'
        }
        failure {
            echo 'One or more tests failed. Check the Allure report for details.'
        }
    }
}
