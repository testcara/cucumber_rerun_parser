import json
import sys
import datetime
import logging
import argparse

logging.basicConfig(
    format='%(asctime)s [%(filename)s::%(funcName)s] %(levelname)s %(message)s',
    level=logging.DEBUG
)


class CucumberRerunReprotParser(object):
    """
    The class is used to parser the rerun json report, then
    based the result, refresh the original cucumber report
    and finally generate one new report file.
    Note:
    1. Only json format report can be processed.
    2. The script will not update the files you provide.
    3. One new json report will be generated

    So if you are using cucumber to show your report, please make sure you just
    provide meaningful reports.

    Examples:
    I use the following commands to [re]run cases then generate report:
    cucumber --format json_pretty --strict -o test.json -f pretty -f rerun
    --out rerun.txt || cucumber @rerun.txt --format json_pretty --strict -o rerun.json
    python3 parser_rerun.py --rerun-report=rerun.json --origin-report=test.json
    --new-report=new-report.json
    """

    def __init__(self, rerun_json_report, original_json_report, new_json_report):
        self.rerun_json_report = rerun_json_report
        self.original_json_report = original_json_report
        self.new_json_report = new_json_report

    def __read_json(self, file):
        """
        Read json files and return raw_data
        """
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except Exception:
            raise Exception('The file {} cannot be found or read'.format(file))

    def __write_json(self, json, new_json_report):
        """
        Write json files with specify content
        """
        try:
            with open(new_json_report, 'w+') as f:
                f.write(json)
        except:
            raise Exception(
                'Cannot write the new report {} with content {}'.format(new_json_report))

    def __get_total_scenarios_num(self, data):
        scenarios_num = 0
        for features in data:
            for element in features['elements']:
                if element['type']=='scenario':
                    scenarios_num += 1
        return scenarios_num


    def get_passed_scenario_from_rerun_report(self):
        """
        return {}
        """
        logging.info('Read the data from {}'.format(self.rerun_json_report))
        raw_data = self.__read_json(self.rerun_json_report)

        logging.info('Get scenarios and results maps from {}'.format(
            self.rerun_json_report))
        scenarios_and_results = {}
        # It is the feature number not the scenario number
        scenarios_num = self.__get_total_scenarios_num(raw_data)

        scenarios_and_results={}
        if scenarios_num > 0 :
            for features in raw_data:
                for element in features['elements']:
                    if element['type']=='scenario':
                        id=element['id']
                        result='passed'
                        for step in element['steps']:
                            if step['result']['status']=='failed':
                                result='failed'
                        scenarios_and_results[id]=result

            if len(scenarios_and_results) == scenarios_num:
                logging.info('Have got all scenarios and results:')
                logging.info(scenarios_and_results)
            else:
                raise Exception(
                    'Scenarios total num is changed! Something should be wrong!')

            scenarios_and_results_copy = scenarios_and_results.copy()
            if 'failed' in list(scenarios_and_results.values()):
                logging.info('Pop failed scenarios')
                for key in scenarios_and_results_copy.keys():
                    if scenarios_and_results[key] == 'failed':
                        scenarios_and_results.pop(key)
            else:
                logging.info('Rerun scenarios are passed.')

            if len(scenarios_and_results) <= 0:
                logging.info('There is no rerun passed scenarios.')
                return {}
            else:
                logging.info('Have got all passed scenarios:')
                logging.info(scenarios_and_results)
            return scenarios_and_results
        else:
            logging.info("There is no content in {}".format(
                self.rerun_json_report))
            return {}

    def refresh_report_with_rerun_passed_scenarios(self, scenarios_and_results):
        """
        return json or none
        """
        if len(scenarios_and_results) <= 0:
            logging.info(
                'No rerun passed scenarios. No refreshment is needed!')
            return
        else:
            logging.info("Update the report {} with rerun results {}".format(
                self.original_json_report, scenarios_and_results))
            logging.info("Get the data from {}".format(
                self.original_json_report))
            raw_data = self.__read_json(self.original_json_report)

            scenarios_num = self.__get_total_scenarios_num(raw_data)
            if scenarios_num > 0:
                logging.info(
                    "There are {} scenarios totally.".format(str(scenarios_num)))
                logging.info("Rewrite the results of {} scenarios".format(
                    str(len(scenarios_and_results))))

                for features in raw_data:
                    for element in features['elements']:
                        if element['type']=='scenario' and element['id'] in scenarios_and_results:
                            for step in element['steps']:
                                duration='3m'
                                step['result']= {'status': 'passed', 'duration': 9187}

                if self.__get_total_scenarios_num(raw_data) == scenarios_num:
                    logging.info("Complete the result refresh")
                    logging.info(
                        "Now there are {} cases passed".format(str(scenarios_num)))
                    return json.dumps(raw_data, indent=4)
                else:
                    raise Exception(
                        'Scenarios total num is changed! Something should be wrong!')
            else:
                logging.info("There is no {} or content in the file.".format(
                    self.original_json_report))
                return

    def write_new_report(self, json):
        logging.info('Write the new json report {}'.format(
            self.new_json_report))
        if json is not None:
            self.__write_json(json, self.new_json_report)
            logging.info('Complete to generate the new report {}'.format(
                self.new_json_report))
        else:
            logging.info('There is no content to write')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rerun-report', help='The rerun json report path')
    parser.add_argument('--origin-report', help='The origin json report path')
    parser.add_argument('--new-report', help='The new json report path')

    args = parser.parse_args()
    rerun_report = args.rerun_report
    origin_report = args.origin_report
    new_report = args.new_report
    parser = CucumberRerunReprotParser(rerun_report, origin_report, new_report)
    passed_scenarios = parser.get_passed_scenario_from_rerun_report()
    new_report_json = parser.refresh_report_with_rerun_passed_scenarios(
        passed_scenarios)
    parser.write_new_report(new_report_json)
