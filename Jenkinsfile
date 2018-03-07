
node {        
        stage 'Cleanup workspace'
        sh 'chmod 777 -R .'
        sh 'rm -rf *'
   
        
        stage 'Build .whl & .deb'
            sh 'fpm -s python -t deb .'
            sh 'python setup.py bdist_wheel'
            sh 'mv *.deb dist/'

        stage 'Archive build artifact: .whl & .deb'
            archive 'dist/*'

        stage 'Trigger downstream publish'
            build job: 'publish-local', parameters: [
                string(name: 'artifact_source', value: "${currentBuild.absoluteUrl}/artifact/dist/*zip*/dist.zip"),
                string(name: 'source_branch', value: "${env.BRANCH_NAME}")]
}
