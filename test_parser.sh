#!/bin/bash
#set -euo pipefail
set -uo

now=$(date +'%s')

make_1_case_fail(){
    sed -i "s/#assert false/assert false/g" features/step_definitions/b.rb
}

make_1_case_pass(){
    sed -i "s/assert false/#assert false/g" features/step_definitions/b.rb
}

clean_files()
{
    rm ${now}-test.json ${now}-rerun.json ${now}-new-report.json
    rm rerun.txt
}

log_format="-f json_pretty --strict -o"
cucumber_rerun_format=" -f pretty -f rerun -o "

run_case="cucumber ${log_format} ${now}-test.json ${cucumber_rerun_format} rerun.txt"
rerun_case_to_show="cucumber @rerun.txt"
rerun_case="cucumber @rerun.txt ${log_format} ${now}-rerun.json"

echo "---> One case will fail ..."
make_1_case_fail || true
echo ${run_case}
${run_case}

echo "---> Rerun will pass ..."
make_1_case_pass
echo ${rerun_case}

${rerun_case_to_show}
${rerun_case}

echo "---> Parser will show 5 cases are passed ..."

python3 cucumber_rerun_parser.py --rerun-report=${now}-rerun.json --origin-report=${now}-test.json --new-report=${now}-new-report.json
clean_files
