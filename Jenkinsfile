/* =============================================================================
   Jenkins Declarative Pipeline — Clone GitHub Repository Stage

   Description
   -----------
   This Jenkins pipeline performs a single automated stage: cloning the
   project's GitHub repository into the Jenkins workspace. It uses the
   built-in Jenkins Git plugin and authenticates via a stored credential.

   The pipeline uses the following components:

   - agent any
       Runs the pipeline on any available Jenkins agent.

   - checkout scmGit(...)
       Performs a Git checkout using the specified branch, repository URL,
       and Jenkins credential ID.

   - credentialsId: 'github-token'
       Securely retrieves the stored GitHub Personal Access Token (PAT).

   Purpose
   -------
   This pipeline stage ensures that Jenkins always checks out the most
   up-to-date version of the repository’s `main` branch, ready for
   subsequent build, test, or deployment stages.

   Notes
   -----
   - Ensure the Jenkins credential ID `github-token` exists in:
       Jenkins → Manage Jenkins → Credentials.
   - The repository URL must be HTTPS to use token-based authentication.
   - This pipeline can be expanded with additional stages (build, test,
     docker build, deployment, etc.).
   =============================================================================
*/

pipeline {

    /* Use any available Jenkins agent */
    agent any

    stages {

        /* ---------------------------------------------------------
           Stage: Clone GitHub Repo
           Fetches the repository into the Jenkins workspace.
           --------------------------------------------------------- */
        stage('Clone GitHub Repo') {
            steps {
                script {

                    // Display progress information in Jenkins logs
                    echo 'Cloning GitHub repo to Jenkins...'

                    // Perform checkout using the Git plugin and PAT credentials
                    checkout scmGit(
                        branches: [[name: '*/main']],             // Target branch
                        extensions: [],                           // No special behaviours
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',        // PAT stored in Jenkins
                            url: 'https://github.com/Ch3rry-Pi3-AI/LLMOps-Medical-Chatbot.git'
                        ]]
                    )
                }
            }
        }
    }
}
