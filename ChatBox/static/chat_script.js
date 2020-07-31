var loc = window.location
var formData = document.getElementById('form')
var wsStart = 'ws://'
if(loc.protocol == "https:"){wsStart = "wss://"}
var endpoint = wsStart+loc.host+loc.pathname
var chatSocket = new ReconnectingWebSocket(endpoint)
chatSocket.onmessage = function(e){
    e = JSON.parse(e.data)
    var msg = e['text']
    var username = e['username']
    document.getElementById('all-msgs').innerHTML+='<li class="list-group-item"><strong>'+username+"</strong>: "+msg+'</li>'
}
chatSocket.onerror = function(e){
}
chatSocket.onopen = function(e){
}
chatSocket.onclose = function(e){
}
document.getElementById("send-msg").onclick = function(e){
    e.preventDefault()
    var msgTxt = document.getElementById("msg-txt").value
    document.getElementById('msg-txt').value = ""
    chatSocket.send(msgTxt)
}