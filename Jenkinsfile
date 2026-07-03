pipeline {
    // We force Jenkins to run the entire job on the D: drive to save your C: drive!
    agent {
        node {
            label '' // Empty label tells Jenkins to run on ANY available node
            customWorkspace 'D:\\Jenkins\\workspace\\Simple-Automation'
        }
    }

    // ── SCHEDULED NIGHTLY BUILD ──
    // Uncomment the block below to run the tests automatically every night at midnight!
    triggers {
        cron('H 0 * * *')
    }

    // We can define variables here to make our code cleaner
    environment {
        // We must use the absolute path because Jenkins runs as LocalSystem
        // and doesn't know where Python is installed on your computer!
        PYTHON = '"C:\\Users\\CHANDRA SHEKAR\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"'
    }

    stages {
        // STAGE 1: Jenkins automatically pulls the code from GitHub before this block starts.
        // We just print a message to verify we have the code.
        stage('Checkout & Verify') {
            steps {
                echo "Code successfully pulled from GitHub!"
                // Windows batch command to list files to prove we are in the right place
                bat 'dir' 
            }
        }

        // STAGE 2: Set up the Python environment and install dependencies
        stage('Setup Environment') {
            steps {
                echo "Setting up Python Virtual Environment..."
                // Using 'bat' because Jenkins will be running on your Windows laptop
                bat """
                    ${PYTHON} -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                """
            }
        }

        // STAGE 3: Run the API tests
        stage('Run API Tests') {
            steps {
                echo "Running API Test Suite..."
                bat """
                    call venv\\Scripts\\activate.bat
                    pytest -m api -v --alluredir=allure-results
                """
            }
        }

        // STAGE 4: Run the UI tests
        stage('Run UI Tests') {
            steps {
                echo "Running UI Test Suite..."
                bat """
                    call venv\\Scripts\\activate.bat
                    pytest -m ui -v --alluredir=allure-results
                """
            }
        }
    }

    // This block runs after all stages finish, regardless of success or failure
    post {
        always {
            echo "Pipeline finished! Generating Allure Report..."
            // This 'allure' step requires the Allure Jenkins Plugin to be installed!
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
        success {
            echo "✅ ALL TESTS PASSED! Ready for deployment!"
        }
        failure {
            echo "❌ TESTS FAILED! Sending alert to development team!"
            // To make this work, you must configure the SMTP server in Manage Jenkins -> System
            mail to: 'adelli.chandrashekar@gmail.com',
                 subject: "Pipeline Failed: ${env.JOB_NAME} Build #${env.BUILD_NUMBER}",
                 body: "The nightly automation suite has failed. Please check the Allure Report!"
        }
    }
}
