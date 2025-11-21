/* =============================================================================
   Jenkins Declarative Pipeline — AWS ECR Build, Scan, Push, and App Runner Deploy

   Description
   -----------
   This Jenkins pipeline performs three major CI/CD operations:

   1. Clone GitHub Repository
      Fetches the latest project code from the `main` branch using secure
      GitHub credentials stored in Jenkins.

   2. Build, Scan, and Push Docker Image to AWS ECR
      - Authenticates with AWS using Jenkins credentials
      - Builds a Docker image from the repository
      - Scans the image using Trivy (HIGH + CRITICAL severity)
      - Tags the image using the 'latest' tag
      - Pushes the image to AWS Elastic Container Registry (ECR)
      - Stores the vulnerability report as a Jenkins artifact

   3. Deploy Latest Image to AWS App Runner
      - Locates the App Runner service by name
      - Retrieves its ARN programmatically
      - Triggers a new deployment so App Runner pulls the updated ECR image

   Environment Variables
   ---------------------
   AWS_REGION   : AWS region for ECR and App Runner (e.g., eu-west-2)
   ECR_REPO     : Name of the ECR repository
   IMAGE_TAG    : Tag applied to the Docker image (e.g., latest)
   SERVICE_NAME : Name of the App Runner service to update

   Requirements
   ------------
   - Jenkins instance must run in a Docker-enabled environment
   - Jenkins container must have AWS CLI installed
   - Jenkins container must have Trivy installed
   - Jenkins credentials:
       * github-token  → GitHub Personal Access Token
       * aws-token     → IAM Access Key + Secret Key

   Notes
   -----
   - Trivy is non-blocking to prevent pipeline failures (`|| true`)
   - App Runner deployment is triggered manually via `start-deployment`
   - Future stages can extend this pipeline with ECS/EKS deployment
   =============================================================================
*/

pipeline {

    /* Run pipeline on any available Jenkins agent */
    agent any

    /* Shared environment variables */
    environment {
        AWS_REGION   = 'eu-west-2'
        ECR_REPO     = 'my-repo'
        IMAGE_TAG    = 'latest'
        SERVICE_NAME = 'llmops-medical-service'
    }

    stages {

        /* --------------------------------------------------------------
           Stage: Clone GitHub Repo
           Securely checks out the main branch of the repository.
           -------------------------------------------------------------- */
        stage('Clone GitHub Repo') {
            steps {
                script {

                    // Print progress message
                    echo 'Cloning GitHub repo to Jenkins...'

                    // Secure Git checkout with PAT stored in Jenkins credentials
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/Ch3rry-Pi3-AI/LLMOps-Medical-Chatbot.git'
                        ]]
                    )
                }
            }
        }

        /* --------------------------------------------------------------------
           Stage: Build, Scan, and Push Docker Image to ECR
           Uses AWS credentials to authenticate, build, scan, tag, and push the
           image into AWS Elastic Container Registry.
           -------------------------------------------------------------------- */
        stage('Build, Scan, and Push Docker Image to ECR') {
            steps {

                // Attach AWS credentials for CLI usage
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {

                        // Query AWS account ID
                        def accountId = sh(
                            script: "aws sts get-caller-identity --query Account --output text",
                            returnStdout: true
                        ).trim()

                        // Construct base ECR URL
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

                        // Full image tag
                        def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                        // Build, scan, tag, and push Docker image
                        sh """
                        # Authenticate Docker to AWS ECR
                        aws ecr get-login-password --region ${AWS_REGION} \
                            | docker login --username AWS --password-stdin ${ecrUrl}

                        # Build the container image
                        docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .

                        # Run vulnerability scan (non-blocking)
                        trivy image --severity HIGH,CRITICAL --format json \
                            -o trivy-report.json ${env.ECR_REPO}:${IMAGE_TAG} || true

                        # Tag the image for ECR
                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${imageFullTag}

                        # Push to AWS ECR
                        docker push ${imageFullTag}
                        """

                        // Store the Trivy report in Jenkins
                        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                    }
                }
            }
        }

        /* --------------------------------------------------------------------
           Stage: Deploy to AWS App Runner
           Triggers a new deployment for an existing App Runner service so that
           it pulls the freshly updated container image from ECR.
           -------------------------------------------------------------------- */
        stage('Deploy to AWS App Runner') {
            steps {

                // Use AWS credentials again for App Runner API calls
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {

                        // Query AWS account ID
                        def accountId = sh(
                            script: "aws sts get-caller-identity --query Account --output text",
                            returnStdout: true
                        ).trim()

                        // Construct repository URL
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                        def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                        // Info message for Jenkins logs
                        echo "Triggering deployment to AWS App Runner..."

                        // Trigger new deployment on App Runner
                        sh """
                        # Fetch the App Runner service ARN by name
                        SERVICE_ARN=\$(aws apprunner list-services \
                            --query "ServiceSummaryList[?ServiceName=='${SERVICE_NAME}'].ServiceArn" \
                            --output text \
                            --region ${AWS_REGION})

                        echo "Found App Runner Service ARN: \$SERVICE_ARN"

                        # Start a new deployment
                        aws apprunner start-deployment \
                            --service-arn \$SERVICE_ARN \
                            --region ${AWS_REGION}
                        """
                    }
                }
            }
        }
    }
}
