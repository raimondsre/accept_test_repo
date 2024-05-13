#!/usr/bin/env nextflow
project_dir = projectDir

process writeToFile {
    executor = 'local'
    maxForks = 1

    input:
    file 'input'

    script:
    """
    cat ${input} > ${projectDir}/output/output.json
    """
}

process demo {
    executor = 'local'
    maxForks = 1

    output:
    stdout

    script:
    """
    source ${project_dir}/venv/bin/activate && python ${projectDir}/demo.py ${project_dir}
    """
}

workflow {
    demo | collect | writeToFile
}

workflow.onComplete {
    println "Pipeline completed at: $workflow.complete"
    println "Execution status: ${ workflow.success ? 'OK' : 'failed' }"

    def proc = "${project_dir}/completed.sh".execute()
    def b = new StringBuffer()
    proc.consumeProcessErrorStream(b)
    println proc.text
    println b.toString()
}

workflow.onError {
    println "Error: Pipeline execution stopped with the following message: ${workflow.errorMessage}"

    def proc = "${project_dir}/failed.sh".execute()
    def b = new StringBuffer()
    proc.consumeProcessErrorStream(b)
    println proc.text
    println b.toString()
}