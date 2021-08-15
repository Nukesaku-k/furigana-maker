#!/usr/bin/env python
# coding: UTF-8
# usage: ./api.py

# from dataclasses import dataclass, field
# from typing import List
# import json
import requests
# import xml.etree.ElementTree as ET
import xmltodict


from flask import Blueprint
from flask_restful import Api, Resource, reqparse, request

api_bp = Blueprint('api', __name__, url_prefix='/api')
post_parser = reqparse.RequestParser()

ENDPOINT = "https://jlp.yahooapis.jp/FuriganaService/V1/furigana"
API_KEY = "___TO_BE_SET___"  # Client ID

FURIGANA = '<ruby>{surface}<rp>（</rp><rt>{furigana}</rt><rp>）</rp></ruby>'
BRAKETS = '{surface}（{furigana}）'


class List(Resource):
    def post(self):
        data = {
            "appid": API_KEY,
            "grade": request.form['grade'],
            "sentence": request.form['sentence'].replace('\n', '')
        }
        convert_type = request.form['type']
        response = requests.post(ENDPOINT, data=data)
        word_dict = xmltodict.parse(response.text)
        word_line = ''
        word_list = convert_to_word_list(word_dict['ResultSet']['Result']['WordList']['Word'])
        for word_set in word_list:
            if has_hurigana(word_set):
                if kana_mixed(word_set):
                    for subword_set in word_set['SubWordList']['SubWord']:
                        if has_hurigana(subword_set):
                            word_line += get_format(convert_type).format(
                                surface=trim_surface(subword_set),
                                furigana=trim_furigana(subword_set)
                            )
                        else:
                            word_line += trim_surface(subword_set)
                else:
                    word_line += get_format(convert_type).format(
                        surface=trim_surface(word_set),
                        furigana=trim_furigana(word_set)
                    )
            else:
                word_line += trim_surface(word_set)
        # print(word_line)
        return word_line


def kana_mixed(word_set: dict) -> bool:
    return 'SubWordList' in word_set


def convert_to_word_list(word_set: dict) -> list:
    word_list = []
    if type(word_set) == list:
        word_list = word_set  # Orverwrite
    else:
        word_list.append(word_set)
    return word_list


def has_hurigana(word_set: dict) -> bool:
    if 'Furigana' in word_set:
        return word_set['Surface'] != word_set['Furigana']


def ruby_or_not(convert_type: str) -> bool:
    return convert_type == '1'


def trim_surface(word_set: dict) -> str:
    return word_set['Surface']


def trim_furigana(word_set: dict) -> str:
    return word_set['Furigana']


def get_format(convert_type: dict) -> str:
    if convert_type == '1':
        return FURIGANA
    else:
        return BRAKETS


api = Api(api_bp)
api.add_resource(List, '/list')


# def test(sentence: str, grade: str, convert_type: str):
#     data = {
#         "appid": API_KEY,
#         "grade": grade,
#         "sentence": sentence
#     }
#
#     response = requests.post(ENDPOINT, data=data)
#     word_dict = xmltodict.parse(response.text)
#     word_line = ''
#     word_list = convert_to_word_list(word_dict['ResultSet']['Result']['WordList']['Word'])
#     for word_set in word_list:
#         if has_hurigana(word_set):
#             if kana_mixed(word_set):
#                 for subword_set in word_set['SubWordList']['SubWord']:
#                     if has_hurigana(subword_set):
#                         word_line += get_format(convert_type).format(
#                             surface=trim_surface(subword_set),
#                             furigana=trim_furigana(subword_set)
#                         )
#                     else:
#                         word_line += trim_surface(subword_set)
#             else:
#                 word_line += get_format(convert_type).format(
#                     surface=trim_surface(word_set),
#                     furigana=trim_furigana(word_set)
#                 )
#         else:
#             word_line += trim_surface(word_set)
#     print(word_line)
#
#
# if __name__ == '__main__':
#     param = {
#         'sentence': '昨今、若者の車離れが問題となっている。',
#         'grade': '1',
#         'convert_type': '1'
#     }
#     test(**param)
