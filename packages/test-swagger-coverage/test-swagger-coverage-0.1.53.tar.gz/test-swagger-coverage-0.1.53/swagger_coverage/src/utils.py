import json
from typing import List

from swagger_coverage.src.files import FileOperation
from swagger_coverage.src.models import EndpointStatisticsHtml, PercentStatistic



def sort_requests_results(data: dict) -> List:
    """
    Sort request result
    """
    results = []
    for key, value in data.items():
        if value.get("time_executions") is not None:
            name = f"{value.get('tag')} ({value.get('method')} {value.get('path')})"
            if len(value.get("time_executions")) != 0:
                avg_time = sum(value.get("time_executions")) / len(
                    value.get("time_executions")
                )
            else:
                continue
            if avg_time > 3:
                color = "danger"
            elif avg_time > 1:
                color = "warning"
            else:
                color = "light"
            results.append({"name": name, "results": avg_time, "color": color})
    sorted_results = sorted(results, key=lambda d: d["results"], reverse=True)
    return sorted_results


def to_dict(data) -> dict:
    """
    Convert nested object to dict
    :return: dict
    """
    return json.loads(json.dumps(data, default=lambda o: o.__dict__))

def _percentage(part, whole) -> str:
    """
    Calculate percentage of verified statuses
    """
    res = 100 * float(part) / float(whole)
    return format(res, ".1f")

def _get_summary(diff: dict, data: dict):
    """
    Calculate report summary
    """
    count_success = 0
    count_of_unverified = 0
    for key, value in data.items():
        is_checked_list = [
            list(status.values())[0] for status in value.get("statuses")
        ]
        count_success += len([status for status in is_checked_list if status > 0])
        count_of_unverified += len(
            [status for status in is_checked_list if status == 0]
        )
    count_diff = len(list(diff.items()))
    count_total = count_success + count_of_unverified
    # get percent
    percentage_success = _percentage(count_success, count_total)
    percentage_unverified = _percentage(count_of_unverified, count_total)
    return (
        EndpointStatisticsHtml(
            count_total, count_success, count_of_unverified, count_diff
        ),
        PercentStatistic(percentage_success, percentage_unverified),
    )


def merge_results(paths: list):
    results = []
    for path in paths:
        results.append(FileOperation.load_json(str(path)))
    summary_res = {}
    for res in results:
        if summary_res.get("data") is None:
            summary_res["data"] = {"summary": res.get("data").get("summary")}
        else:
            pass
        if summary_res.get("data").get("swagger_data") is None:
            sum_data_dict = summary_res["data"]
            sum_data_dict["swagger_data"] = res.get("data").get("swagger_data")
        else:
            # Add new results
            swagger_data = summary_res.get("data")["swagger_data"]
            result_data = res.get("data").get("swagger_data")
            for route, value in  swagger_data.items():
                if result_data.get(route):
                    try:
                        for status in swagger_data[route].get('statuses'):
                            for key, value in status.items():
                                for status_res in result_data[route]['statuses']:
                                        status[key] = status.get(key, 0) + status_res.get(key, 0)
                                pass
                    except:
                            for status in result_data[route].get('statuses'):
                                for key, value in status.items():
                                    for status_res in swagger_data[route]['statuses']:
                                        if res.get("data").get(key):
                                            status[key] = summary_res.get(key,0) + status.get(key)
                    try:
                        if swagger_data[route].get('time_executions'):
                            swagger_data[route]['time_executions'] = swagger_data[route].get('time_executions') + (
                                result_data[route].get('time_executions', []))
                        else:
                            swagger_data[route]['time_executions'] = result_data[route].get('time_executions', []) + (
                                swagger_data[route].get('time_executions', []))
                    except:
                        pass
            summary_res["api_url"] = res.get("api_url")
            summary_res["swagger_url"] = res.get("swagger_url")
            summary_res["path"] = res.get("path")
            summary_res["data"]["diff"] = res["data"].get("diff")
    summary = _get_summary(summary_res['data']['diff'], summary_res['data']['swagger_data'])
    return summary_res, summary
