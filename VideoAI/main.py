import argparse
import matplotlib.pyplot as plt
from google.cloud import videointelligence


def analyze_labels(path):
    """ Detects labels given a GCS path. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(path, features=features)
    print('\nNow processing ' + str(path) + ' for label annotations:')

    result = operation.result(timeout=90)
    print('\nFinished processing.')

    summary = []

    shot_labels = result.annotation_results[0].shot_label_annotations
    segment_labels = result.annotation_results[0].segment_label_annotations

    for i, shot_label in enumerate(shot_labels):
        label = shot_label.entity.description
        length = 0
        for j, segment in enumerate(shot_label.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            duration = end_time - start_time
            length += duration
        summary.append([label, round(length, 2)])

    summary = sorted(summary, key=lambda x: x[1], reverse=True)
    summary = summary[:10]

    labels = [i[0] for i in summary]
    values = [i[1] for i in summary]

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=180)
    title_string = 'Top 10 topics in ' + str(path)
    fig1.suptitle(title_string, fontsize=16)

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', help='GCS file path for label detection.')
    args = parser.parse_args()

    analyze_labels(args.path)
