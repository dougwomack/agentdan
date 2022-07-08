pipeline {
  agent any
  stages {
    stage('Pull Application') {
      steps {
        sh 'echo "Check out base application source!"'
      }
    }

    stage('Build IaC') {
      parallel {
        stage('Build IaC') {
          steps {
            sh 'echo "Build IaC and write attributes to Consul!"'
            sh 'echo "Update ServiceNow CMDB"'
            sh '''echo "Check OpsView for prior execution and update an existing resource, or create new!"
echo "Associate with proper profile for service type!"'''
            sh '''echo "Check Dynatrace for prior execution and update an existing resource, or create new!"
echo "Associate with proper profile for service type!"'''
            sh 'echo "Setup log forwarder to Splunk!"'
            sh 'echo "Add/Update DNS with appropriate A/CNAME records!"'
          }
        }

        stage('Build Mulesoft') {
          steps {
            sh '''echo "Build Mulesoft component and write attributes to Consul!"
'''
          }
        }

        stage('Build Pega') {
          steps {
            sh 'echo "Build Pega component and write attributes to Consul!"'
          }
        }

      }
    }

  }
}