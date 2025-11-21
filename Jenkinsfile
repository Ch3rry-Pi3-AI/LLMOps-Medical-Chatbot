/* =============================================================================
   Jenkins Declarative Pipeline — AWS ECR Build, Scan, and Push

   Description
   -----------
   This Jenkins pipeline performs two major CI/CD tasks:

   1. Clone GitHub Repository
      Retrieves the latest project code from the `main` branch using secure
      GitHub credentials stored in Jenkins.

   2. Build, Scan, and Push Docker Image to AWS ECR
      - Authenticates with AWS using Jenkins credentials
      - Builds a Docker image from the repository
      - Scans the image using Trivy for HIGH and CRITICAL vulnerabilities
      - Tags the image with 'latest' and pushes it to ECR
      - Archives the Trivy report as a Jenkins build artifact

   Environment Variables
   ---------------------
   AWS_REGION   : AWS region where ECR is hosted (e.g., eu-west-2)
   ECR_REPO     : Name of the repository inside AWS ECR
   IMAGE_TAG    : Image tag applied to the build (e.g., latest)
   SERVICE_NAME : Name of the downstream service (if used for deployment)

   Requirements
   ------------
   - Jenkins must be running inside a Docker-enabled environment
   - AWS CLI installed inside the Jenkins agent
   - Trivy installed inside the Jenkins agent
   - Jenkins credentials:
       * github-token  → GitHub PAT for repository access
       * aws-token     → AWS credential for ECR authentication

   Notes
   -----
   - Trivy scan is allowed to fail gracefully (using `|| true`) to prevent
     blocking the pipeline while still producing a report.
   - This pipeline can be expanded with deployment stages (ECS, EKS, Lambda, etc.).
   =============================================================================
*/

pipeline {

    /* Allow Jenkins to run the pipeline on any available agent */
    agent any

    /* Define environment variables for AWS and ECR usage */
    environment {
        AWS_REGION   = 'eu-west-2'
        ECR_REPO     = 'my-repo'
        IMAGE_TAG    = 'latest'
        SERVICE_NAME = 'llmops-medical-service'
    }

    stages {

        /* --------------------------------------------------------------
           Stage: Clone GitHub Repo
           Pulls the project source code using the Git SCM plugin.
           -------------------------------------------------------------- */
        stage('Clone GitHub Repo') {
            steps {
                script {

                    // Log progress to Jenkins console
                    echo 'Cloning GitHub repo to Jenkins...'

                    // Perform a secure checkout of the main branch
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
           Uses AWS credentials to authenticate, build, scan, tag, and push
           the Docker image to AWS Elastic Container Registry.
           -------------------------------------------------------------------- */
        stage('Build, Scan, and Push Docker Image to ECR') {
            steps {

                // Attach AWS credentials securely during this stage
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {

                        // Retrieve AWS account ID from STS
                        def accountId = sh(
                            script: "aws sts get-caller-identity --query Account --output text",
                            returnStdout: true
                        ).trim()

                        // Construct ECR URL (e.g., 123456789012.dkr.ecr.eu-west-2.amazonaws.com/my-repo)
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

                        // Full image tag (e.g., .../my-repo:latest)
                        def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                        // Build, scan, tag, and push Docker image
                        sh """
                        # Authenticate Docker with AWS ECR
                        aws ecr get-login-password --region ${AWS_REGION} \
                            | docker login --username AWS --password-stdin ${ecrUrl}

                        # Build local Docker image
                        docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .

                        # Run vulnerability scan (non-blocking)
                        trivy image --severity HIGH,CRITICAL --format json \
                            -o trivy-report.json ${env.ECR_REPO}:${IMAGE_TAG} || true

                        # Tag image for ECR
                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${imageFullTag}

                        # Push image to AWS ECR
                        docker push ${imageFullTag}
                        """

                        // Archive the Trivy scan report even if empty
                        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                    }
                }
            }
        }
    }
}
