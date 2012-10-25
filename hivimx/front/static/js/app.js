WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

var myplayer;
// socket.io specific code

var left = $('#left');
var right = $('#right');

var socket = io.connect('http://localhost:8000/front');

socket.on('stations', function (stations) {
    if (stations.length > 0) {
	var nowplaying = $("#now-playing");
	var h2 = $('<h2>').text('Now playing');
	h2.appendTo(nowplaying);
	var list = $('<ul>');
	list.appendTo(nowplaying);
	for (var id=0; id<stations.length; id++) {
	    var station = stations[id];
	    var a = $('<a>').click(function() {
		socket.emit('join', station.name);
		return false
	    });
	    a.attr('class', 'station');
	    a.appendTo(list);
	    var li = $('<li>');
	    li.appendTo(a);
	    var h3 = $('<h3>').text('#' + station.name);
	    h3.appendTo(li);
	    if(station.playing) {
		a.append('<p>').text('Now playing: ' + station.playing);
	    }
	}
    }
});

function addVideo(video) {
    var queue = $('#queue');
    var li = $('<li>');
    li.data('video', video);
    li.text(video.title);
    li.appendTo(queue);
    li.click(function() {
	var self = $(this);
	if(!self.attr('class')) {
	    var video = self.data('video');
	    socket.emit('vote', video.id);
	    self.attr('class', 'vote');
	}
    });
    return li;
}

function play(video) {
    var frame = $('#frame');
    frame.data('playing', video);
    if(!myplayer) {
	myplayer = DM.player("player", {video: video.id, height: 420, width: 560, params: {autoplay: 1}})
	myplayer.addEventListener(
	    "apiready", 
	    function(e) {
		e.target.play();
	    }
	);
	myplayer.addEventListener(
	    "ended",
	    function(e) {
		console.log("ended");
		var next = frame.data('next');
		if(next) {
		    myplayer.load(next.id);
		    frame.data('playing', next);
		    frame.data('next', undefined);
		} else {
		    socket.emit('next');
		}
	    }
	);
    } else {
	myplayer.load(video.id);
    }
}


socket.on('join', function(name, infos) {
    window.location.hash = name;
    $('.home').hide();
    var title = $('.main h1');
    var a = $('<a>');
    a.attr('href', '#'+name);
    a.text('#' + name);
    a.appendTo(title);
    $('.main').show();
    var frame = $('#frame');
    frame.data('playing', undefined);
    if(infos.playing) {
	play(infos.playing);
    } else {
	socket.emit('next');
    }
    playing = frame.data('playing');
    for(var key in infos.videos) {
	var video = infos.videos[key];
	if (playing.id != video.id) {
	    addVideo(video);
	}
    }
});

socket.on('next', function(video) {
    console.log(video);
    play(video);
    var queue = $('#queue');
    for(var i = 0; i<queue.children().length; i++) {
	var li = $(queue.children()[i]);
	if(li.data('video')['id'] == video.id) {
	    li.remove();
	    break;
	}
    }
});

socket.on('root', function() {
    window.location.href = '/'
});

var station = window.location.hash;
if(station) {
    socket.emit('join', station.substr(1));
} else {
    socket.emit('stations');
}


$('.home form').submit(function() {
    var input = $('#station-name');
    var name = input.val();
    socket.emit('new_station', name);
    return false;
});

$('.main form').submit(function() {
    var input = $('.main form input[type="text"]');
    socket.emit('search', input.val());
    return false;
});


socket.on('results', function(videos) {
    var results = $('#results');
    results.html('');
    for(var i=0; i<videos.length; i++) {
	var video = videos[i];	
	var li = $('<li>');
	li.data('video', video.id);
	li.text(video.title);
	li.click(function() {
	    socket.emit('add', $(this).data('video'));
	});
	li.appendTo(results);
    }
});


socket.on('add', function(video) {
    var li = addVideo(video);
    var frame = $("#frame");
    if(!frame.data("playing")) {
	li.remove();
	play(video);
    }
});
