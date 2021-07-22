#!/usr/bin/env python
# coding: UTF-8
# usage: ./api.py

# import json
import requests
import xml.etree.ElementTree as ET
# import xmltodict


from flask import Blueprint
from flask_restful import Api, Resource, reqparse, request

api_bp = Blueprint('api', __name__, url_prefix='/api')
post_parser = reqparse.RequestParser()

ENDPOINT = "https://jlp.yahooapis.jp/FuriganaService/V1/furigana"
API_KEY = "___TO_BE_SET___"  # Client ID


class List(Resource):
    def post(self):
        ret_html = ""
        sentence = request.form['sentence']
        grade = request.form['grade']
        convert_type = request.form['type']

        data = {
            "appid": API_KEY,
            "grade": grade,
            "sentence": sentence
        }

        response = requests.post(ENDPOINT, data=data)
        root = ET.fromstring(response.text)

        ruby_dict = {}
        text = []
        for line in root:
            for word_list in line[0]:
                if len(word_list) == 1:
                    text.append(word_list[0].text)
                elif len(word_list) == 4:
                    text.append(word_list[3][0][0].text)
                    if len(word_list[3]) == 3:
                        text.append(word_list[3][1][0].text)
                        ruby_dict[word_list[3][1][0].text] = word_list[3][1][1].text
                        text.append(word_list[3][2][0].text)
                    else:
                        if word_list[3][0][0].text != word_list[3][0][1].text:
                            ruby_dict[word_list[3][0][0].text] = word_list[3][0][1].text
                            text.append(word_list[3][1][0].text)
                        else:
                            ruby_dict[word_list[3][1][0].text] = word_list[3][1][1].text
                            text.append(word_list[3][1][0].text)
                else:
                    text.append(word_list[0].text)
                    ruby_dict[word_list[0].text] = word_list[1].text
        if convert_type == '1':
            for word in text:
                if word in list(ruby_dict.keys()):
                    ret_html += "<ruby>{}<rp>".format(word)
                    ret_html += "（</rp><rt>{}</rt><rp>）</rp></ruby>".format(ruby_dict[word])
                else:
                    ret_html += word
        else:
            for word in text:
                if word in list(ruby_dict.keys()):
                    ret_html += "{}".format(word)
                    ret_html += "（{}）".format(ruby_dict[word])
                else:
                    ret_html += word
        return ret_html


api = Api(api_bp)
api.add_resource(List, '/list')


# def test(sentence: str, grade: str):
#     data = {
#         "appid": API_KEY,
#         "grade": grade,
#         "sentence": sentence
#     }
#
#     response = requests.post(ENDPOINT, data=data)
#     dict = xmltodict.parse(response.text)
#     print(json.dumps(dict, ensure_ascii=False, indent=2))
#
#
# if __name__ == '__main__':
#     param = {
#         "sentence": "私は、山田太郎です。今日は学校で図画工作の授業で、初めての写生をしました",
#         "grade": "1"
#     }
#     test(**param)
