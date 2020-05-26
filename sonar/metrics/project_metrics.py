from prometheus_client.core import GaugeMetricFamily


def make_metrics(projects):
    list_metrics = []

    # Total Projects
    metric = GaugeMetricFamily(
        'sonar_projects_total',
        'Total projects in Sonar',
        labels=None
    )

    metric.add_metric(
        labels=[],
        value=projects.get_total_projects()
    )

    list_metrics.append(metric)

    # Group Metric Status
    list_status_label = projects.get_status_labels()
    for status in list_status_label:
        metric = GaugeMetricFamily(
            'sonar_projects_{}'.format(status.lower()),
            'Number {} project in Sonar'.format(status),
            labels=None
        )

        metric.add_metric(
            labels=[],
            value=projects.get_total_status(status)
        )

        list_metrics.append(metric)

    # Projects Statuses
    for prj_name in projects.project_info:
        metric_name = prj_name.replace("-", "_")
        metric = GaugeMetricFamily(
            'sonar_project_{}'.format(metric_name),
            'Information of {} project'.format(metric_name),
            labels=['measure']
        )
        for keys, values in projects.get_project_measures(prj_name).items():
            metric.add_metric(
                labels=[keys],
                value=values
            )
        list_metrics.append(metric)

    # Statuses divided by projects
    for measure in projects.measures_total.keys():
        metric = GaugeMetricFamily(
            'sonar_measures_{}_by_project'.format(measure.lower()),
            'Display status {} divided by projects'.format(measure),
            labels=['prj']
        )

        for key, value1 in projects.get_list_project_info().items():
            metric.add_metric(
                labels=[key],
                value=value1['measures'][measure]
            )

        list_metrics.append(metric)

    # Measures
    for measure in projects.measures_total.keys():
        metric = GaugeMetricFamily(
            'sonar_measures_{}'.format(measure.lower()),
            '# of {} in Sonar'.format(measure),
            labels=None
        )

        metric.add_metric(
            labels=[],
            value=projects.measures_total[measure]
        )

        list_metrics.append(metric)

    return list_metrics
