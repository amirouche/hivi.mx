#!/usr/bin/env python
import os

from memo import Memo
from memo.structures.base import Base

from dailymotion import embed


class Station(Base):

    def __init__(self, server, key):
        super(Station, self).__init__(server, key)
        self.viewers = 0
        self.playing = None
        self.last = None
        self.videos = {}

    def infos(self):
        return dict(
            name=self.key,
            viewers=self.viewers,
            playing=self.playing
        )

    @staticmethod
    def CREATE_STATION(server, key):
        if key in server.dict:
            return 'station already exists'
        else:
            server.dict[key] = Station(server, key)
            return 'OK'

    @staticmethod
    def STATIONS(server):
        return [station.infos() for station in server.dict.values()]

    def NEXT(self):
        videos = sorted(self.videos.values(), key=lambda x: x['score'])
        if videos:
            video = videos[-1]
            self.playing = video
            self.videos.pop(video['id'])
            return video
        else:
            return None

    def JOIN(self):
        self.viewers += 1
        return {
            'videos': self.videos,
            'viewers': self.viewers,
            'playing': self.playing,
        }

    def LEAVE(self):
        self.viewers -= 1

    def VOTE(self, id):
        if id in self.videos:
            self.videos[id]['score'] = 1 + self.videos[id]['score']
            return 'OK'
        return 'not found'

    def ADD(self, url):
        video = embed(url, autoplay=True).value()
        id = url.split('/')[-1]
        if id not in self.videos:
            video['score'] = 1
            video['id'] = id
            self.videos[id] = video
        else:
            video = self.videos[id]
            video['score'] += 1
        return video


server = Memo(address='127.0.0.1', port=8008)
server.add_structure(Station)
server.start()
