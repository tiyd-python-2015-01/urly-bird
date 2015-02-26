from io import BytesIO
import matplotlib.pyplot as plt
import datetime
from .models import Timestamp


def create_plot(url_id):
    timestamp = Timestamp.query.filter_by(url_id=url_id).first_or_404()
    click_data = timestamp.clicks_per_day().items()
    click_data = sorted(click_data, key=lambda x: x[0])
    for click in click_data:
        print(click)

    dates = [datetime.datetime.strptime(c[0], "%Y-%m-%d") for c in click_data]
    num_clicks = [c[1] for c in click_data]
    fig = BytesIO()
    plt.plot_date(x=dates, y=num_clicks, fmt='-')
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return fig
