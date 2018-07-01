/*global $, WebSocket, console, window, document*/
"use strict";

/**
 * Connects to Pi server and receives video data.
 */

function toggleDpadButtons(){
    var dpad_buttons = document.getElementsByClassName("d-button")
    for (var i = 0; i < dpad_buttons.length; i++) {
        dpad_buttons[i].disabled = !dpad_buttons[i].disabled
    }
}

function loadTitle(){
    $.getJSON( "static/config/config.json", function(json) {
            $('#title').text(json.title)
    })
}

function bindDpadButtons(_client){
    $( '#left-button' ).on({
         "touchstart": function(){ _client.move('LEFT') }
        ,"mousedown": function(){ _client.move('LEFT') }
        ,"touchend": function(){ _client.stop('LEFT') }
        ,"mouseup": function(){ _client.stop('LEFT') }
    })

    $( '#right-button' ).on({
         "touchstart": function(){ _client.move('RIGHT') }
        ,"mousedown": function(){ _client.move('RIGHT') }
        ,"touchend": function(){ _client.stop('RIGHT') }
        ,"mouseup": function(){ _client.stop('RIGHT') }
    })

    $( '#back-button' ).on({
         "touchstart": function(){ _client.move('BACKWARDS') }
        ,"mousedown": function(){ _client.move('BACKWARDS') }
        ,"touchend": function(){ _client.stop('BACKWARDS') }
        ,"mouseup": function(){ _client.stop('BACKWARDS') }
    })

    $( '#forward-button' ).on({
         "touchstart": function(){ _client.move('FORWARD') }
        ,"mousedown": function(){ _client.move('FORWARD') }
        ,"touchend": function(){ _client.stop('FORWARD') }
        ,"mouseup": function(){ _client.stop('FORWARD') }
    })
}

var client = {

    // Connects to Pi via websocket
    connect: function (port,callback) {
        var self = this, video = document.getElementById("video");

        this.socket = new WebSocket("ws://" + window.location.hostname + ":" + port + "/websocket");

        // Request the video stream once connected
        this.socket.onopen = function () {
            console.log("Connected!");
            self.readCamera();
            bindDpadButtons(self)  
        };

        this.socket.onmessage = function (messageEvent) {
            video.src = "data:image/jpeg;base64," + messageEvent.data;
        };
    },

    move: function(_direction){
        console.log('move '+_direction)
        this.socket.send(_direction);
    },

    stop: function(_direction){
        console.log('stop '+_direction)
        this.socket.send('STOP_'+_direction);
        
    },

    self_drive: function(){
        console.log('self_drive called')
        var self_drive_button = document.getElementById("action-button");

        if (self_drive_button.innerText == 'Self Drive !'){
            self_drive_button.innerText = 'Driving !'
            toggleDpadButtons()
            this.socket.send("self_drive");

        }else{
            self_drive_button.innerText = 'Self Drive !'
            toggleDpadButtons()
            this.socket.send("manual");
        }
    },

    save_frames: function(){
        console.log('save frames called')
        this.socket.send("save_frames");
    },

    // Requests video stream
    readCamera: function () {
        this.socket.send("read_camera");
    },

    setMode: function(_mode){
        // Set Train Mode
        if(_mode == 'True'){
            $('#action-button' )
                .text('Train ! ')
                .click(function(){
                    client.save_frames()
                })
        }else{
            $('#action-button' )
                .text('Self Drive ! ')
                .click(function(){
                    client.self_drive()
                })
        } 
    }
};


