from json.decoder import JSONObject
from abstracts.abstract_displayer import AbstractDisplayer
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class QueryDisplayer(AbstractDisplayer):

    def make_table(self, json_response: dict, image_url: str) -> None:
        dataframe = self._make_dataframe(json_response)

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(dataframe.columns),
                        line_color='darkslategray',
                        fill_color='seashell',
                        height=30),
            cells=dict(values=[dataframe[k].tolist() for k in dataframe.columns[:]],
                       line_color='darkslategray',
                       fill_color='white',
                       height=30)
        )])
        fig.update_layout(
            height = len(dataframe) * 55 + 100,
            width = len(dataframe.columns) * 500
        )

        img_bytes = fig.to_image(format="png")
        f = open(image_url, 'wb')
        f.write(img_bytes)
        f.close()

    def make_bargraph(self, json_response: dict, image_url: str, xaxis_metric: str, yaxis_metric: str):
        dataframe = self._make_dataframe(json_response)
        self._make_image(px.bar(dataframe, xaxis_metric, yaxis_metric), image_url)

    def make_scatter(self, json_response: dict, image_url: str, xaxis_metric: str, yaxis_metric: str):
        dataframe = self._make_dataframe(json_response)
        self._make_image(px.scatter(dataframe, xaxis_metric, yaxis_metric), image_url)

    def make_line(self, json_response: dict, image_url: str, xaxis_metric: str, yaxis_metric: str):
        dataframe = self._make_dataframe(json_response)
        self._make_image(px.line(dataframe, xaxis_metric, yaxis_metric), image_url)

    def _make_dataframe(self, json_response: dict):
        data = []
        data_dict = {}
        column_names = []

        if "tables" not in json_response:
            return None

        for column in json_response['tables'][0]['columns']:
            column_names.append(column['name'])
        for row in json_response['tables'][0]['rows']:
            data.append(row)

        return pd.DataFrame(data, columns=column_names)

    def _make_image(self, fig, image_url: str):
        img_bytes = fig.to_image(format="png")
        f = open(image_url, 'wb')
        f.write(img_bytes)
        f.close()
