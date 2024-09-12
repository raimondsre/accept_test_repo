#!/usr/bin/env nextflow
project_dir = projectDir

//Run this script to notify the platform that task execution has started
def startProc = "${project_dir}/started.sh".execute()
def sb = new StringBuffer()
startProc.consumeProcessErrorStream(sb)
println startProc.text
println sb.toString()

process writeToFile {
    executor = 'local'
//     maxForks = 1

    input:
    file 'input'

    script:
    """
    cat ${input} > ${projectDir}/output/output.json
    """
}

process demo {
    executor = 'local'
//     maxForks = 3

    output:
    stdout

    script:
    """
    source ${project_dir}/venv/bin/activate && python ${projectDir}/demo.py ${project_dir}
    """
}

workflow {
    demo | writeToFile
}

workflow.onComplete {
    println "Pipeline completed at: $workflow.complete"
    println "Execution status: ${ workflow.success ? 'OK' : 'failed' }"
    f = new File("${projectDir}/status.txt")
    f.append("\nPipeline completed at: $workflow.complete")
    f.append("\nExecution status: ${ workflow.success ? 'OK' : 'failed' }")

    def proc = "${project_dir}/completed.sh".execute()
    def b = new StringBuffer()
    proc.consumeProcessErrorStream(b)
    println proc.text
    println b.toString()
}

workflow.onError {
    println "Error: Pipeline execution stopped with the following message: ${workflow.errorMessage}"
    f = new File("${projectDir}/status.txt")
    f.append("\nError: Pipeline execution stopped with the following message: ${workflow.errorMessage}")

    def proc = "${project_dir}/failed.sh".execute()
    def b = new StringBuffer()
    proc.consumeProcessErrorStream(b)
    println proc.text
    println b.toString()
}