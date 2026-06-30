pipeline {
    // This tells Jenkins it can run on any available Jenkins agent/node
    agent any

    // We can define variables here to make our code cleaner
    environment {
        PYTHON = 'python' // On some systems this might be 'python3'
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
                    pip install --upgrade pip
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
                    pytest -m api -v --html=reports/api_report.html
                """
            }
        }

        // STAGE 4: Run the UI tests
        stage('Run UI Tests') {
            steps {
                echo "Running UI Test Suite..."
                bat """
                    call venv\\Scripts\\activate.bat
                    pytest -m ui -v --html=reports/ui_report.html
                """
            }
        }
    }

    // This block runs after all stages finish, regardless of success or failure
    post {
        always {
            echo "Pipeline finished! Cleaning up..."
            // In a real project, we might archive the HTML reports here
            archiveArtifacts artifacts: 'reports/*.html', allowEmptyArchive: true
        }
        success {
            echo "✅ ALL TESTS PASSED! Ready for deployment!"
        }
        failure {
            echo "❌ TESTS FAILED! Sending alert to development team!"
        }
    }
}
