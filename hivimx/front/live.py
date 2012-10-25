import json

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from memo_client import MemoClient

from dailymotion import Dailymotion


memo = MemoClient('127.0.0.1', 8008)
dailymotion = Dailymotion()


class Namespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    def emit_to_me(self, event, *args):
        pkt = dict(
             type="event",
             name=event,
             args=args,
             endpoint=self.ns_name)
        self.socket.send_packet(pkt)

    def broadcast_to_room(self, room, event, *args):
        """This is sent to *all* in the room (in this particular Namespace)"""
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'rooms' not in socket.session:
                continue
            if room_name in socket.session['rooms']:
                socket.send_packet(pkt)

    def recv_disconnect(self):
        if 'room' in self.session:
            name = self.session['room']
            memo.LEAVE(name)
            self.emit_to_room(name, 'leave')
        self.disconnect(silent=True)

    def on_stations(self):
        self.emit_to_me('stations', memo.STATIONS())

    def on_new_station(self, name):
        response = memo.CREATE_STATION(name)
        if response == 'OK':
            self.session['room'] = name
            self.emit_to_me(
                'join',
                name,
                {
            'videos': {},
            'viewers': 1,
            'playing': None,
            })
            self.join(name)
        # FIXME don't know what to do

    def on_join(self, name):
        try:
            infos = memo.JOIN(name)
        except:
            # the room doesn't exists redirect to root
            self.emit_to_me('root')
        else:
            self.session['room'] = name
            self.join(name)
            self.emit_to_me('join', name, infos)
            self.broadcast_to_room(name, 'new user')

    def on_search(self, q):
        videos = dailymotion.videos(search=q, limit=30)()
        videos = [video.value() for video in videos]
        self.emit_to_me('results', videos)

    def on_add(self, identifier):
        url = 'http://www.dailymotion.com/video/' + identifier
        room = self.session['room']
        video = memo.ADD(room, url)
        self.broadcast_to_room(room, 'add', video)

    def on_vote(self, identifier):
        room = self.session['room']
        memo.VOTE(room, identifier)

    def on_next(self):
        room = self.session['room']
        self.broadcast_to_room(room, 'next', memo.NEXT(room))
